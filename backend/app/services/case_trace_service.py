"""Case Trace Service - assembles per-case trace views (FR-023, FR-024, REQ-DOMAIN-004)."""
import uuid

from sqlalchemy.orm import Session

from app.repositories.case_event_repository import CaseEventRepository
from app.repositories.case_repository import CaseRepository
from app.schemas.trace import (
    ApprovalStageDTO,
    CaseEventDTO,
    CaseStepDTO,
    CaseTraceResponse,
)
from app.services.agent_registry_service import AgentRegistryService
from app.services.visibility_policy_service import VisibilityPolicyService


class CaseTraceService:
    """Service assembling per-case trace timelines (FR-023, FR-024)."""

    # Future HITL approval gates (deferred from MVP but preserved as placeholders)
    APPROVAL_GATES = [
        {
            "stage_step_id": "ATS4",
            "stage_status": "future_visible_placeholder",
            "required_role": "specialist_reviewer",
            "notes": "Specialist fact review - deferred from MVP but preserved as visible governance gate",
        },
        {
            "stage_step_id": "ATS6",
            "stage_status": "future_visible_placeholder",
            "required_role": "specialist_reviewer",
            "notes": "Specialist determination verification - deferred from MVP but preserved as visible governance gate",
        },
        {
            "stage_step_id": "ATS8",
            "stage_status": "future_visible_placeholder",
            "required_role": "section_head",
            "notes": "Section Head decision review - deferred from MVP but preserved as visible governance gate",
        },
        {
            "stage_step_id": "ATS11",
            "stage_status": "future_visible_placeholder",
            "required_role": "policy_legal_approver",
            "notes": "Final approval - deferred from MVP but preserved as visible governance gate",
        },
        {
            "stage_step_id": "ATS14",
            "stage_status": "future_visible_placeholder",
            "required_role": "technical_committee",
            "notes": "Technical Committee adjudication - deferred from MVP but preserved as visible governance gate",
        },
    ]

    def __init__(
        self,
        session: Session,
        visibility_policy: VisibilityPolicyService | None = None,
        agent_registry: AgentRegistryService | None = None,
    ):
        self.session = session
        self.case_repo = CaseRepository(session)
        self.event_repo = CaseEventRepository(session)
        self.visibility_policy = visibility_policy or VisibilityPolicyService()
        self.agent_registry = agent_registry or AgentRegistryService()

    def get_case_trace(self, case_id: uuid.UUID, viewer_role: str) -> CaseTraceResponse:
        """Assemble complete case trace view (FR-023, FR-024).

        Steps:
        1. Query case_events ordered by occurred_at
        2. Group events by step_id
        3. Build steps array with status and decision_source
        4. Build events array
        5. Build approval_chain placeholders (ATS4, ATS6, ATS8, ATS11, ATS14)
        6. Apply visibility filter based on viewer role
        """
        # Load case
        case = self.case_repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")

        # Load events - pass UUID directly
        events = self.event_repo.list_by_case(case_id, order_by_occurred=True)

        # Build steps from events
        steps_map: dict[str, CaseStepDTO] = {}
        for event in events:
            if event.step_id not in steps_map:
                # Determine step status
                if event.step_id == case.current_step_id:
                    step_status = "current"
                elif event.event_type.startswith("validation_") and event.reason_code:
                    step_status = "blocked"
                elif event.event_type in ("route_resolved", "validation_passed"):
                    step_status = "completed"
                else:
                    step_status = "pending"

                # Determine actor label
                if event.actor_type == "agent":
                    agent = self.agent_registry.get_agent_by_id(event.actor_id)
                    actor_label = agent.agent_name if agent else event.actor_id
                elif event.actor_type == "system":
                    actor_label = "System"
                elif event.actor_type == "human":
                    actor_label = f"User {event.actor_id}"
                else:
                    actor_label = event.actor_id

                steps_map[event.step_id] = CaseStepDTO(
                    step_id=event.step_id,
                    step_status=step_status,
                    decision_source=event.decision_source,
                    actor_label=actor_label,
                    rationale_summary=event.rationale_summary,
                    evidence_ref=event.evidence_ref,
                    occurred_at=event.occurred_at,
                )

        steps = list(steps_map.values())

        # Build events array
        event_dtos = [
            CaseEventDTO(
                event_id=event.id,
                event_type=event.event_type,
                step_id=event.step_id,
                decision_source=event.decision_source,
                actor_type=event.actor_type,
                actor_id=event.actor_id,
                visible_to_external=event.visible_to_external,
                reason_code=event.reason_code,
                rationale_summary=event.rationale_summary,
                evidence_ref=event.evidence_ref,
                correlation_id=event.correlation_id,
                occurred_at=event.occurred_at,
            )
            for event in events
        ]

        # Build approval chain placeholders
        approval_chain = [ApprovalStageDTO(**gate) for gate in self.APPROVAL_GATES]

        # Build response
        trace = CaseTraceResponse(
            case_id=case.id,
            case_reference=case.case_reference,
            workflow_type=case.workflow_type,
            current_step_id=case.current_step_id,
            case_state=case.case_state,
            steps=steps,
            events=event_dtos,
            approval_chain=approval_chain,
        )

        # Apply visibility policy
        return self.visibility_policy.filter_for_viewer(trace, viewer_role)

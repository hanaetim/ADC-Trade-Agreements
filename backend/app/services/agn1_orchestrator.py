"""AGN1 Orchestrator - executes ATS1-ATS3 intake workflow (FR-002, FR-004, REQ-DOMAIN-002)."""
import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.services.agent_registry_service import AgentRegistryService
from app.services.audit_service import AuditService
from app.services.deterministic_rule_engine import DeterministicRuleEngine
from app.services.routing_service import RoutingService


@dataclass
class IntakeOutcome:
    """Result of AGN1 intake orchestration."""

    success: bool
    case_state: str  # intake_blocked, routed, queued_for_review
    current_step_id: str
    accountable_role: str
    reason_codes: list[str]
    agent_disposition: str  # completed, blocked, queued_for_review
    event_ids: list[uuid.UUID]


class Agn1Orchestrator:
    """Orchestrator executing ATS1-ATS3 intake workflow (FR-002, FR-004)."""

    def __init__(
        self,
        session: Session,
        agent_registry: AgentRegistryService | None = None,
        rule_engine: DeterministicRuleEngine | None = None,
        routing_service: RoutingService | None = None,
        audit_service: AuditService | None = None,
    ):
        self.session = session
        self.agent_registry = agent_registry or AgentRegistryService()
        self.rule_engine = rule_engine or DeterministicRuleEngine()
        self.routing_service = routing_service or RoutingService()
        self.audit_service = audit_service or AuditService(session)

    def start_intake(self, case_id: uuid.UUID, payload: dict[str, Any], correlation_id: str) -> IntakeOutcome:
        """Execute ATS1-ATS3 intake workflow (FR-002, FR-004).

        Steps:
        1. Resolve AGN1 from agent registry
        2. Evaluate completeness and eligibility (deterministic rules)
        3. If blocked, transition to intake_blocked state
        4. If passed, classify workflow and resolve routing
        5. Emit case_event and audit_log entries
        6. Return intake outcome
        """
        event_ids: list[uuid.UUID] = []
        reason_codes: list[str] = []

        # Step 1: Verify AGN1 is active
        agn1 = self.agent_registry.get_agent_by_id("AGN1")
        if not agn1 or not agn1.executable_in_mvp:
            # Should not happen in MVP but handle gracefully
            event_id = self.audit_service.record_security_audit(
                event_category="workflow",
                severity="error",
                actor_id="system",
                action="agn1_unavailable",
                correlation_id=correlation_id,
                entity_type="case",
                entity_id=str(case_id),
                details={"error": "AGN1 not available"},
                case_id=case_id,
            )
            event_ids.append(event_id)
            return IntakeOutcome(
                success=False,
                case_state="intake_blocked",
                current_step_id="ATS1",
                accountable_role="intake_exception_handler",
                reason_codes=["AGN1_UNAVAILABLE"],
                agent_disposition="blocked",
                event_ids=event_ids,
            )

        # Step 2: Evaluate completeness (ATS1)
        completeness_decision = self.rule_engine.evaluate_completeness(payload)
        event_id = self.audit_service.record_case_event(
            case_id=case_id,
            event_type="validation_completeness",
            step_id="ATS1",
            decision_source="deterministic_rule",
            actor_type="system",
            actor_id="DeterministicRuleEngine",
            correlation_id=correlation_id,
            visible_to_external=True,
            reason_code=completeness_decision.reason_code,
            rationale_summary=completeness_decision.rationale,
            payload={"outcome": completeness_decision.outcome, "blocking": completeness_decision.blocking},
        )
        event_ids.append(event_id)

        if completeness_decision.blocking:
            if completeness_decision.reason_code:
                reason_codes.append(completeness_decision.reason_code)
            return IntakeOutcome(
                success=False,
                case_state="intake_blocked",
                current_step_id="ATS1",
                accountable_role="intake_exception_handler",
                reason_codes=reason_codes,
                agent_disposition="blocked",
                event_ids=event_ids,
            )

        # Step 3: Evaluate eligibility (ATS2)
        eligibility_decision = self.rule_engine.evaluate_eligibility(payload)
        event_id = self.audit_service.record_case_event(
            case_id=case_id,
            event_type="validation_eligibility",
            step_id="ATS2",
            decision_source="deterministic_rule",
            actor_type="system",
            actor_id="DeterministicRuleEngine",
            correlation_id=correlation_id,
            visible_to_external=True,
            reason_code=eligibility_decision.reason_code,
            rationale_summary=eligibility_decision.rationale,
            payload={"outcome": eligibility_decision.outcome, "blocking": eligibility_decision.blocking},
        )
        event_ids.append(event_id)

        if eligibility_decision.blocking:
            if eligibility_decision.reason_code:
                reason_codes.append(eligibility_decision.reason_code)
            return IntakeOutcome(
                success=False,
                case_state="intake_blocked",
                current_step_id="ATS2",
                accountable_role="intake_exception_handler",
                reason_codes=reason_codes,
                agent_disposition="blocked",
                event_ids=event_ids,
            )

        # Step 4: Classify workflow and resolve routing (ATS3)
        classification = self.routing_service.classify_workflow(payload)
        step_resolution = self.routing_service.resolve_next_step(
            classification.workflow_type, current_step="ATS2"
        )
        role_resolution = self.routing_service.resolve_accountable_role(
            classification.workflow_type, step_resolution.next_step_id
        )

        # Record routing decision
        event_id = self.audit_service.record_case_event(
            case_id=case_id,
            event_type="route_resolved" if step_resolution.resolved else "route_unresolved",
            step_id="ATS3",
            decision_source="agent",
            actor_type="agent",
            actor_id="AGN1",
            correlation_id=correlation_id,
            visible_to_external=False,
            rationale_summary=f"Classified as {classification.workflow_type}, routed to {step_resolution.next_step_id}",
            payload={
                "workflow_type": classification.workflow_type,
                "next_step": step_resolution.next_step_id,
                "accountable_role": role_resolution.accountable_role,
                "resolved": step_resolution.resolved and role_resolution.resolved,
            },
        )
        event_ids.append(event_id)

        # Determine final state
        if step_resolution.resolved and role_resolution.resolved:
            case_state = "routed"
            agent_disposition = "completed"
        else:
            case_state = "queued_for_review"
            agent_disposition = "queued_for_review"
            reason_codes.append("UNRESOLVED_ROUTE")

        return IntakeOutcome(
            success=True,
            case_state=case_state,
            current_step_id=step_resolution.next_step_id,
            accountable_role=role_resolution.accountable_role,
            reason_codes=reason_codes,
            agent_disposition=agent_disposition,
            event_ids=event_ids,
        )

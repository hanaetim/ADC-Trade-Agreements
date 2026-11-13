"""Visibility Policy Service - role-based trace filtering (FR-024, REQ-DOMAIN-004)."""
from app.schemas.trace import CaseTraceResponse


class VisibilityPolicyService:
    """Service applying role-based visibility filters to trace data (FR-024)."""

    EXTERNAL_ROLES = {"external_applicant"}
    INTERNAL_ROLES = {
        "intake_exception_handler",
        "specialist_reviewer",
        "section_head",
        "policy_legal_approver",
        "technical_committee",
        "auditor",
    }

    def filter_for_viewer(self, trace: CaseTraceResponse, viewer_role: str) -> CaseTraceResponse:
        """Apply visibility policy based on viewer role (FR-024).

        Rules:
        - External applicants see only events where visible_to_external=True
        - Internal reviewers see all events
        - Restricted reasoning text filtered by role
        """
        if viewer_role in self.EXTERNAL_ROLES:
            # Filter events to only those visible to external
            trace.events = [event for event in trace.events if event.visible_to_external]

            # Filter steps to match remaining events
            visible_step_ids = {event.step_id for event in trace.events}
            trace.steps = [step for step in trace.steps if step.step_id in visible_step_ids]

            # Mask restricted rationale text
            for event in trace.events:
                if event.decision_source in ("agent", "deterministic_rule"):
                    # Keep summary but mask detailed internal reasoning
                    if event.rationale_summary and len(event.rationale_summary) > 200:
                        event.rationale_summary = event.rationale_summary[:200] + "..."

        # Internal roles see everything
        return trace

    def can_view_internal_reasoning(self, viewer_role: str) -> bool:
        """Check if viewer can see internal reasoning details."""
        return viewer_role in self.INTERNAL_ROLES

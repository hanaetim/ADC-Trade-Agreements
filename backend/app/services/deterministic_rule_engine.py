"""Deterministic Rule Engine - completeness and eligibility validation (FR-002)."""
from typing import Any


class RuleDecision:
    """Result of a deterministic rule evaluation."""

    def __init__(self, outcome: str, blocking: bool, reason_code: str | None = None, rationale: str | None = None):
        self.outcome = outcome  # passed, failed
        self.blocking = blocking
        self.reason_code = reason_code
        self.rationale = rationale


class DeterministicRuleEngine:
    """Evaluates mandatory field presence, eligibility rules, routing-target validity (FR-002)."""

    MANDATORY_FIELDS = {
        "submission_type",
        "submission_channel",
        "applicant_reference",
        "applicant_name",
    }

    VALID_WORKFLOW_TYPES = {
        "origin_ruling",
        "agreement_update",
        "inquiry",
        "study",
        "certificate_sampling",
        "dispute",
    }

    def evaluate_completeness(self, payload: dict[str, Any]) -> RuleDecision:
        """Check mandatory field presence (FR-002)."""
        missing_fields = []
        for field in self.MANDATORY_FIELDS:
            if field not in payload or not payload[field]:
                missing_fields.append(field)

        if missing_fields:
            return RuleDecision(
                outcome="failed",
                blocking=True,
                reason_code="INCOMPLETE_SUBMISSION",
                rationale=f"Missing required fields: {', '.join(missing_fields)}",
            )

        return RuleDecision(outcome="passed", blocking=False)

    def evaluate_eligibility(self, payload: dict[str, Any]) -> RuleDecision:
        """Check eligibility rules (FR-002).

        For MVP: validates submission_type is in allowed workflow taxonomy.
        """
        submission_type = payload.get("submission_type")

        if not submission_type or submission_type not in self.VALID_WORKFLOW_TYPES:
            return RuleDecision(
                outcome="failed",
                blocking=True,
                reason_code="INELIGIBLE_WORKFLOW",
                rationale=f"Invalid or unsupported workflow type: {submission_type}",
            )

        # Additional eligibility checks would go here for specific workflow types
        # For MVP, all valid workflow types are eligible

        return RuleDecision(outcome="passed", blocking=False)

    def evaluate_routing_constraints(self, workflow_type: str, next_step: str) -> RuleDecision:
        """Validate routing-target validity (FR-002, FR-004)."""
        # For MVP, ATS1→ATS2→ATS3 are valid intake steps
        valid_intake_steps = {"ATS1", "ATS2", "ATS3"}

        if next_step not in valid_intake_steps:
            return RuleDecision(
                outcome="failed",
                blocking=True,
                reason_code="UNRESOLVED_ROUTE",
                rationale=f"Step {next_step} not in MVP intake scope",
            )

        return RuleDecision(outcome="passed", blocking=False)

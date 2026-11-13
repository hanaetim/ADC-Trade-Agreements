"""Routing service for workflow classification and step resolution (FR-004)."""
from typing import Optional

from app.models.workflow_taxonomy import WorkflowType
from app.services.workflow_catalog_service import WorkflowCatalogService


class WorkflowClassification:
    """Result of workflow classification."""

    def __init__(self, workflow_type: WorkflowType, confidence: str = "high"):
        self.workflow_type = workflow_type
        self.confidence = confidence


class StepResolution:
    """Result of step resolution."""

    def __init__(self, next_step_id: str, resolved: bool = True):
        self.next_step_id = next_step_id
        self.resolved = resolved


class RoleResolution:
    """Result of role resolution."""

    def __init__(self, accountable_role: str, resolved: bool = True):
        self.accountable_role = accountable_role
        self.resolved = resolved


class RoutingService:
    """Service for workflow routing decisions (FR-004)."""

    def __init__(self, catalog_service: Optional[WorkflowCatalogService] = None):
        self.catalog_service = catalog_service or WorkflowCatalogService()

    def classify_workflow(self, case_payload: dict) -> WorkflowClassification:
        """Classify submission into workflow type.

        MVP implementation uses the submission_type directly.
        """
        submission_type = case_payload.get("submission_type")
        if not submission_type:
            # Default to inquiry if not specified
            return WorkflowClassification(WorkflowType.INQUIRY, confidence="low")

        try:
            workflow_type = WorkflowType(submission_type)
            return WorkflowClassification(workflow_type, confidence="high")
        except ValueError:
            # Invalid type defaults to inquiry
            return WorkflowClassification(WorkflowType.INQUIRY, confidence="low")

    def resolve_next_step(self, workflow_type: WorkflowType, current_step: Optional[str] = None) -> StepResolution:
        """Resolve next atomic step for workflow.

        MVP implements ATS1→ATS2→ATS3 intake flow.
        """
        if current_step is None or current_step == "ATS1":
            return StepResolution("ATS2", resolved=True)
        elif current_step == "ATS2":
            return StepResolution("ATS3", resolved=True)
        elif current_step == "ATS3":
            # After ATS3, routing is complete for MVP
            return StepResolution("ATS3", resolved=True)
        else:
            # Unresolved routing for steps outside MVP scope
            return StepResolution(current_step or "ATS1", resolved=False)

    def resolve_accountable_role(self, workflow_type: WorkflowType, next_step: str) -> RoleResolution:
        """Resolve accountable role for workflow and step.

        MVP routes all intake steps to intake_exception_handler.
        """
        role = self.catalog_service.get_step_role(next_step)
        if role:
            return RoleResolution(role, resolved=True)
        else:
            # Unresolved role defaults to intake handler
            return RoleResolution("intake_exception_handler", resolved=False)

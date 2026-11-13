"""Workflow Catalog Service - static workflow and step metadata (FR-004, FR-023)."""
from typing import Any


class WorkflowCatalogService:
    """Service providing static workflow and step metadata."""

    # Workflow metadata for all six workflow types
    WORKFLOW_METADATA: dict[str, dict[str, Any]] = {
        "origin_ruling": {
            "label": "Origin Ruling",
            "description": "Determine origin eligibility for trade agreement benefits",
            "mvp_active": True,
        },
        "agreement_update": {
            "label": "Agreement Update",
            "description": "Process changes to existing trade agreement terms",
            "mvp_active": False,
        },
        "inquiry": {
            "label": "Inquiry",
            "description": "Respond to trade agreement information requests",
            "mvp_active": False,
        },
        "study": {
            "label": "Compliance Study",
            "description": "Conduct Kyoto/TFA/SAFE compliance studies",
            "mvp_active": False,
        },
        "certificate_sampling": {
            "label": "Certificate Sampling",
            "description": "Sample and verify origin certificates",
            "mvp_active": False,
        },
        "dispute": {
            "label": "Dispute",
            "description": "Adjudicate disputed origin determinations",
            "mvp_active": False,
        },
    }

    # Step-to-role mapping for intake steps (ATS1-ATS3)
    STEP_ROLE_MAP: dict[str, str] = {
        "ATS1": "intake_exception_handler",
        "ATS2": "intake_exception_handler",
        "ATS3": "intake_exception_handler",
        # Future steps preserved as metadata
        "ATS4": "specialist_reviewer",
        "ATS6": "specialist_reviewer",
        "ATS8": "section_head",
        "ATS11": "policy_legal_approver",
        "ATS14": "technical_committee",
    }

    def get_workflow_metadata(self, workflow_type: str) -> dict[str, Any]:
        """Get metadata for a workflow type."""
        return self.WORKFLOW_METADATA.get(workflow_type, {})

    def get_step_role(self, step_id: str) -> str:
        """Get accountable role for a step ID."""
        return self.STEP_ROLE_MAP.get(step_id, "intake_exception_handler")

    def is_mvp_active_workflow(self, workflow_type: str) -> bool:
        """Check if workflow has active implementation in MVP."""
        metadata = self.get_workflow_metadata(workflow_type)
        return bool(metadata.get("mvp_active", False))

"""ICOS Registration Adapter - mocked for MVP (FR-001)."""
import uuid
from typing import Optional


class IcosRegistrationResult:
    """Result of ICOS registration synchronization."""

    def __init__(self, status: str, icos_reference_id: Optional[str] = None, message: Optional[str] = None):
        self.status = status  # 'pending', 'succeeded', 'failed'
        self.icos_reference_id = icos_reference_id
        self.message = message


class IcosRegistrationAdapter:
    """Mocked adapter for ICOS system-of-record registration (FR-001).

    In MVP, this is a mock that always succeeds. Future implementation
    will make real HTTP calls to ICOS REST API.
    """

    def register_case(self, case_payload: dict, correlation_id: str) -> IcosRegistrationResult:
        """Register a case with ICOS system of record.

        MVP mock implementation always returns success with generated reference.
        """
        # Mock: generate a fake ICOS reference
        icos_ref = f"ICOS-{uuid.uuid4().hex[:12].upper()}"

        # In real implementation, this would:
        # 1. Marshal case_payload to ICOS format
        # 2. POST to ICOS /api/cases endpoint
        # 3. Handle response and errors
        # 4. Return actual ICOS reference ID

        return IcosRegistrationResult(
            status="succeeded",
            icos_reference_id=icos_ref,
            message="Mock registration successful"
        )

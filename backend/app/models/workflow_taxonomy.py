"""Workflow taxonomy enumeration and metadata."""
from enum import Enum


class WorkflowType(str, Enum):
    """Workflow type taxonomy for case classification (FR-004)."""

    ORIGIN_RULING = "origin_ruling"
    AGREEMENT_UPDATE = "agreement_update"
    INQUIRY = "inquiry"
    STUDY = "study"
    CERTIFICATE_SAMPLING = "certificate_sampling"
    DISPUTE = "dispute"

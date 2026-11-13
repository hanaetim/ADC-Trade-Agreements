"""Seed data for development and testing."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database import engine
from app.models.audit_log import AuditLogModel
from app.models.case import CaseModel
from app.models.case_event import CaseEventModel
from app.models.user import UserModel


def seed_users(session: Session):
    """Seed default users with all roles."""
    users_data = [
        {"email": "external@example.com", "password": "External-pass-1", "role": "external_applicant"},
        {"email": "intake@example.com", "password": "Intake-pass-1", "role": "intake_exception_handler"},
        {"email": "specialist@example.com", "password": "Specialist-pass-1", "role": "specialist_reviewer"},
        {"email": "sectionhead@example.com", "password": "Section-pass-1", "role": "section_head"},
        {"email": "policy@example.com", "password": "Policy-pass-1", "role": "policy_legal_approver"},
        {"email": "technical@example.com", "password": "Technical-pass-1", "role": "technical_committee"},
        {"email": "auditor@example.com", "password": "Auditor-pass-1", "role": "auditor"},
    ]

    for user_data in users_data:
        # Check if user already exists
        stmt = select(UserModel).where(UserModel.email == user_data["email"])
        existing = session.execute(stmt).scalar_one_or_none()

        if not existing:
            user = UserModel(
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                role=user_data["role"],
                is_active=True,
            )
            session.add(user)

    session.commit()


def seed_cases(session: Session):
    """Seed sample cases in various states with events and audit logs."""
    cases_data: list[dict] = [
        {
            "case_reference": "IAO-2026-000001",
            "workflow_type": "origin_ruling",
            "submission_channel": "portal",
            "applicant_reference": "APP-2026-00123",
            "applicant_name": "Global Trading Corp",
            "goods_description": "Electronic components for industrial machinery",
            "origin_country_code": "CN",
            "agreement_reference": "FTA-GCC-RCEP",
            "case_state": "routed",
            "current_step_id": "ATS3",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": [],
        },
        {
            "case_reference": "IAO-2026-000002",
            "workflow_type": "agreement_update",
            "submission_channel": "email_intake",
            "applicant_reference": "APP-2026-00124",
            "applicant_name": "ACME Imports Ltd.",
            "goods_description": "Textile products",
            "origin_country_code": "IN",
            "agreement_reference": "FTA-GCC-INDIA",
            "case_state": "routed",
            "current_step_id": "ATS3",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": [],
        },
        {
            "case_reference": "IAO-2026-000003",
            "workflow_type": "inquiry",
            "submission_channel": "portal",
            "applicant_reference": "APP-2026-00125",
            "applicant_name": "Emirates Logistics",
            "goods_description": None,
            "origin_country_code": None,
            "agreement_reference": None,
            "case_state": "intake_blocked",
            "current_step_id": "ATS1",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": ["INCOMPLETE_SUBMISSION"],
        },
        {
            "case_reference": "IAO-2026-000004",
            "workflow_type": "study",
            "submission_channel": "internal_entry",
            "applicant_reference": "INT-2026-001",
            "applicant_name": "Internal Compliance Team",
            "goods_description": "Kyoto Convention compliance study",
            "origin_country_code": "AE",
            "agreement_reference": "KYOTO-TFA",
            "case_state": "queued_for_review",
            "current_step_id": "ATS3",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": [],
        },
        {
            "case_reference": "IAO-2026-000005",
            "workflow_type": "origin_ruling",
            "submission_channel": "portal",
            "applicant_reference": "APP-2026-00126",
            "applicant_name": "Test Imports Inc",
            "goods_description": "Testing goods for exception action tests",
            "origin_country_code": None,
            "agreement_reference": None,
            "case_state": "intake_blocked",
            "current_step_id": "ATS1",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": ["INCOMPLETE_SUBMISSION"],
        },
        {
            "case_reference": "IAO-2026-000006",
            "workflow_type": "inquiry",
            "submission_channel": "portal",
            "applicant_reference": "APP-2026-00127",
            "applicant_name": "Another Test Company",
            "goods_description": None,
            "origin_country_code": None,
            "agreement_reference": None,
            "case_state": "intake_blocked",
            "current_step_id": "ATS1",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": ["INCOMPLETE_SUBMISSION"],
        },
        {
            "case_reference": "IAO-2026-000007",
            "workflow_type": "agreement_update",
            "submission_channel": "portal",
            "applicant_reference": "APP-2026-00128",
            "applicant_name": "Third Test Corp",
            "goods_description": "Goods description",
            "origin_country_code": "US",
            "agreement_reference": "FTA-US-UAE",
            "case_state": "queued_for_review",
            "current_step_id": "ATS3",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": [],
        },
        {
            "case_reference": "IAO-2026-000008",
            "workflow_type": "origin_ruling",
            "submission_channel": "portal",
            "applicant_reference": "APP-2026-00129",
            "applicant_name": "Fourth Test Company",
            "goods_description": None,
            "origin_country_code": None,
            "agreement_reference": None,
            "case_state": "intake_blocked",
            "current_step_id": "ATS1",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": ["INCOMPLETE_SUBMISSION"],
        },
        {
            "case_reference": "IAO-2026-000009",
            "workflow_type": "study",
            "submission_channel": "internal_entry",
            "applicant_reference": "INT-2026-002",
            "applicant_name": "Fifth Test Entity",
            "goods_description": "Test goods",
            "origin_country_code": "AE",
            "agreement_reference": "TEST-REF",
            "case_state": "queued_for_review",
            "current_step_id": "ATS3",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": [],
        },
        {
            "case_reference": "IAO-2026-000010",
            "workflow_type": "inquiry",
            "submission_channel": "portal",
            "applicant_reference": "APP-2026-00130",
            "applicant_name": "Sixth Test Inc",
            "goods_description": None,
            "origin_country_code": None,
            "agreement_reference": None,
            "case_state": "intake_blocked",
            "current_step_id": "ATS1",
            "accountable_role": "intake_exception_handler",
            "registration_sync_status": "succeeded",
            "reason_codes_json": ["INCOMPLETE_SUBMISSION"],
        },
    ]

    for case_data in cases_data:
        # Check if case already exists
        stmt = select(CaseModel).where(CaseModel.case_reference == case_data["case_reference"])
        existing = session.execute(stmt).scalar_one_or_none()

        if not existing:
            case_id = uuid.uuid4()
            case = CaseModel(
                id=case_id,
                submitted_at=datetime.now(timezone.utc),
                case_reference=case_data["case_reference"],
                workflow_type=case_data["workflow_type"],
                submission_channel=case_data["submission_channel"],
                applicant_reference=case_data["applicant_reference"],
                applicant_name=case_data["applicant_name"],
                goods_description=case_data.get("goods_description"),
                origin_country_code=case_data.get("origin_country_code"),
                agreement_reference=case_data.get("agreement_reference"),
                case_state=case_data["case_state"],
                current_step_id=case_data["current_step_id"],
                accountable_role=case_data["accountable_role"],
                registration_sync_status=case_data["registration_sync_status"],
                reason_codes_json=case_data["reason_codes_json"],
            )
            session.add(case)
            session.flush()

            # Create sample events for each case showing completed ATS1-ATS3 steps
            correlation_id = f"seed-{case_data['case_reference']}"

            # ATS1: Completeness validation
            event1 = CaseEventModel(
                id=uuid.uuid4(),
                case_id=case_id,
                event_type="validation_completeness",
                step_id="ATS1",
                decision_source="deterministic_rule",
                actor_type="system",
                actor_id="DeterministicRuleEngine",
                visible_to_external=True,
                reason_code="INCOMPLETE_SUBMISSION" if case_data["case_state"] == "intake_blocked" else None,
                rationale_summary="Missing required fields: goods_description, origin_country_code" if case_data["case_state"] == "intake_blocked" else "All required fields present",
                correlation_id=correlation_id,
                payload_json={"outcome": "failed" if case_data["case_state"] == "intake_blocked" else "passed", "blocking": case_data["case_state"] == "intake_blocked"},
                occurred_at=datetime.now(timezone.utc),
            )
            session.add(event1)

            # ATS2: Eligibility validation (only if passed ATS1)
            if case_data["case_state"] != "intake_blocked":
                event2 = CaseEventModel(
                    id=uuid.uuid4(),
                    case_id=case_id,
                    event_type="validation_eligibility",
                    step_id="ATS2",
                    decision_source="deterministic_rule",
                    actor_type="system",
                    actor_id="DeterministicRuleEngine",
                    visible_to_external=True,
                    reason_code=None,
                    rationale_summary=f"Workflow type {case_data['workflow_type']} is eligible",
                    correlation_id=correlation_id,
                    payload_json={"outcome": "passed", "blocking": False},
                    occurred_at=datetime.now(timezone.utc),
                )
                session.add(event2)

                # ATS3: Routing resolution
                event3 = CaseEventModel(
                    id=uuid.uuid4(),
                    case_id=case_id,
                    event_type="route_resolved" if case_data["case_state"] == "routed" else "route_unresolved",
                    step_id="ATS3",
                    decision_source="agent",
                    actor_type="agent",
                    actor_id="AGN1",
                    visible_to_external=False,
                    reason_code=None,
                    rationale_summary=f"Classified as {case_data['workflow_type']}, routed to {case_data['current_step_id']}",
                    correlation_id=correlation_id,
                    payload_json={
                        "workflow_type": case_data["workflow_type"],
                        "next_step": case_data["current_step_id"],
                        "accountable_role": case_data["accountable_role"],
                        "resolved": case_data["case_state"] == "routed",
                    },
                    occurred_at=datetime.now(timezone.utc),
                )
                session.add(event3)

            # Create audit log entry for case registration
            audit_entry = AuditLogModel(
                id=uuid.uuid4(),
                case_id=case_id,
                event_category="workflow",
                severity="info",
                actor_id="system",
                action="case_registered",
                correlation_id=correlation_id,
                entity_type="case",
                entity_id=str(case_id),
                details_json={
                    "case_reference": case_data["case_reference"],
                    "workflow_type": case_data["workflow_type"],
                    "submission_channel": case_data["submission_channel"],
                },
                occurred_at=datetime.now(timezone.utc),
            )
            session.add(audit_entry)

    session.commit()


def run_seed():
    """Run all seed functions."""
    with Session(engine) as session:
        print("Seeding users...")
        seed_users(session)
        print("Seeding cases...")
        seed_cases(session)
        print("Seed data complete.")


if __name__ == "__main__":
    run_seed()

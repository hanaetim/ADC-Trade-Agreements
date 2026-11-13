"""Unit tests for Deterministic Rule Engine (FR-002)."""

from app.services.deterministic_rule_engine import DeterministicRuleEngine


def test_evaluate_completeness_success():
    """Test completeness validation passes with all required fields."""
    engine = DeterministicRuleEngine()

    payload = {
        "submission_type": "origin_ruling",
        "submission_channel": "portal",
        "applicant_reference": "APP-001",
        "applicant_name": "Test Applicant",
    }

    decision = engine.evaluate_completeness(payload)

    assert decision.outcome == "passed"
    assert decision.blocking is False
    assert decision.reason_code is None


def test_evaluate_completeness_fails_missing_fields():
    """Test completeness validation fails with missing required fields."""
    engine = DeterministicRuleEngine()

    payload = {
        "submission_type": "origin_ruling",
        # Missing: submission_channel, applicant_reference, applicant_name
    }

    decision = engine.evaluate_completeness(payload)

    assert decision.outcome == "failed"
    assert decision.blocking is True
    assert decision.reason_code == "INCOMPLETE_SUBMISSION"
    assert "submission_channel" in decision.rationale
    assert "applicant_reference" in decision.rationale
    assert "applicant_name" in decision.rationale


def test_evaluate_eligibility_success():
    """Test eligibility validation passes with valid workflow type."""
    engine = DeterministicRuleEngine()

    payload = {
        "submission_type": "origin_ruling",
    }

    decision = engine.evaluate_eligibility(payload)

    assert decision.outcome == "passed"
    assert decision.blocking is False


def test_evaluate_eligibility_fails_invalid_workflow():
    """Test eligibility validation fails with invalid workflow type."""
    engine = DeterministicRuleEngine()

    payload = {
        "submission_type": "invalid_workflow_type",
    }

    decision = engine.evaluate_eligibility(payload)

    assert decision.outcome == "failed"
    assert decision.blocking is True
    assert decision.reason_code == "INELIGIBLE_WORKFLOW"


def test_evaluate_routing_constraints_success():
    """Test routing constraint validation passes for MVP intake steps."""
    engine = DeterministicRuleEngine()

    decision = engine.evaluate_routing_constraints("origin_ruling", "ATS1")

    assert decision.outcome == "passed"
    assert decision.blocking is False


def test_evaluate_routing_constraints_fails_non_mvp_step():
    """Test routing constraint validation fails for non-MVP steps."""
    engine = DeterministicRuleEngine()

    decision = engine.evaluate_routing_constraints("origin_ruling", "ATS4")

    assert decision.outcome == "failed"
    assert decision.blocking is True
    assert decision.reason_code == "UNRESOLVED_ROUTE"


def test_all_workflow_types_are_valid():
    """Test all six workflow taxonomy values are recognized as eligible."""
    engine = DeterministicRuleEngine()

    workflow_types = [
        "origin_ruling",
        "agreement_update",
        "inquiry",
        "study",
        "certificate_sampling",
        "dispute",
    ]

    for workflow_type in workflow_types:
        decision = engine.evaluate_eligibility({"submission_type": workflow_type})
        assert decision.outcome == "passed", f"{workflow_type} should be eligible"

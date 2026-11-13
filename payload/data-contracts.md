# Data Contracts

Source contracts — entities, fixture shapes, state models, UI data contracts, and shared enums. Not target-language models. Field names are canonical and reused across `agent-register.md` and `mcp-tool-register.md`.

## Shared enums / value sets

- `case_type`: `advance_ruling | agreement_update | inquiry_internal | inquiry_external | ministry_sampling | dispute | objection`
- `recommendation`: `accept | reject | request_info | suspend`
- `approval_decision`: `approve | modify | reject`
- `reviewer_role`: `section_employee | section_head | policy_governance_director | legal_affairs | operations_head_centre | technical_committee`
- `origin_criterion`: `wholly_obtained | substantial_transformation | rvc | tariff_shift | de_minimis`
- `language`: `ar | en | bilingual`
- `case_status`: see state model below

## Entities

- **Case** — `case_id` (str), `case_type` (case_type), `status` (case_status), `customer_ref` (Optional[str]), `received_at` (datetime), `language` (language), `assigned_role` (Optional[reviewer_role])
- **ExtractedContent** — `commodity` (str), `hs_candidate` (Optional[str]), `declared_origin` (str), `agreement_ref` (str), `supporting_docs` ([Document]), `extraction_confidence` ({str: float}), `extraction_flags` ([str])
- **OriginRuleSet** — `agreement_ref` (str), `criteria` ([origin_criterion]), `rvc_threshold_pct` (Optional[float]) `[inferred]`, `de_minimis_pct` (Optional[float]) `[inferred]`, `rule_notes` ([str])
- **OriginDetermination** — `determined_origin` (str), `criterion_applied` (origin_criterion), `threshold_used` (Optional[float]), `determination_basis` ([str]), `confidence` (float)
- **ClassificationResult** — `hs_code` (str), `tariff_item` (str), `rationale` (str)
- **AdvanceRuling** — `ruling_id` (str), `case_id` (str), `determined_origin` (str), `validity_from` (date), `validity_to` (date) `[inferred]` config period, `fee_amount` (decimal) `[inferred]` config, `binding` (bool, =true), `published` (bool)
- **DraftDocument** — `draft_id` (str), `draft_type` (enum), `content_ar` (str), `content_en` (str), `rationale` ([str]), `draft_status` (enum(pending_review))
- **IssuedArtifact** — `artifact_id` (str), `type` (enum), `issued_at` (datetime), `approver_role` (reviewer_role), `validity_window` (Optional[{from,to}]), `binding` (bool)
- **CustomsDeclaration** — `declaration_ref` (str), `preferential_treatment_field` (str), `origin_field` (str), `line_items` ([LineItem]), `status` (str)
- **DisputeCase** — `dispute_id` (str), `declaration_ref` (str), `level` (enum(centre, department, committee)), `objection_filed_at` (Optional[datetime]), `notification_at` (Optional[datetime]), `supporting_evidence` ([Document])
- **DeclarationCorrection** — `declaration_ref` (str), `corrected_fields` ([enum(preferential_treatment_field, origin_field)]), `rationale` (str)
- **CertificateVerification** — `certificate_ref` (str), `status` (enum(pending, valid, invalid)), `response_detail` (Optional[str]), `images` ([Document])
- **ValidationResult** — `overall` (enum(passed, warned, blocked)), `rule_outcomes` ([RuleOutcome])
- **RuleOutcome** — `rule_id` (str), `result` (enum(pass, fail)), `severity` (enum(blocking, request_info, warn)), `detail` (str)
- **AuditEvent** — `case_id` (str), `step_id` (str), `agent_id` (str), `actor` (str), `action` (str), `before_state` (str), `after_state` (str), `rationale` (str), `timestamp` (datetime)
- **Notification** — `notification_type` (enum), `recipient_role` (str), `case_id` (str), `sent_at` (datetime)

## Fixture shapes (mock systems)

All external systems mocked. Fixtures must cover variety so every atomic step, branch, and HITL gate is demonstrable.

### Integration notes (variety the fixtures must exercise)

- **Advance-ruling requests:** ≥ 8 cases covering accept, reject-for-fee-unpaid, reject-for-multiple-commodities, reject-for-open-declaration, request-additional-info, suspend, and at least one of each origin criterion (wholly-obtained, substantial transformation, RVC, tariff-shift). Arabic and English submissions both represented.
- **Agreement update letters:** ≥ 3 FCA letters — one requiring a tariff cross-check, one requiring an amendment with legal-review comments, one accepted without comments.
- **Inquiries:** internal and external, including one needing a classification-section cross-check.
- **Disputes/objections:** at least one in-time and one out-of-time objection (to exercise BR-14), one requiring Ministry-of-Economy certificate verification (valid and invalid responses).
- **Customs declarations:** ≥ 10 with varied agreements/origin fields across transport modes and free-zone/warehouse origins, to feed determination and dispute flows.
- **Ministry sampling:** one ministry letter + a period with enough declarations to sample from.

### Shape examples

```json
// AdvanceRulingRequest (digital customs platform fixture)
{
  "case_id": "AR-2026-0001",
  "customer_ref": "TRD-4471",
  "commodity": "aluminium alloy extruded profiles",
  "hs_candidate": "7604.21",
  "declared_origin": "AE",
  "agreement_ref": "GCC-FTA",
  "fee_payment_status": "paid",
  "supporting_docs": ["invoice.pdf", "bom.pdf"],
  "language": "en"
}
```
```json
// AgreementUpdateLetter (FCA fixture)
{
  "letter_id": "FCA-UPD-2026-014",
  "update_list": [
    {"agreement_ref": "GCC-India-FTA", "change": "preferential rate reduced", "affected_hs": ["8703"]}
  ],
  "requires_classification_check": true
}
```
```json
// Objection (exercises BR-14)
{
  "dispute_id": "OBJ-2026-0007",
  "declaration_ref": "DCL-55120",
  "notification_at": "2026-10-01T09:00:00",
  "objection_filed_at": "2026-11-20T09:00:00",
  "reason": "disputes origin field correction"
}
```

## Case state model

`status` transitions (advance-ruling exemplar; other workflows reuse the review sub-states):

- **States:** `received`, `validating`, `rejected_incomplete`, `extracting`, `info_requested`, `suspended`, `determining`, `pending_review`, `in_review`, `approved`, `issued`, `published`, `objection_filed`, `committee_review`, `closed`
- **Transitions (selected):**
  - `received → validating` (AGN1 / Rule Engine)
  - `validating → rejected_incomplete` (any BR-02 blocking failure) [terminal-ish → `closed`]
  - `validating → extracting` (BR-02 pass)
  - `extracting → info_requested` (BR-04.1 fail) ; `info_requested → extracting` (customer responds)
  - `extracting → determining` (confidence ok)
  - `determining → suspended` (recommendation=suspend) ; `suspended → determining` (info supplied)
  - `determining → pending_review` (recommendation=accept/reject)
  - `pending_review → in_review → approved | pending_review` (reviewer approve / modify-return)
  - `approved → issued → published` (advance ruling only)
  - `issued → objection_filed → committee_review` (customer objects)
  - `committee_review → closed` (out_of_time auto-reject via BR-14, or committee uphold)
  - `committee_review → determining` (committee modify → re-issue)
- **Terminal states:** `closed`, `published` (rulings), `rejected_incomplete`(→closed)

## Review (HITL) sub-state model

Applies to every reviewer tier and draft type:

- **States:** `pending_review`, `in_review`, `changes_requested`, `approved`, `rejected`
- **Transitions:** `pending_review → in_review`; `in_review → approved`; `in_review → changes_requested → pending_review` (loop back to drafter); `in_review → rejected`
- **Terminal:** `approved`, `rejected`

## UI data contracts (bilingual web app, AR/EN)

Every screen must render AR (RTL) and EN (LTR).

- **Case inbox / queue (role-scoped):**
  - Data consumed: `[Case]` from TOL1 filtered by `assigned_role`; `case_type`, `status`, `received_at`
  - Actions: open case, claim for review
- **Case detail + step/trace view (visibility requirement):**
  - Data consumed: `Case`; ordered `[AuditEvent]` from TOL7 (step_id, agent_id, action, before/after state, rationale); `ExtractedContent`; `OriginDetermination` (criterion_applied, threshold_used, determination_basis, confidence); `recommendation`
  - Actions: none (read/inspect) — this is the "every atomic step and agent at work" surface
- **Review screen (HITL gate):**
  - Data consumed: `DraftDocument` (content_ar, content_en, rationale); resolved `approver_role` from BR-11; `ValidationResult`
  - Actions: approve / request-changes (loops to drafter) / reject — enforced against the reviewer's role
- **Origin determination panel:**
  - Data consumed: `OriginDetermination`, `OriginRuleSet` (criteria + thresholds), `ClassificationResult`
  - Actions: none (read); feeds the review screen
- **Dispute / objection screen:**
  - Data consumed: `DisputeCase`, `time_limit_result` (BR-14), `adjudication_decision`, `DeclarationCorrection`, `CertificateVerification`
  - Actions: committee uphold / modify / reject
- **Customer portal (mocked customer surface):**
  - Data consumed: own `[Case]` status, `IssuedArtifact`, info-requests
  - Actions: submit request, pay fee (mock), respond to info-request, view decision, file objection
- **Audit trail view:**
  - Data consumed: immutable `[AuditEvent]` for a case from TOL7
  - Actions: none (read/export)

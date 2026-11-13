# Agent Register

All agents are **build** at Full tier. IDs are stable (`AGN1`–`AGN6`, plus the Deterministic Rule Engine). Field names are canonical and reused across `mcp-tool-register.md` and `data-contracts.md`. Where the blueprint did not give an explicit I/O schema, fields are marked `[synthesized]`.

| ID | Name | Atomic steps | Type | Zone | Status |
|----|------|--------------|------|------|--------|
| AGN1 | Intake & Routing | ATS1, ATS2 | Deterministic + AI | Green | build |
| AGN2 | Content Extraction | ATS3 | AI/LLM | Green | build |
| AGN3 | Rules & Origin Determination | ATS5, ATS6, ATS7 | AI/LLM | Amber | build |
| AGN4 | Ruling / Correspondence Drafting | ATS8, ATS10 | AI/LLM | Amber | build |
| AGN5 | Decision & Issuance | ATS11, ATS12 | Deterministic + AI | Amber | build |
| AGN6 | Dispute Adjudication | ATS13, ATS14 | AI/LLM | Red | build |
| — | Deterministic Rule Engine | ATS4, ATS9 | Deterministic | Green/Amber | build |

> Step-to-agent mapping follows the blueprint's Phase 1 assignment (AGN3 owns ATS5/ATS6/ATS7). The Deterministic Rule Engine carries the hard validation and legal-constraint checks that must be exact and auditable.

---

## AGN1 — Intake & Routing

**Responsibility.** Receives a new request or inbound trigger (advance-ruling request, agreement update letter, inquiry, Ministry sampling letter, dispute/objection), registers the case, determines its type, and routes it to the correct downstream workflow. For advance-ruling requests it first confirms fee payment and runs the completeness/eligibility gate before routing. Classifies inquiries (internal vs external) and determines whether a Classification-Section cross-check is needed.

**Inputs:**
- `trigger_type` (enum(advance_ruling, agreement_update, inquiry_internal, inquiry_external, ministry_sampling, dispute, objection)) — source of the case
- `raw_payload` (dict) — submitted request/letter content
- `customer_ref` (Optional[str]) — customer identifier when customer-originated
- `fee_payment_status` (enum(none, paid)) `[synthesized]` — advance-ruling fee state
- `received_at` (datetime) — timestamp used for legal-time-limit calculations downstream

**Outputs:**
- `case` (Case) — registered case with assigned `case_id`, `case_type`, `status`
- `routing_target` (enum(extraction, rule_engine, drafting, adjudication, terminate)) — next stage
- `completeness_result` (ValidationResult) — outcome of the eligibility/completeness gate (advance-ruling path)
- `requires_classification_check` (bool) `[synthesized]`

**Downstream notes.** Hands validated advance-ruling cases to AGN2/Deterministic Rule Engine; routes update letters to the update workflow; routes disputes/objections to AGN6. A failed completeness gate routes to AGN4 for a reasoned rejection draft.

---

## AGN2 — Content Extraction

**Responsibility.** Extracts structured fields from the request payload and attachments (commodity description, HS/tariff candidate, declared origin, agreement invoked, supporting documents, certificate data). Multilingual (Arabic/English). Produces the normalized case content the Rules & Origin agent reasons over.

**Inputs:**
- `case` (Case) — from AGN1
- `raw_documents` ([Document]) — attachments and request body
- `source_language` (enum(ar, en, mixed)) `[synthesized]`

**Outputs:**
- `extracted_content` (ExtractedContent) — structured fields (commodity, hs_candidate, declared_origin, agreement_ref, supporting_docs)
- `extraction_confidence` ({field_name: float}) — per-field confidence
- `extraction_flags` ([str]) — missing/low-confidence field markers

**Downstream notes.** Low-confidence or missing mandatory fields raise the "request additional information" branch (AGN5/AGN1 info-request). Full-tier accuracy target applies to extraction.

---

## AGN3 — Rules & Origin Determination

**Responsibility.** The analytical core. Studies the case against the acceptance conditions and the rules of origin, determines the commodity's origin, and produces a recommendation (accept, reject-with-reasons, request-additional-information, suspend). Applies the documented origin criteria — wholly-obtained, substantial transformation, regional value content, tariff-shift — per the invoked agreement, and reconciles with the Classification Section cross-check.

**Inputs:**
- `case` (Case)
- `extracted_content` (ExtractedContent) — from AGN2
- `classification_result` (ClassificationResult) — tariff cross-check (TOL via قسم التصنيف والتقييم mock)
- `origin_rule_set` (OriginRuleSet) — per-agreement rules of origin (BR-06)
- `prior_rulings` ([AdvanceRuling]) `[synthesized]` — precedent lookup

**Outputs:**
- `origin_determination` (OriginDetermination) — determined origin, criterion applied, threshold used, rationale
- `recommendation` (enum(accept, reject, request_info, suspend)) — case outcome
- `determination_basis` ([str]) — enumerated reasons tied to specific rules
- `confidence` (float)

**Downstream notes.** Amber zone — output is a recommendation subject to HITL review before AGN4 drafts and AGN5 issues. Full-tier accuracy target applies; evaluation harness scores determination correctness against a labelled set.

---

## AGN4 — Ruling / Correspondence Drafting

**Responsibility.** Drafts the formal written artifact for the case: the advance-ruling decision, the official inquiry response, the update circular (تعميم) draft, the Ministry-of-Economy letter, the rejection-with-reasons notice, or the information-request. Bilingual drafting. Produces reviewable drafts that carry the determination rationale and binding-status / validity-period language for rulings.

**Inputs:**
- `case` (Case)
- `origin_determination` (Optional[OriginDetermination]) — for ruling drafts
- `draft_type` (enum(advance_ruling, inquiry_response, update_circular, ministry_letter, rejection, info_request))
- `template_context` (dict) `[synthesized]` — validity period, fee, legal references

**Outputs:**
- `draft_document` (DraftDocument) — bilingual draft with content, rationale, metadata
- `draft_status` (enum(pending_review)) — enters the review state machine

**Downstream notes.** Amber — every draft goes through one or more review tiers (Section Head, Legal Affairs, Policy & Governance Director depending on draft type) before approval. Review loop states are in `data-contracts.md`.

---

## AGN5 — Decision & Issuance

**Responsibility.** Applies the authority/approval matrix, records the approval decision, issues the finalized artifact, triggers e-signature where required, publishes the advance ruling to the customs website, sends notifications, and closes the case. Also handles fee-validation and completeness-rejection issuance, suspension, and the information-request issuance.

**Inputs:**
- `case` (Case)
- `draft_document` (DraftDocument) — approved draft
- `approver_role` (enum(section_employee, section_head, policy_governance_director, legal_affairs)) — resolved from the authority matrix (BR-11)
- `approval_decision` (enum(approve, modify, reject)) — reviewer action

**Outputs:**
- `issued_artifact` (IssuedArtifact) — final ruling/circular/letter with issuance metadata, validity window, binding status
- `publication_status` (enum(none, published)) — website publication for advance rulings
- `notifications_sent` ([Notification])
- `case_final_state` (enum(issued, rejected, suspended, closed))

**Downstream notes.** Amber — issuance of a binding ruling and financially/legally consequential decisions require the matrix-resolved approver. Publication and e-sign are mocked but state-tracked.

---

## AGN6 — Dispute Adjudication

**Responsibility.** Adjudicates disputes over the agreements/origin field of a customs declaration at both the customs-centre and department levels, and handles objections escalated to the Technical Committee. Studies the objection, coordinates with Customs Audit / Classification & Valuation / Origin as needed, may raise a Ministry-of-Economy certificate-authenticity check, and produces a modify-or-uphold recommendation. Enforces the legal-time-limit check on Technical-Committee objections.

**Inputs:**
- `dispute_case` (DisputeCase) — objection to a declaration-correction decision or advance ruling
- `objection_filed_at` (datetime) — for legal-time-limit calculation (BR-14)
- `declaration_ref` (str) — affected customs declaration
- `supporting_evidence` ([Document]) `[synthesized]` — seizure record, goods docs, declaration, inspection notes, grievance request
- `certificate_verification` (Optional[CertificateVerification]) — Ministry-of-Economy result when authenticity is challenged

**Outputs:**
- `time_limit_result` (enum(in_time, out_of_time)) — legal admissibility
- `adjudication_decision` (enum(uphold, modify, reject)) — Technical Committee outcome
- `correction` (Optional[DeclarationCorrection]) — fields corrected (preferential-treatment field, origin field only)
- `adjudication_rationale` ([str])

**Downstream notes.** **Red zone** — the highest-constraint path. Out-of-time objections are auto-rejected (BR-14) and the flow terminates. A modify outcome routes back to the issuing process (re-issue corrected decision). Every step and the committee recommendation must be visible and audited.

---

## Deterministic Rule Engine

**Responsibility.** Executes the exact, auditable, non-LLM checks: advance-ruling fee/completeness/eligibility validation (single commodity, no open declaration, not under review/appeal), legal-constraint checks, the authority/approval-matrix resolution, and the objection legal-time-limit computation. These must be deterministic and 100%-reproducible for audit.

**Inputs:**
- `case` (Case)
- `rule_set_id` (enum(completeness, legal_constraints, authority_matrix, time_limit)) — which rule set to run
- `rule_params` (dict) `[synthesized]` — configurable thresholds (fee amount, objection window, validity period)

**Outputs:**
- `validation_result` (ValidationResult) — per-rule pass/fail with severity
- `resolved_authority` (Optional[str]) — approver role from the matrix
- `rule_outcomes` ([RuleOutcome]) — enumerated outcomes for the audit trail

**Downstream notes.** Green/Amber. Carries the hard business rules in `business-rules.md` (BR-02, BR-09, BR-11, BR-14). Deterministic steps must meet the **≥99.9% step-level integrity** target. `source-stated`

# Business Rules

Explicit rule sets were found in the blueprint. They are extracted below as contracts. Numeric thresholds not quantified in the source are marked `[inferred]` and held as configurable parameters; the coding agent must request authoritative values from the stakeholder before production use (`open-question`). Rule IDs are stable (`BR-nn`) and referenced from `agent-register.md`.

## BR-02 — Advance-ruling completeness & eligibility gate

Enforced by the Deterministic Rule Engine (AGN1 intake path). All must pass for the request to be accepted; any failure routes to reasoned rejection.

| ID | Rule | Inputs | Pass condition | Failure severity |
|----|------|--------|----------------|------------------|
| BR-02.1 | Fee paid | `fee_payment_status` | `== paid` | blocking (reject) |
| BR-02.2 | Single commodity | `extracted_content.commodity` | request covers exactly one commodity type | blocking (reject) |
| BR-02.3 | No open declaration | `declaration_ref` lookup (TOL2) | no customs declaration already registered for the goods at the centre | blocking (reject) |
| BR-02.4 | Not under review/appeal | goods status | goods not subject to a verification, review, or appeal before any agency/court | blocking (reject) |
| BR-02.5 | Required info present | `extraction_flags` | no missing mandatory field | request-info (suspend) |

**Enforcement note.** BR-02.5 triggers the information-request / suspend branch rather than outright rejection.

## BR-06 — Rules-of-origin determination criteria

Enforced by AGN3. The determination selects and applies the agreement-appropriate criterion; the applied criterion and threshold are recorded in `origin_determination.determination_basis`.

| Criterion | Applies when | Threshold / test | Source state |
|-----------|-------------|------------------|--------------|
| Wholly obtained | goods entirely produced in one country | no foreign materials | source-stated |
| Substantial transformation | goods incorporate foreign materials | tariff-shift or qualifying process per agreement | source-stated |
| Regional value content (RVC) | agreement uses value-content rule | value content ≥ `rvc_threshold_pct` | threshold `[inferred]` — per-agreement config |
| Tariff-shift (CTC) | agreement uses change-in-classification rule | HS heading/subheading change per agreement rule | source-stated |
| De-minimis tolerance | small non-originating content | non-originating ≤ `de_minimis_pct` | threshold `[inferred]` — per-agreement config |

`[NEEDS CLARIFICATION]` marker 2 in `scope-decisions.md` covers the unquantified thresholds. Model as a per-agreement rule table; seed with clearly-marked placeholder values.

## BR-09 — Legal / regulatory constraint checks

Enforced by the Deterministic Rule Engine. Compliance with GCC Customs Law, WCO, WTO, Kyoto (Revised), Trade Facilitation Agreement, and SAFE Framework where the case invokes them. Determinations and rulings that would conflict with a binding legal constraint are blocked and flagged for the relevant reviewer tier.

| ID | Rule | Pass condition | Severity |
|----|------|----------------|----------|
| BR-09.1 | Binding-advice conformance | ruling conforms to WCO / TFA advance-ruling guidance | blocking |
| BR-09.2 | Agreement validity | invoked agreement is active (not suspended per latest FCA update) | blocking |
| BR-09.3 | Dual-field correction scope | dispute corrections touch only preferential-treatment field + origin field | blocking |

## BR-11 — Authority / approval matrix

Enforced by the Deterministic Rule Engine (AGN5 issuance). Resolves which role must approve based on artifact type. Four-tier model; each tier independently enforceable.

| Artifact / decision | Required approver |
|---------------------|-------------------|
| Advance ruling (issue) | رئيس قسم الاتفاقيات الدولية والمنشأ (Section Head) |
| Inquiry response | Section Head (after employee draft) |
| Agreement update circular (تعميم) | Legal Affairs review → مدير إدارة السياسات والحوكمة (Policy & Governance Director) |
| Ministry-of-Economy letter | Section Head → Policy & Governance Director |
| Certificate sampling letter | Section Head → Policy & Governance Director (e-sign) |
| Dispute correction (centre/department) | رئيس قسم العمليات (centre) / Section Head (department) |
| Objection outcome | اللجنة الفنية — صاحب صلاحية اعتماد توصيات اللجنة الفنية |

## BR-14 — Objection legal-time-limit check

Enforced by the Deterministic Rule Engine (AGN6, Technical-Committee branch).

| ID | Rule | Logic | Outcome |
|----|------|-------|---------|
| BR-14.1 | Admissibility window | `objection_filed_at − notification_at ≤ objection_window_days` | in_time → proceed to committee; out_of_time → auto-reject + terminate |

`objection_window_days` and the start event are **not quantified in source** — `[inferred]` configurable parameter. See `[NEEDS CLARIFICATION]` marker 1 in `scope-decisions.md`. The computed result and the window value used must be written to the audit trail (TOL7).

## BR-04 — Extraction confidence gate

Enforced around AGN2. Low per-field confidence or a missing mandatory field raises the request-additional-information branch rather than proceeding to determination.

| ID | Rule | Condition | Outcome |
|----|------|-----------|---------|
| BR-04.1 | Confidence floor | any mandatory `extraction_confidence[field] < conf_floor` | request-info / suspend |

`conf_floor` is `[inferred]` — configurable (default placeholder, not statistically baselined; see `open-question` on KPI data).

## Reliability constraints (Full tier)

- Deterministic steps (ATS4, ATS9, matrix/time-limit): **≥99.9% step-level integrity**. `source-stated`
- AI steps (AGN2 extraction, AGN3 determination, AGN4 drafting): blueprint accuracy targets preserved as build constraints, measured by the Full-tier evaluation harness against labelled gold sets. Exact target percentages follow the blueprint's Phase 4 criteria. `source-stated`

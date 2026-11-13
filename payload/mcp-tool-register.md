# MCP Tool Register

All tools build against **mocked** backends (user decision: mock all external systems). The mock layer conforms to each tool's I/O contract so a later swap to real MCP Gateway connectors requires no agent change — that boundary is the replacement note on each tool. Entity shapes referenced here are defined once in `data-contracts.md`.

| ID | Name | Mode | Used by |
|----|------|------|---------|
| TOL1 | Case & Request Store | mock/build | AGN1, AGN5, AGN6 |
| TOL2 | Customs Declaration Lookup | mock/build | AGN3, AGN6 |
| TOL3 | Origin Rules & Agreements Knowledge | mock/build | AGN3, AGN2 |
| TOL4 | Tariff Classification Cross-Check | mock/build | AGN3 |
| TOL5 | Document Drafting & Template | mock/build | AGN4 |
| TOL6 | Notification & Publication | mock/build | AGN5 |
| TOL7 | Audit & Evidence Recorder | mock/build | all agents |
| TOL8 | Ministry-of-Economy Verification | mock/build | AGN6 |

---

## TOL1 — Case & Request Store

**Purpose.** Persist and query cases, requests, rulings, circulars, and their state across the منظومة العمليات المؤسسية المتكاملة system of record.

**Inputs:**
- `operation` (enum(create, read, update, query)) `[synthesized]`
- `case_id` (Optional[str])
- `payload` (dict) — case/request fields on create/update
- `query` (Optional[dict]) — filters on query

**Outputs:**
- `case` (Case) — on read/create/update
- `results` ([Case]) — on query
- `status` (enum(ok, not_found, error))

**Side effects.** Writes case state. **Replacement note:** back with SQLite fixtures; real impl = SoR connector via MCP Gateway.

---

## TOL2 — Customs Declaration Lookup

**Purpose.** Retrieve customs declarations (and their agreements/origin fields) for origin determination and dispute adjudication.

**Inputs:**
- `declaration_ref` (Optional[str])
- `period` (Optional[{from: date, to: date}]) — for sampling / batch retrieval
- `filters` (Optional[dict]) `[synthesized]`

**Outputs:**
- `declarations` ([CustomsDeclaration]) — header + agreements field + origin field + line items
- `status` (enum(ok, not_found, error))

**Side effects.** Read-only. **Replacement note:** mock returns seeded declarations; real impl = SoR query.

---

## TOL3 — Origin Rules & Agreements Knowledge

**Purpose.** Retrieve the applicable rules of origin, agreement terms, and prior answers/rulings used by determination and extraction.

**Inputs:**
- `agreement_ref` (Optional[str])
- `commodity_or_hs` (Optional[str])
- `query_text` (Optional[str]) — semantic lookup of prior answers `[synthesized]`

**Outputs:**
- `origin_rule_set` (OriginRuleSet) — criteria + thresholds (BR-06)
- `agreement_terms` ([str])
- `prior_answers` ([PriorAnswer]) `[synthesized]`
- `status` (enum(ok, not_found, error))

**Side effects.** Read-only. **Replacement note:** mock from seeded rule/agreement knowledge; real impl = SoR + knowledge base.

---

## TOL4 — Tariff Classification Cross-Check

**Purpose.** Obtain the classification decision from قسم التصنيف والتقييم for a commodity during origin determination and update processing.

**Inputs:**
- `commodity_description` (str)
- `hs_candidate` (Optional[str])

**Outputs:**
- `classification_result` (ClassificationResult) — determined HS/tariff item + rationale
- `status` (enum(ok, pending, error))

**Side effects.** Read-only cross-section call. **Replacement note:** mock keyed by commodity/HS; real impl = Classification Section service.

---

## TOL5 — Document Drafting & Template

**Purpose.** Render bilingual (AR/EN) draft artifacts (rulings, circulars, letters, responses) from determination output and templates.

**Inputs:**
- `draft_type` (enum(advance_ruling, inquiry_response, update_circular, ministry_letter, rejection, info_request))
- `content_context` (dict) — determination, validity, fee, legal refs
- `language` (enum(ar, en, bilingual))

**Outputs:**
- `draft_document` (DraftDocument)
- `status` (enum(ok, error))

**Side effects.** None (produces draft only). **Replacement note:** mock renders from templates; real impl = document service.

---

## TOL6 — Notification & Publication

**Purpose.** Send electronic notifications and publish advance rulings to the customs website.

**Inputs:**
- `notification_type` (enum(created, info_requested, approved, rejected, issued, published, objection))
- `recipient_role` (str)
- `case_id` (str)
- `publish` (bool) — website publication flag

**Outputs:**
- `notification` (Notification)
- `publication_status` (enum(none, published))
- `status` (enum(ok, error))

**Side effects.** Emits notifications; marks publication. **Replacement note:** mock records emissions; real impl = notification + web-publish services.

---

## TOL7 — Audit & Evidence Recorder

**Purpose.** Append immutable audit entries (step, agent, decision, reviewer, state transition) and attach evidence (certificate images, verification responses).

**Inputs:**
- `case_id` (str)
- `event` (AuditEvent) — step, actor, action, before/after state, rationale
- `evidence` (Optional[[Document]])

**Outputs:**
- `audit_entry_id` (str)
- `status` (enum(ok, error))

**Side effects.** Append-only write — entries are immutable. **Replacement note:** mock = append-only SQLite table; real impl = audit store. Used by every agent and HITL gate.

---

## TOL8 — Ministry-of-Economy Verification

**Purpose.** Submit origin-certificate authenticity checks to وزارة الاقتصاد and receive the export-country verification result; also deliver certificate sampling letters.

**Inputs:**
- `certificate_images` ([Document])
- `certificate_ref` (str)
- `request_type` (enum(authenticity_check, sampling_delivery))

**Outputs:**
- `verification` (CertificateVerification) — status(pending, valid, invalid) + response detail
- `status` (enum(ok, pending, error))

**Side effects.** Initiates an async external exchange. **Replacement note:** mock returns pending then a seeded valid/invalid response; real impl = Ministry channel. No fixed timeout — case holds in async pending.

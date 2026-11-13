# Integration Decisions

All external systems and MCP tools are in scope at Full tier. All external systems are **mocked** per user decision ("mock all external systems"). The replacement boundary is the MCP Gateway connector layer — mocks conform to the same tool I/O contracts so a later swap to real connectors needs no agent changes.

## External systems

| System | Mode | Role in workflow | Mock strategy |
|--------|------|------------------|---------------|
| منظومة العمليات المؤسسية المتكاملة (Integrated Enterprise Operations — system of record) | mock | Primary SoR: cases, requests, customs declarations, rulings, circulars, audit records, notifications | SQLite-backed fixture store + seeded JSON; exposes CRUD/query matching TOL I/O |
| المنصة الرقمية للخدمات الجمركية (Digital Customs Services Platform) | mock | Customer-facing channel: request submission, fee payment, info-request responses, decision viewing, objection filing | Hand-coded stub responses + in-app customer screens drive the same fixtures |
| الهيئة الاتحادية للجمارك (Federal Customs Authority) | mock | Inbound update letters carrying the agreement/tariff update list | Seeded update-letter fixtures (JSON) |
| قسم التصنيف والتقييم (Classification & Valuation Section) | mock | Tariff-item cross-check / classification decision during update processing and origin determination | Stub returning classification-decision fixtures keyed by HS/commodity |
| وزارة الاقتصاد (Ministry of Economy) | mock | Origin-certificate authenticity verification; receives sampling letters | Mocked async exchange: pending → response fixture (valid / invalid) |

### Environment and credential assumptions

- No real credentials required — all access is through mock connectors. `user-decided`
- Secrets management: environment variables with a `.env.example`. `inferred` MVP default (applies even at Full tier because integrations are mocked).
- Real auth (OAuth 2.0 / service accounts for the SoR and customer platform) is deferred; the mock layer records the intended auth pattern as a note for the later swap. `deferred`

## MCP tools

All TOL1–TOL8 build against mocked backends. Modes, I/O, side effects, and replacement notes are in `mcp-tool-register.md`. Summary of backend strategy:

| Tool | Mode | Backend strategy |
|------|------|------------------|
| TOL1–TOL7 | mock/build | Build the tool interface; back it with fixture data conforming to the documented I/O so the determination, drafting, and issuance paths run end to end |
| TOL8 | mock/build | In scope (AGN6 dispute adjudication is in scope at Full tier); backed by dispute/objection fixtures |

## Orphaned-dependency handling

Because every producing agent and step is in scope, no in-scope input lacks an in-scope producer. The only seeded inputs are the external triggers that originate outside the department:

- **Federal Customs Authority update letters** — seed fixtures (the FCA is external). Recorded in `data-contracts.md` (AgreementUpdateLetter fixture).
- **Customer advance-ruling requests, objections, info-request responses** — seed fixtures + customer screens (the customer is external). Recorded in `data-contracts.md`.
- **Ministry-of-Economy verification responses** — seed fixtures (the Ministry is external). Recorded in `data-contracts.md`.

## Failure / unavailability expectations

- Mock connectors must support an injectable error mode (system unavailable, timeout, malformed payload) so the orchestrator's error-handling and the "data not current / inaccurate inputs" operational risks can be demonstrated. `inferred` — supports the Full-tier visibility goal and the blueprint's operational-risk register.
- Ministry-of-Economy verification has no fixed timeout; the case holds in an async pending state until a response fixture arrives. `inferred`

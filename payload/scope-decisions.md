# Scope Decisions

## Build tier and pattern

- **Build tier:** Full — `user-decided`. The user asked to show every atomic thinking step, every HITL gate, and every agent at work. Nothing is descoped.
- **Scope pattern:** Full-coverage (all six workflows, all agents, all atomic steps). This is not one of the thinned MVP patterns — it is the complete process surface.
- **Rationale:** the build is a demonstration-grade, full-fidelity execution of the قسم الاتفاقيات الدولية والمنشأ operation, so transparency of reasoning and the approval chain is the primary outcome.

## Agents in scope

All agents BUILD. `user-decided`

| ID | Agent | Status |
|----|-------|--------|
| AGN1 | Intake & Routing | build |
| AGN2 | Content Extraction | build |
| AGN3 | Rules & Origin Determination | build |
| AGN4 | Ruling / Correspondence Drafting | build |
| AGN5 | Decision & Issuance | build |
| AGN6 | Dispute Adjudication (RED zone) | build |
| — | Deterministic Rule Engine | build |

Full agent responsibilities, I/O, and zones are in `agent-register.md`.

## MCP tools in scope

All TOL1–TOL8 BUILD against mocked backends. `user-decided` (follows "mock all external systems"). Modes and I/O are in `mcp-tool-register.md`.

## External systems

All external systems **mock**. `user-decided`

| System | Mode |
|--------|------|
| منظومة العمليات المؤسسية المتكاملة (Integrated Enterprise Operations / system of record) | mock |
| المنصة الرقمية للخدمات الجمركية (Digital Customs Services Platform) | mock |
| الهيئة الاتحادية للجمارك (Federal Customs Authority — update-letter feed) | mock |
| قسم التصنيف والتقييم (Classification & Valuation Section — tariff cross-check) | mock |
| وزارة الاقتصاد (Ministry of Economy — certificate verification) | mock |

Fixture/source expectations are in `integration-decisions.md` and shapes in `data-contracts.md`.

## UX surface

- **Primary surface:** web app, **bilingual Arabic + English** (RTL for AR, LTR for EN). `user-decided`
- **HITL surface:** in-app review screens with role-scoped queues for each reviewer tier (Section employee, Section Head, Policy & Governance Director, Legal Affairs, Technical Committee), plus a customer-facing surface for request submission, fee payment, information-request responses, decision viewing, and objection filing. `source-stated` + `inferred` (surface rendering)
- **Visibility requirement:** because the user wants every atomic step and agent visible, the UI must expose a step/trace view per case (agent, step, input, output, decision, state) in addition to the operational screens. `user-decided`
- Per-screen data contracts are in `data-contracts.md`.

## Repository topology

- **Decision:** frontend + backend. `user-decided`
- Written to `repos.yaml` as two greenfield application repositories (`topology: multi`).

## Tech-stack decisions

- Pro-code framework: Anthropic SDK direct. `user-decided` (sensible defaults)
- Working-file storage: local filesystem + SQLite. `user-decided` (sensible defaults)
- Test framework: pytest. `user-decided` (sensible defaults)
- Language/runtime: Python 3.11 backend. `inferred` default.
- Front-end design system: Carbon Design System `[inferred]` for an IBM/enterprise bilingual look; the coding agent may substitute an equivalent RTL-capable system.
- Reliability targets: preserved as build constraints at Full tier (evaluation harness in scope). `source-stated`

## Assumptions

- Baseline volume and KPI targets are **not stated in source documents**; cycle-time and accuracy baselines are `open-question` and must be confirmed with stakeholders before any statistical acceptance gate is finalised. The functional acceptance intent in `implementation-brief.md` does not depend on them.
- The Technical Committee legal time limit for objections is counted from customer notification / certain knowledge of the decision; the exact number of days is **not quantified in source** — `open-question`, default to a configurable parameter. `[inferred]`
- Advance-ruling fee amount and validity-period length are **not quantified in source** — configurable parameters. `[inferred]`
- Ministry-of-Economy response SLA for certificate verification is **not stated** — modelled as an asynchronous pending state with no fixed timeout. `[inferred]`

## `[NEEDS CLARIFICATION]` markers (max 3)

Because all agents and steps are in scope, the mid-stream-cut and orphaned-dependency patterns do not fire. The remaining ambiguities that affect the build:

1. `[NEEDS CLARIFICATION: objection legal time limit (ATS14 branch) is not quantified in the source — number of days and the start event (notification vs. certain knowledge).]`
   **Default resolution:** implement as a configurable `objection_window_days` parameter with a documented default placeholder, counted from the notification timestamp; record the computed in-time/out-of-time result in the audit trail. Enforcement logic is in `business-rules.md` (BR-14).
2. `[NEEDS CLARIFICATION: rules-of-origin criteria thresholds (regional value content percentage, de-minimis) are agreement-specific and not enumerated in the source.]`
   **Default resolution:** model the criteria as a per-agreement rule table (`business-rules.md` BR-06) with threshold values held as configurable data keyed by agreement; seed fixtures with representative but clearly-marked placeholder thresholds. Determinations record which criterion and threshold were applied.
3. `[NEEDS CLARIFICATION: advance-ruling validity-period length and fee amount are not quantified in the source.]`
   **Default resolution:** both are configurable parameters surfaced in the mocked fee/validity config; the ruling record stores the resolved values. Recorded in `data-contracts.md` (AdvanceRuling entity).

## Deferred scope

- **Production system-of-record integration** — all external systems are mocked; real MCP Gateway connectors are deferred. `deferred`
- **Real e-signature and real customer-platform authentication** — the e-sign step and customer identity are simulated. `deferred`
- **Real Ministry-of-Economy correspondence channel** — modelled as a mocked async exchange. `deferred`
- **Statistical KPI baselining** — pending stakeholder volume/KPI data. `deferred`

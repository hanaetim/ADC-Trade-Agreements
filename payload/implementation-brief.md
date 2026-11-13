# Implementation Brief — International Agreements & Origin Management Application

**Client:** الإدارة العامة لجمارك أبوظبي (Abu Dhabi Customs) — قسم الاتفاقيات الدولية والمنشأ (International Agreements & Rules of Origin Section)
**Process domain:** Customs and Trade Regulatory Compliance
**Build date basis:** 2026-11-13

## Objective

Build an agentic application that executes the full International Agreements & Origin (الاتفاقيات والمنشأ) operation end to end: advance origin-ruling intake and determination, international/FTA/bilateral agreement update processing, internal and external inquiry handling, Kyoto/TFA/SAFE compliance study orchestration, origin-certificate sampling for the Ministry of Economy (وزارة الاقتصاد), and dispute adjudication across the customs centre and the department. The application must make **every atomic thinking step, every human-in-the-loop (HITL) gate, and every agent visible and demonstrable** — this is an explicit Full-tier build goal so stakeholders can observe the reasoning, routing, and approval chain at work.

## Target users

- **قسم الاتفاقيات الدولية والمنشأ staff (Section employees / الموظف المعني):** create/triage requests, review agent output, record information requests, draft responses and rulings. `source-stated`
- **رئيس قسم الاتفاقيات الدولية والمنشأ (Section Head):** reviews and approves rulings, update circulars, Ministry letters, and dispute resolutions. `source-stated`
- **مدير إدارة السياسات والحوكمة (Policy & Governance Director):** approves update circulars and Ministry-of-Economy correspondence. `source-stated`
- **اللجنة الفنية (Technical Committee) — مقرر اللجنة + صاحب صلاحية اعتماد التوصيات:** adjudicates objections to section decisions. `source-stated`
- **المتعامل (Customer/Trader):** submits advance-ruling requests, pays fees, responds to information requests, views decisions, files objections — via the digital customs services platform surface. `source-stated`
- **Operators:** monitor the orchestration, HITL queues, and audit trail. `inferred`

## Primary workflows (all in scope at Full tier)

1. **Advance origin ruling** — request intake → fee/completeness/eligibility validation → case study against rules of origin → ruling drafting → review/approve → issue → publish → customer objection branch. (ATS1–ATS8 thread + issuance) `source-stated`
2. **Agreement/tariff update processing** — Federal Customs Authority (الهيئة الاتحادية للجمارك) update letter → update request → classification cross-check → multi-level review (Section Head, Legal Affairs, Policy & Governance Director) → circular → system update. `source-stated`
3. **Inquiry handling (internal + external)** — classify, retrieve relevant agreement/origin rules & prior answers, request additional info if needed, draft official response, close. `source-stated`
4. **Quarterly compliance study** — Kyoto / Trade Facilitation / SAFE Framework — committee invite → compliance/non-compliance report → multi-level approval → recommendations loop. `source-stated`
5. **Origin-certificate sampling for Ministry of Economy** — ministry letter → retrieve declarations in period → random sampling → sample letter with attached certificate images → review/approve/e-sign → send. `source-stated`
6. **Dispute adjudication** — customs-centre dispute (correct declaration agreements/origin field) → department-level adjudication → Technical Committee objection with legal-time-limit check → uphold/modify decision. `source-stated`

## Selected build scope and acceptance intent

- **Build tier:** Full — `user-decided`. Every atomic step (ATS1–ATS14), every agent (AGN1–AGN6 + Deterministic Rule Engine), and every HITL gate is in scope.
- **Acceptance intent (functional + reliability, Full tier):**
  - The application runs each of the six workflows end to end on mocked systems of record, with each atomic step surfaced and inspectable.
  - Every HITL gate (review / approve / modify / reject / objection) blocks and routes exactly as specified, with the reviewer role enforced.
  - The rules-of-origin determination applies the documented criteria (wholly-obtained, substantial transformation, regional value content, tariff-shift) and records the basis of each determination.
  - The legal-time-limit check on objections rejects out-of-time objections and routes in-time objections to the Technical Committee.
  - Deterministic steps meet the blueprint's reliability target of **≥99.9% step-level integrity** `source-stated`; AI determination/extraction steps meet the blueprint's accuracy targets with an evaluation harness in scope at Full tier.
  - A complete, immutable audit trail records every step, decision, reviewer, and state transition.
  - The UI operates in **Arabic and English** (bilingual, RTL + LTR) — `user-decided`.

## Key constraints and compliance posture

- **Bilingual, RTL-aware UI** (Arabic primary, English secondary) is a hard build constraint. `user-decided`
- **Four reviewer tiers** must be independently enforceable: Section employee → Section Head → Policy & Governance Director / Legal Affairs → Technical Committee. `source-stated`
- **Legal-time-limit enforcement** on objections is a hard rule — an out-of-time objection must be auto-rejected and the flow terminated. `source-stated`
- **Advance rulings are binding on customs for a defined validity period** and must conform to WCO / Trade Facilitation Agreement advance-ruling guidance; the ruling record must capture validity window and binding status. `source-stated`
- **Dual-field correction scope:** dispute corrections act only on the preferential-treatment field and the goods-origin field of the customs declaration. `source-stated`
- **Audit/evidence:** every decision requires a recorded rationale; Ministry-of-Economy certificate-authenticity checks require attaching certificate images and the export-country verification response. `source-stated`
- **Reliability targets preserved as build constraints** because Full tier includes the evaluation harness (see `business-rules.md` and `data-contracts.md`).

## Resolved tech stack (provenance-tagged)

| Item | Choice | Provenance |
|------|--------|------------|
| Platform | ICA + AI Core (MCP / LLM / A2A Gateways) | Project context (EAEF Platform Overview) |
| System-of-record access | منظومة العمليات المؤسسية المتكاملة via MCP Gateway connectors — **mocked** for this build | Blueprint + Decided by user |
| Models | multilingual extraction LLM (AGN2); large reasoning LLM (AGN3, AGN6); multilingual generation LLM (AGN4) | Blueprint |
| Orchestration | supervisor topology over a deterministic backbone | Blueprint |
| Observability | Control Tower (structured telemetry); structured step-trace logging at minimum | Project context (EAEF Platform Overview) |
| Language & runtime | Python 3.11 | Default for MVP |
| Agent framework | Anthropic SDK direct | Decided by user (sensible defaults) |
| Working-file storage | local filesystem + SQLite | Decided by user (sensible defaults) |
| Test framework | pytest | Decided by user (sensible defaults) |
| Front-end | web app, bilingual AR/EN (RTL + LTR); Carbon Design System `[inferred]` for IBM/enterprise look | Decided by user + inferred |
| Repository topology | frontend + backend | Decided by user |

Downstream method and coding agent own all remaining architecture: module layout, component structure, state management, build order, and test strategy.

# README — Implementation Payload

## What this is

This folder is the **method-neutral implementation payload** generated from the EAEF Layer 2 process blueprint for **Customs and Trade Regulatory Compliance — International Agreements & Origin Management** (الإدارة العامة لجمارك أبوظبي / Abu Dhabi Customs, قسم الاتفاقيات الدولية والمنشأ).

It is complementary implementation source material — build-facing decisions, registers, rules, and contracts layered on top of the blueprint. It is **not** a rewritten blueprint, **not** final Spec Kit / OpenSpec / BMAD / native method artifacts, and **not** the Enterprise App Kit zip.

## Files

- `repos.yaml` — Enterprise App Kit repository topology (frontend + backend, greenfield).
- `implementation-brief.md` — objective, users, workflows, selected scope, acceptance intent, constraints, resolved stack.
- `scope-decisions.md` — Full build tier, all agents/tools/systems in scope, UX surface, assumptions, `[NEEDS CLARIFICATION]` markers, deferred scope.
- `integration-decisions.md` — external systems and MCP tools (all mocked), fixture/source expectations, failure modes.
- `agent-register.md` — AGN1–AGN6 + Deterministic Rule Engine with status, responsibilities, I/O, zones, handoffs.
- `mcp-tool-register.md` — TOL1–TOL8 with modes, I/O, side effects, replacement boundaries.
- `business-rules.md` — completeness/eligibility, rules-of-origin criteria, legal constraints, authority matrix, objection time-limit, confidence gate, reliability targets.
- `data-contracts.md` — entities, fixture shapes, case + review state models, bilingual UI data contracts, shared enums.

## How packaging works

Process Studio packages this payload under `ent-app-kit/payload/` with the Enterprise App Kit engine. Packaging **injects the authoritative blueprint snapshot separately** as `payload/blueprint/blueprint.md` and `payload/blueprint/blueprint-metadata.json` — this generator does not emit a blueprint copy.

The engine adds shared delivery machinery (`setup.sh`, scripts, `kit-*` agent skills, JSON schemas). The user unpacks the kit, runs `ent-app-kit/setup.sh`, picks a coding agent (Claude Code / Codex CLI / IBM Bob) and an SDD method (Spec Kit / OpenSpec), starts the agent from the workspace root, and says `Build the app kit.`

## What downstream owns

- The selected **App Kit method** creates method-native planning artifacts (Spec Kit feature dirs, OpenSpec proposals/spec deltas/tasks, or a native work plan) from this source.
- The **coding agent is the architect**: module layout, component structure, state management, build order, test strategy, framework conventions, and the bilingual RTL/LTR front-end implementation are all decided downstream. This payload gives contracts and decisions, not code or file layout.
- Dedicated downstream workflows may create knowledge-synthesis and navigation artifacts from the payload plus the injected blueprint.

## Scope at a glance

- **Tier:** Full — every atomic step (ATS1–ATS14), every agent (AGN1–AGN6 + Deterministic Rule Engine), every HITL gate, all six workflows.
- **Integrations:** all five external systems mocked; TOL1–TOL8 built against mocks.
- **UX:** bilingual (Arabic RTL + English LTR) web app with a per-case step/trace view so every step and agent is visible at work.
- **Deliberately deferred to the coding agent / method:** application architecture and file layout; and (as explicit build deferrals) real SoR/customer/Ministry integration, real e-signature and auth, and statistical KPI baselining pending stakeholder volume/KPI data.

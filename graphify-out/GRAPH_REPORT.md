# Graph Report - adc-trade-agreements  (2026-11-13)

## Corpus Check
- 231 files · ~172,711 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: (none) 7, .example 2, .tsbuildinfo 2)

## Summary
- 2131 nodes · 3909 edges · 156 communities (113 shown, 43 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `094c525c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- setup-runtime.test.js
- validate.js
- smoke-local-package.mjs
- compile-check.js
- lint_wiki.py
- Open Knowledge Format (OKF)
- Kit Method Adapter: Spec Kit
- Phase 1: Cognitive Deconstruction
- cli.test.js
- package.json
- steps
- Enterprise App Kit LLM Wiki Profile
- Kit Scope Mapping
- auth_service.py
- Pitfall Registry
- manifest.yaml
- Abu Dhabi Customs - International Agreements & Origin Application
- UI Context
- LLM Wiki
- compilerOptions
- Scope Decisions
- Kit Backend Engineering
- Kit Method Adapter: OpenSpec 2
- Phase Payloads
- Workflow
- App Startup & Seeding
- Kit UI Design
- Slice Sizing: OpenSpec
- Slice Sizing: Spec Kit
- repositories
- Business Rules
- repositories
- Design Brief Template
- Implementation Brief — International Agreements & Origin Management Application
- Kit Conformance
- OpenSpec Delegation Contract
- Kit UI Context
- Integration Decisions
- README — Implementation Payload
- Enterprise App Kit Orchestrator
- Kit Design Language
- Kit Frontend Engineering
- Common Pitfalls
- interface
- Spec Kit Phase Sequence
- OpenSpec Workflow: Simple
- Product Delivery Slices Template
- minimal/README.md
- variant-worker-prompt-template.md
- auth-context.tsx
- International Agreements & Origin Application - Backend
- CaseTracePage.tsx
- database.py
- test_full_integration.py
- db_session
- CaseDetailPage.tsx
- AuthSessionModel
- health_check
- docker-entrypoint.sh
- adc-trade-agreements-backend
- App.tsx
- frontend/package.json
- SetupError
- compilerOptions
- validate_slices.py
- driver.js
- TASK-5 Handoff: Backend Authentication and Authorization
- compilerOptions
- Verification Checklist - TASK-8: Integration and End-to-End Testing
- prompt.js
- Backend Flows
- cases.py
- rate_limit.py
- Data Contracts
- status
- Agent Register
- correlation.py
- CaseQueuePage.tsx
- scripts
- CaseEventRepository
- CaseSubmissionForm.tsx
- @playwright/test
- Summary
- frontend/tsconfig.json
- UserModel
- main.py
- UUID
- TASK-4 Handoff: Backend Feature B2 - Intake Validation, Trace View, and Exception Actions
- scripts
- Agn1Orchestrator
- In-Scope Features Implemented and Tested
- test_case_acceptance.py
- test_case_integration.py
- seed_cases
- RoleResolution
- index.js
- case.ts
- case_registration_service.py
- trace.ts
- test_deterministic_rule_engine.py
- Implementation Status
- WorkflowCatalogService
- @types/node
- AuditService
- @vitejs/plugin-react
- Wireframes Implemented with E2E Specs
- Settings
- backend
- CaseAttachmentRepository
- Backend Endpoints Functional with Acceptance Tests
- Test Suite Results
- CaseRegistrationService
- database
- Auth Working with RBAC Enforcement
- Seed Data Loaded and Documented
- reset_rate_limiter
- schemas/case.py
- ICOS Adapter Mocked
- Startup Scripts Tested
- .record_case_event
- eslint.config.js
- Architecture
- common.py
- agn1_orchestrator.py
- Troubleshooting
- ExceptionActionForm.tsx
- Production Deployment Notes
- start.sh
- Testing
- Development Workflow
- Environment Configuration
- CI/CD
- Database Management
- Docker Deployment
- Prerequisites
- stop.sh

## God Nodes (most connected - your core abstractions)
1. `SetupError` - 50 edges
2. `CaseRepository` - 34 edges
3. `UserModel` - 33 edges
4. `hash_password()` - 32 edges
5. `CaseModel` - 27 edges
6. `status()` - 27 edges
7. `runSetup()` - 23 edges
8. `toolPackageSpec()` - 22 edges
9. `AuthService` - 21 edges
10. `note()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Observability` --references--> `AuditService`  [INFERRED]
  README.md → backend/app/services/audit_service.py
- `Trace Endpoint` --references--> `CaseTraceResponse`  [INFERRED]
  .handoff/TASK-4.md → backend/app/schemas/trace.py
- `AGN1 — Intake & Routing` --references--> `status()`  [INFERRED]
  payload/agent-register.md → src/setup/output.js
- `Case state model` --references--> `status()`  [INFERRED]
  payload/data-contracts.md → src/setup/output.js
- `Entities` --references--> `status()`  [INFERRED]
  payload/data-contracts.md → src/setup/output.js

## Import Cycles
- None detected.

## Communities (156 total, 43 thin omitted)

### Community 0 - "setup-runtime.test.js"
Cohesion: 0.09
Nodes (19): claudeCodeAdapter, codexAdapter, ibmBobAdapter, kiroAdapter, ADAPTER_BY_ID, ADAPTERS, writeYamlFile(), initGitRepo() (+11 more)

### Community 1 - "validate.js"
Cohesion: 0.08
Nodes (27): isSupportedAgent(), listAgentAdapters(), SUPPORTED_AGENT_IDS, main(), printRootHelp(), DEFAULTS, normalizeMode(), parseSetupArgs() (+19 more)

### Community 2 - "smoke-local-package.mjs"
Cohesion: 0.11
Nodes (19): allowedPayloadPackageDirectories, allowedPayloadPackageFiles, copiedKitRoot, forbiddenPackageFiles, forbiddenPackagePrefixes, keepWorkspace, kitRoot, normalizePath() (+11 more)

### Community 3 - "compile-check.js"
Cohesion: 0.11
Nodes (39): findAgentAdapter(), checkAdapter(), checkKitStructure(), checkPayload(), CheckResult, checkSchemas(), checkSelectedMethod(), checkSkills() (+31 more)

### Community 4 - "lint_wiki.py"
Cohesion: 0.06
Nodes (44): _alembic(), _annotation_kind(), _column_kind(), _env_py_text(), _foreign_key(), _has_alembic_version(), _last_name(), _mapped_columns() (+36 more)

### Community 5 - "Open Knowledge Format (OKF)"
Cohesion: 0.05
Nodes (41): 10.1 A computation is its own concept, 10.2 Contract fields, 10.3 The computation, 10.4 Concepts that use a computation, 10.5 How a consumer uses it (informative), 10.6 Verification versus attestation, 10. Attested computations concept, 11. Conformance (+33 more)

### Community 6 - "Kit Method Adapter: Spec Kit"
Cohesion: 0.18
Nodes (10): Completion Criteria, Delegation Reference, Integration Gate, Kit Method Adapter: Spec Kit, Operating Contract, Orchestrator Self-Check, Phase ledger, Scope Control (+2 more)

### Community 7 - "Phase 1: Cognitive Deconstruction"
Cohesion: 0.05
Nodes (37): 1.1 Atomic Thinking Step Register, 1.2 Business Ontology, 1.3 Autonomy Zone Map, 1.4 Human-in-the-Loop Specification, 1.5 Data Products Definition, 1.6 Integration with Systems of Record, 1.7 MCP Tool Register, 1.8 Agent Definition Register (+29 more)

### Community 8 - "cli.test.js"
Cohesion: 0.05
Nodes (50): packageRoot, requireFromBin, formatCliError(), ensureRuntimeDependencies(), hasRuntimeDependencies(), npmCommand(), packageRoot, RUNTIME_DEPENDENCIES (+42 more)

### Community 9 - "package.json"
Cohesion: 0.12
Nodes (19): bin, ent-app-kit, dependencies, ajv@^8.20.0, @clack/prompts@^1.7.0, yaml@^2.9.0, description, engines (+11 more)

### Community 10 - "steps"
Cohesion: 0.07
Nodes (31): runs-on, services, steps, DATABASE_URL, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, runs-on (+23 more)

### Community 11 - "Enterprise App Kit LLM Wiki Profile"
Cohesion: 0.11
Nodes (18): Agent Page, App Kit Content States, Build Workflow, Control Page, Decision Page, Enterprise App Kit LLM Wiki Profile, Eval Page, Graphify (+10 more)

### Community 12 - "Kit Scope Mapping"
Cohesion: 0.11
Nodes (18): 1. Discover and triage the payload, 2. Extract the Product / Boundary Model, 3. Handle source identifiers, 4. Classify the pitfall registry, 5. Load method sizing, 6. Decompose into slices, 7. Fill coverage and validate, Anti-Padding Rules (+10 more)

### Community 13 - "auth_service.py"
Cohesion: 0.11
Nodes (7): create_access_token(), decode_access_token(), verify_password(), test_health_endpoint(), test_jwt_token_creation(), test_password_hashing(), test_root_endpoint()

### Community 14 - "Pitfall Registry"
Cohesion: 0.12
Nodes (16): PIT-001: Integration depth, PIT-002: Source fidelity, PIT-003: Method shortcuts, PIT-004: README drift, PIT-005: Browser runtime validation, PIT-006: Startup and seeding, PIT-007: Unowned cross-cutting scope, PIT-008: Design fidelity (+8 more)

### Community 15 - "manifest.yaml"
Cohesion: 0.12
Nodes (15): defaults, agent, method, integrity, sbom, signing, kit, air_schema (+7 more)

### Community 16 - "Abu Dhabi Customs - International Agreements & Origin Application"
Cohesion: 0.20
Nodes (9): Abu Dhabi Customs - International Agreements & Origin Application, API Documentation, Directory Structure, Key Endpoints, License, Project Purpose, Quick Start (Local Development), Seed Credentials (+1 more)

### Community 17 - "UI Context"
Cohesion: 0.13
Nodes (14): Binding UI Inputs, Conflicts, Downstream Handling, Earning a row, Existing Frontend Conventions, External / User-Provided Authorities, Optional Inspiration, Promoted Screen Precedents (+6 more)

### Community 18 - "LLM Wiki"
Cohesion: 0.14
Nodes (13): Build A New Wiki, Bundle Location, Enterprise App Kit Profile, Ingest New Sources, Issues To Avoid, Lint A Wiki, LLM Wiki, Model (+5 more)

### Community 19 - "compilerOptions"
Cohesion: 0.15
Nodes (12): compilerOptions, allowJs, checkJs, lib, module, moduleResolution, noEmit, skipLibCheck (+4 more)

### Community 20 - "Scope Decisions"
Cohesion: 0.17
Nodes (11): Agents in scope, Assumptions, Build tier and pattern, Deferred scope, External systems, MCP tools in scope, `[NEEDS CLARIFICATION]` markers (max 3), Repository topology (+3 more)

### Community 21 - "Kit Backend Engineering"
Cohesion: 0.17
Nodes (11): Baseline, Evidence, Kit Backend Engineering, Planning And Review, Reject, Runtime Safety, Scale First, Shape And Contracts (+3 more)

### Community 22 - "Kit Method Adapter: OpenSpec 2"
Cohesion: 0.17
Nodes (11): Authority, Boundaries, Delegation Gate, Kit Method Adapter: OpenSpec 2, Ledger, Operation Surface, Orchestrator Self-Check, Required Setup (+3 more)

### Community 23 - "Phase Payloads"
Cohesion: 0.17
Nodes (11): Failure Signatures, Phase Payloads, Required Worker Report, Spec Kit Delegation Shape, `speckit-checklist`, `speckit-tasks`, `speckit-analyze`, `speckit-clarify`, `speckit-converge`, `speckit-implement` (+3 more)

### Community 24 - "Workflow"
Cohesion: 0.17
Nodes (11): 1. Discover Before Asking, 2. Ask scoping questions (user input required), 3. Create A Brief (user input required), 4. Worker delegation, 5. Maintain The Gallery (user input required), 6. Promote Only Decisions, Boundaries, Context Boundary (+3 more)

### Community 25 - "App Startup & Seeding"
Cohesion: 0.18
Nodes (10): App Startup & Seeding, Completion Checklist, Core Outcome, Discover First, Environment Configuration, Process Requirements, Required Capabilities, Root Composition (+2 more)

### Community 26 - "Kit UI Design"
Cohesion: 0.18
Nodes (10): App Kit Frontend Contract, Binding UI Inputs, Design / Code Conflicts, Design Engine, Design Inputs, Design Review Checklist, Interaction Model Fit, Kit UI Design (+2 more)

### Community 27 - "Slice Sizing: OpenSpec"
Cohesion: 0.20
Nodes (9): Capability Slice Sizing, Hard Rejection Gates, If A Slice Proves Oversized Later, Merge Triggers, Non-Capability Slice Sizing, OpenSpec Discipline, Slice Sizing: OpenSpec, Split Triggers (+1 more)

### Community 28 - "Slice Sizing: Spec Kit"
Cohesion: 0.20
Nodes (9): Capability Slice Sizing, Hard Rejection Gates, If A Slice Proves Oversized Later, Merge Triggers, Non-Capability Slice Sizing, Slice Sizing: Spec Kit, Spec Kit Discipline, Split Triggers (+1 more)

### Community 29 - "repositories"
Cohesion: 0.22
Nodes (8): repositories, description, name, role, source, workspace_path, schema, topology

### Community 30 - "Business Rules"
Cohesion: 0.22
Nodes (8): BR-02 — Advance-ruling completeness & eligibility gate, BR-04 — Extraction confidence gate, BR-06 — Rules-of-origin determination criteria, BR-09 — Legal / regulatory constraint checks, BR-11 — Authority / approval matrix, BR-14 — Objection legal-time-limit check, Business Rules, Reliability constraints (Full tier)

### Community 31 - "repositories"
Cohesion: 0.22
Nodes (8): repositories, description, name, role, source, workspace_path, schema, topology

### Community 32 - "Design Brief Template"
Cohesion: 0.22
Nodes (8): Binding Design Inputs, Design Brief Template, Guardrails, Reference Library *(optional but high-leverage)*, Screen, Shared Design Constraints, Variant Directions, Variant Plan

### Community 33 - "Implementation Brief — International Agreements & Origin Management Application"
Cohesion: 0.25
Nodes (7): Implementation Brief — International Agreements & Origin Management Application, Key constraints and compliance posture, Objective, Primary workflows (all in scope at Full tier), Resolved tech stack (provenance-tagged), Selected build scope and acceptance intent, Target users

### Community 34 - "Kit Conformance"
Cohesion: 0.25
Nodes (7): Conformance Evidence To Check, Defect-Oriented Code Review Pass, Inputs, Kit Conformance, Report, Sweep, UI Surface Wiring

### Community 35 - "OpenSpec Delegation Contract"
Cohesion: 0.25
Nodes (7): Context Placement, Examples, Grammar, OpenSpec Delegation Contract, Pre-Delegation Checklist, Reject If, Three-Class Test

### Community 36 - "Kit UI Context"
Cohesion: 0.25
Nodes (7): 1. Scan, 2. Label Each Source, 3. Extract UI Context, 4. Write The Report, 5. Report Back, Kit UI Context, What This Skill Does Not Do

### Community 37 - "Integration Decisions"
Cohesion: 0.29
Nodes (6): Environment and credential assumptions, External systems, Failure / unavailability expectations, Integration Decisions, MCP tools, Orphaned-dependency handling

### Community 38 - "README — Implementation Payload"
Cohesion: 0.29
Nodes (6): Files, How packaging works, README — Implementation Payload, Scope at a glance, What downstream owns, What this is

### Community 39 - "Enterprise App Kit Orchestrator"
Cohesion: 0.29
Nodes (6): Application Delivery Routing Skills, Context Management And Subagents, Core Rules, Enterprise App Kit Orchestrator, Orchestration Procedure, Resuming A Run

### Community 40 - "Kit Design Language"
Cohesion: 0.33
Nodes (5): Completion Gate, Impeccable, Inputs, Kit Design Language, Outputs

### Community 41 - "Kit Frontend Engineering"
Cohesion: 0.33
Nodes (5): Engineering Baseline, Equivalence Examples, Failure Conditions, Kit Frontend Engineering, Planning And Review

### Community 42 - "Common Pitfalls"
Cohesion: 0.33
Nodes (5): Always Check, Common Pitfalls, Core Rule, Pitfall Registry, Review Bias

### Community 43 - "interface"
Cohesion: 0.40
Nodes (4): interface, default_prompt, display_name, short_description

### Community 44 - "Spec Kit Phase Sequence"
Cohesion: 0.40
Nodes (4): Advancement Rules, Phase Responsibilities, Required Sequence, Spec Kit Phase Sequence

### Community 45 - "OpenSpec Workflow: Simple"
Cohesion: 0.50
Nodes (3): OpenSpec Workflow: Simple, Review Gate, Steps

### Community 49 - "auth-context.tsx"
Cohesion: 0.39
Nodes (6): AuthContext, AuthContextType, AuthSession, LoginRequest, LoginResponse, User

### Community 50 - "International Agreements & Origin Application - Backend"
Cohesion: 0.09
Nodes (22): API Endpoints, Architecture, Authentication (to be implemented in later tasks), Cases (to be implemented in later tasks), Code Quality, Database Schema, Database Setup, Default Users (+14 more)

### Community 51 - "CaseTracePage.tsx"
Cohesion: 0.14
Nodes (11): AgentRegistryPanel(), ApprovalChainDisplay(), ApprovalChainDisplayProps, CaseTraceTimeline(), CaseTraceTimelineProps, DetailedEventStream(), DetailedEventStreamProps, CaseTracePage() (+3 more)

### Community 52 - "database.py"
Cohesion: 0.08
Nodes (8): run_migrations_offline(), run_migrations_online(), upgrade(), Base, AgentDefinitionModel, AuditLogModel, AuthSessionModel, CaseEventModel

### Community 53 - "test_full_integration.py"
Cohesion: 0.18
Nodes (7): test_case_trace_with_visibility_filtering(), test_complete_case_registration_flow(), test_correlation_id_propagation(), test_exception_action_with_rbac_enforcement(), test_incomplete_submission_blocking_flow(), test_pagination_and_filtering(), test_workflow_classification_for_all_types()

### Community 54 - "db_session"
Cohesion: 0.22
Nodes (3): client(), db_session(), _fresh_schema()

### Community 55 - "CaseDetailPage.tsx"
Cohesion: 0.24
Nodes (7): AgentExecutionPanel(), AgentExecutionPanelProps, CaseDetailView(), CaseDetailViewProps, StateTransitionFlow(), StateTransitionFlowProps, CaseDetailPage()

### Community 68 - "App.tsx"
Cohesion: 0.17
Nodes (15): dependencies, react@^18.3.1, react-dom@^18.3.1, react-router-dom@^6.28.0, App(), LoginPage(), RequireAuth(), AppBar() (+7 more)

### Community 69 - "frontend/package.json"
Cohesion: 0.11
Nodes (23): devDependencies, autoprefixer@^10.4.20, eslint@^9.17.0, jsdom@^25.0.1, postcss@^8.4.49, tailwindcss@^3.4.17, @testing-library/jest-dom@^6.6.3, @types/react@^18.3.18 (+15 more)

### Community 70 - "SetupError"
Cohesion: 0.20
Nodes (26): initOpenSpecWorkspace(), initSpeckitWorkspace(), note(), commandExists(), isolatedNpmExecEnv(), runLoggedCommand(), SetupError, spawn() (+18 more)

### Community 71 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleDetection, moduleResolution (+11 more)

### Community 72 - "validate_slices.py"
Cohesion: 0.26
Nodes (26): cell(), collect_sections(), fail(), find_table(), is_separator(), load_registry_pit_ids(), main(), meaningful() (+18 more)

### Community 73 - "driver.js"
Cohesion: 0.23
Nodes (18): agentInstructionsKeptWarning(), agentInstructionsPolicyError(), driverContextBlock(), driverFocusBlock(), driverImplementationFidelityBlock(), driverLlmWikiBlock(), driverMethodBlock(), driverStartupSeedingBlock() (+10 more)

### Community 74 - "TASK-5 Handoff: Backend Authentication and Authorization"
Cohesion: 0.05
Nodes (43): auth_sessions, Authentication Endpoints (AS MOUNTED), Available Seed Users:, Backend Flows, Compliance Notes, Configuration, CORS, Database Tables (+35 more)

### Community 75 - "compilerOptions"
Cohesion: 0.12
Nodes (15): compilerOptions, allowImportingTsExtensions, isolatedModules, lib, module, moduleDetection, moduleResolution, noEmit (+7 more)

### Community 76 - "Verification Checklist - TASK-8: Integration and End-to-End Testing"
Cohesion: 0.13
Nodes (14): ✅ Agent Registry, ✅ AGN1: Intake & Routing Agent, AGN1 Orchestration Functional, AGN2–AGN6 Registered as Deferred, ✅ Audit Log Implementation, Audit Trail Recording All Events, Docker Compose Verified, ✅ docker-compose.yml (+6 more)

### Community 77 - "prompt.js"
Cohesion: 0.20
Nodes (20): AGENT_CHOICES, clackCancel(), clackIo(), deliveryMethodOverview(), exampleSetupCommand(), executionModeOverview(), formatSetupSelection(), formatSetupTitle() (+12 more)

### Community 78 - "Backend Flows"
Cohesion: 0.12
Nodes (16): Architecture Notes, Backend Flows, Case Registration Flow, Cases, Endpoints Implemented, Error Handling, GET /api/v1/cases, GET /api/v1/cases/{case_id} (+8 more)

### Community 79 - "cases.py"
Cohesion: 0.12
Nodes (7): get_current_user(), get_case(), list_cases(), record_exception_action(), register_case(), CaseDetailResponse, ExceptionActionResponse

### Community 81 - "Data Contracts"
Cohesion: 0.20
Nodes (9): Case state model, Data Contracts, Entities, Fixture shapes (mock systems), Integration notes (variety the fixtures must exercise), Review (HITL) sub-state model, Shape examples, Shared enums / value sets (+1 more)

### Community 82 - "status"
Cohesion: 0.20
Nodes (15): MCP Tool Register, TOL1 — Case & Request Store, TOL2 — Customs Declaration Lookup, TOL3 — Origin Rules & Agreements Knowledge, TOL4 — Tariff Classification Cross-Check, TOL5 — Document Drafting & Template, TOL6 — Notification & Publication, TOL7 — Audit & Evidence Recorder (+7 more)

### Community 83 - "Agent Register"
Cohesion: 0.22
Nodes (8): Agent Register, AGN1 — Intake & Routing, AGN2 — Content Extraction, AGN3 — Rules & Origin Determination, AGN4 — Ruling / Correspondence Drafting, AGN5 — Decision & Issuance, AGN6 — Dispute Adjudication, Deterministic Rule Engine

### Community 85 - "CaseQueuePage.tsx"
Cohesion: 0.13
Nodes (18): CaseItem, CaseListTable(), Props, FilterBar(), FilterValues, Props, PaginationControls(), Props (+10 more)

### Community 86 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, lint, preview, test, type-check

### Community 88 - "CaseSubmissionForm.tsx"
Cohesion: 0.17
Nodes (12): vitest@^2.1.8, AttachmentMetadata, CaseSubmissionForm(), CreateCaseRequest, CreateCaseResponse, Props, ValidationError, apiClient (+4 more)

### Community 90 - "Summary"
Cohesion: 0.29
Nodes (7): Acceptance Checks Status, ✅ All Backend Endpoints Functional, ✅ All In-Scope Features Implemented, ✅ All Requirements Met, ✅ All Wireframes Implemented, ✅ Complete Test Coverage, Summary

### Community 96 - "UserModel"
Cohesion: 0.06
Nodes (30): hash_password(), hash_token(), UserModel, AuthService, auth_client(), test_login_endpoint_returns_token(), test_logout_endpoint_revokes_session(), test_protected_endpoint_requires_auth() (+22 more)

### Community 97 - "main.py"
Cohesion: 0.05
Nodes (12): get_db(), lifespan(), root(), register_error_handlers(), login(), logout(), get_case_trace(), AuthUser (+4 more)

### Community 98 - "UUID"
Cohesion: 0.07
Nodes (20): CaseModel, CaseRepository, ApprovalStageDTO, CaseEventDTO, CaseStepDTO, CaseTraceService, VisibilityPolicyService, test_exception_action_close_rejected() (+12 more)

### Community 99 - "TASK-4 Handoff: Backend Feature B2 - Intake Validation, Trace View, and Exception Actions"
Cohesion: 0.09
Nodes (21): Agent Registry, AGN1 Intake Orchestration (ATS1-ATS3), API Endpoints Added, audit_logs, Backend Flows, case_events, Database Tables, Dependencies (+13 more)

### Community 100 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, coverage, test, test:assets, test:smoke, test:smoke:container, test:unit, typecheck (+1 more)

### Community 101 - "Agn1Orchestrator"
Cohesion: 0.13
Nodes (6): Agn1Orchestrator, IntakeOutcome, RoutingService, test_agn1_blocks_on_incomplete_submission(), test_agn1_blocks_on_ineligible_workflow(), test_agn1_start_intake_success()

### Community 102 - "In-Scope Features Implemented and Tested"
Cohesion: 0.33
Nodes (6): FR-001: Register incoming case types ✅, FR-002: Validate completeness and eligibility at intake ✅, FR-004: Route cases to correct workflow and queue ✅, FR-023: Per-case step and trace view ✅, FR-024: Visibility of reasoning, routing, and approvals ✅, In-Scope Features Implemented and Tested

### Community 103 - "test_case_acceptance.py"
Cohesion: 0.11
Nodes (8): test_get_case_by_id(), test_get_case_not_found(), test_get_cases_returns_paginated_list(), test_get_cases_with_filters(), test_get_cases_with_pagination(), test_post_cases_creates_case(), test_post_cases_invalid_workflow_type(), test_post_cases_with_attachments()

### Community 104 - "test_case_integration.py"
Cohesion: 0.11
Nodes (5): WorkflowType, StepResolution, WorkflowClassification, test_routing_service_step_resolution(), test_routing_service_workflow_classification()

### Community 105 - "seed_cases"
Cohesion: 0.25
Nodes (4): run_seed(), seed_cases(), seed_users(), test_seed_data_creates_users()

### Community 107 - "index.js"
Cohesion: 0.18
Nodes (24): getAgentAdapter(), resolveAgentInstructionsPolicy(), initImpeccable(), installImpeccableSkillOnlyFromCodex(), normalizeSkillOnlyMarkdown(), runImpeccableInstall(), runSetup(), formatToolOutput() (+16 more)

### Community 108 - "case.ts"
Cohesion: 0.25
Nodes (7): AgentExecutionSummary, CaseAttachment, CaseDetailResponse, CaseEvent, CaseModel, ExceptionActionRequest, ExceptionActionResponse

### Community 109 - "case_registration_service.py"
Cohesion: 0.15
Nodes (3): IcosRegistrationAdapter, IcosRegistrationResult, test_icos_adapter_mock_registration()

### Community 110 - "trace.ts"
Cohesion: 0.25
Nodes (7): ApprovalStage, ApprovalStageDTO, AuditLog, CaseEventDTO, CaseStepDTO, CaseTraceResponse, Step

### Community 111 - "test_deterministic_rule_engine.py"
Cohesion: 0.10
Nodes (13): DeterministicRuleEngine, RuleDecision, test_all_workflow_types_are_valid(), test_evaluate_completeness_fails_missing_fields(), test_evaluate_completeness_success(), test_evaluate_eligibility_fails_invalid_workflow(), test_evaluate_eligibility_success(), test_evaluate_routing_constraints_fails_non_mvp_step() (+5 more)

### Community 112 - "Implementation Status"
Cohesion: 0.40
Nodes (5): ✅ Backend Seed Module Fixed, ✅ Completed E2E Journey Test, ✅ Completed Integration Test Files, ✅ Completed Verification Checklist Document, Implementation Status

### Community 115 - "@types/node"
Cohesion: 0.29
Nodes (7): @types/node@^22.10.2, typescript@^5.7.2, devDependencies, @types/node@^26.2.0, typescript@^7.0.2, @types/node, typescript

### Community 117 - "@vitejs/plugin-react"
Cohesion: 0.33
Nodes (4): vite@^6.0.5, @vitejs/plugin-react@^4.3.4, vite, @vitejs/plugin-react

### Community 118 - "Wireframes Implemented with E2E Specs"
Cohesion: 0.40
Nodes (5): ✅ wireframe_01: Case Submission (wireframe_case_submission.html), ✅ wireframe_02: Case Queue (wireframe_case_queue.html), ✅ wireframe_03: Case Detail (wireframe_case_detail.html), ✅ wireframe_04: Case Trace (wireframe_case_trace.html), Wireframes Implemented with E2E Specs

### Community 121 - "backend"
Cohesion: 0.12
Nodes (18): build, environment, ports, volumes, x-preview-port, args, context, dockerfile (+10 more)

### Community 124 - "Backend Endpoints Functional with Acceptance Tests"
Cohesion: 0.50
Nodes (4): ✅ Authentication Endpoints, Backend Endpoints Functional with Acceptance Tests, ✅ Case Management Endpoints, ✅ Health Check

### Community 127 - "Test Suite Results"
Cohesion: 0.50
Nodes (4): Backend Tests ✅, Frontend Tests ✅, Static Analysis ✅, Test Suite Results

### Community 130 - "CaseRegistrationService"
Cohesion: 0.14
Nodes (9): CreateCaseRequest, CaseRegistrationService, test_case_repository_list_with_filters(), test_full_registration_flow_with_database(), test_generate_case_reference(), test_register_case_agreement_update(), test_register_case_dispute(), test_register_case_origin_ruling() (+1 more)

### Community 131 - "database"
Cohesion: 0.13
Nodes (14): build, depends_on, environment, args, environment, image, ports, volumes (+6 more)

### Community 132 - "Auth Working with RBAC Enforcement"
Cohesion: 0.67
Nodes (3): Auth Working with RBAC Enforcement, ✅ Authentication, ✅ Authorization (RBAC)

### Community 133 - "Seed Data Loaded and Documented"
Cohesion: 0.67
Nodes (3): ✅ Seed Cases (4 sample cases), Seed Data Loaded and Documented, ✅ Seed Users (7 roles)

### Community 135 - "schemas/case.py"
Cohesion: 0.21
Nodes (5): AgentExecutionSummary, AttachmentMetadata, CaseListItem, CaseListResponse, CaseRecordResponse

### Community 140 - ".record_case_event"
Cohesion: 0.25
Nodes (3): AuditService, test_exception_action_records_event(), AuditService

### Community 141 - "eslint.config.js"
Cohesion: 0.18
Nodes (10): @eslint/js@^9.17.0, eslint-plugin-react-hooks@^5.1.0, eslint-plugin-react-refresh@^0.4.16, globals@^15.14.0, typescript-eslint@^8.18.2, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh (+2 more)

### Community 142 - "Architecture"
Cohesion: 0.20
Nodes (8): require_role(), Agent Orchestration, Architecture, Backend Stack, Frontend Stack, Key Features Implemented (MVP Scope), Observability, Security Features

### Community 146 - "Troubleshooting"
Cohesion: 0.25
Nodes (8): Authentication Issues, Database Migration Errors, Docker Issues, Frontend Build Errors, Node Version Issues, Port Already in Use, Python Version Issues, Troubleshooting

### Community 147 - "ExceptionActionForm.tsx"
Cohesion: 0.20
Nodes (7): @testing-library/react@^16.1.0, ExceptionActionForm(), ExceptionActionFormProps, mockCases, mockNavigate, renderForm(), @testing-library/react

### Community 148 - "Production Deployment Notes"
Cohesion: 0.33
Nodes (6): Compliance, Database, Infrastructure, Monitoring, Production Deployment Notes, Security

### Community 149 - "start.sh"
Cohesion: 0.53
Nodes (4): check_prerequisites(), find_available_port(), port_in_use(), start.sh script

### Community 151 - "Testing"
Cohesion: 0.50
Nodes (4): Backend Tests, End-to-End Tests, Frontend Tests, Testing

### Community 153 - "Development Workflow"
Cohesion: 0.67
Nodes (3): Adding a New Feature, Code Quality, Development Workflow

### Community 154 - "Environment Configuration"
Cohesion: 0.67
Nodes (3): Backend (`backend/.env`), Environment Configuration, Frontend

### Community 155 - "CI/CD"
Cohesion: 0.67
Nodes (3): Backend Job, CI/CD, Frontend Job

### Community 156 - "Database Management"
Cohesion: 0.67
Nodes (3): Database Management, Migrations, Seed Data

### Community 157 - "Docker Deployment"
Cohesion: 0.67
Nodes (3): Docker Deployment, PostgreSQL (Production), SQLite (Development/Single-Instance)

### Community 158 - "Prerequisites"
Cohesion: 0.67
Nodes (3): For Docker Deployment, For Local Development (No Docker Required), Prerequisites

## Knowledge Gaps
- **1 isolated node(s):** `adc-trade-agreements-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1134 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuditService` connect `.record_case_event` to `UUID`, `Agn1Orchestrator`, `Architecture`, `cases.py`, `agn1_orchestrator.py`, `AuditService`, `database.py`, `CaseEventRepository`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `adc-trade-agreements-backend` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `setup-runtime.test.js` be split into smaller, more focused modules?**
  _Cohesion score 0.0945945945945946 - nodes in this community are weakly interconnected._
- **Why does `Architecture` connect `Architecture` to `Abu Dhabi Customs - International Agreements & Origin Application`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `validate.js` be split into smaller, more focused modules?**
  _Cohesion score 0.07781649245063879 - nodes in this community are weakly interconnected._
- **Why does `Abu Dhabi Customs - International Agreements & Origin Application` connect `Abu Dhabi Customs - International Agreements & Origin Application` to `Architecture`, `Troubleshooting`, `Production Deployment Notes`, `Testing`, `Development Workflow`, `Environment Configuration`, `CI/CD`, `Database Management`, `Docker Deployment`, `Prerequisites`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `smoke-local-package.mjs` be split into smaller, more focused modules?**
  _Cohesion score 0.10507246376811594 - nodes in this community are weakly interconnected._
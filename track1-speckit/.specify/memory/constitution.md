<!--
SYNC IMPACT REPORT
==================
Version Change: NONE → 1.0.0
Rationale: Initial constitution creation with 7 core principles for the project.

Modified Principles: N/A (initial creation)

Added Sections:
- Article I — Simplicity First
- Article II — Testability Mandate
- Article III — Explainability Requirement
- Article IV — Data-Driven Design
- Article V — Deterministic Behavior
- Article VI — Separation of Concerns
- Article VII — Python Best Practices
- Governance (Amendment Process)

Removed Sections: N/A

Templates Status:
- ✅ .specify/templates/plan-template.md - Constitution Check section present, aligns with principles
- ✅ .specify/templates/spec-template.md - User scenarios and requirements structure supports testability and explainability mandates
- ✅ .specify/templates/tasks-template.md - Phase-based organization supports separation of concerns and simplicity-first approach

Follow-up TODOs: None

Impact Summary:
This is the initial constitution establishing the foundational principles for the speckit-bmad project.
All principles are concrete, testable, and align with existing template structures.
No breaking changes as this is the first version.
-->

# speckit-bmad Constitution

## Core Principles

### Article I — Simplicity First

All implementations **MUST** favor the simplest solution that satisfies the specification.

- Maximum **1 module** for the initial implementation.
- No speculative features or "might need" functionality.
- Every function must trace directly to a requirement in the specification.

**Rationale**: Complexity is the enemy of maintainability and correctness. By enforcing 
simplicity from the start, we ensure that the codebase remains understandable, testable, 
and evolvable. This principle prevents over-engineering and keeps development focused on 
delivering actual requirements rather than anticipated future needs.

### Article II — Testability Mandate

All business logic **MUST** be testable in isolation.

- Pure functions are preferred over stateful classes.
- Every scoring rule must have at least one corresponding test case.
- Edge cases (empty input, no matching preferences) must be covered.

**Rationale**: Testable code is maintainable code. By requiring isolation and pure functions, 
we ensure that every component can be verified independently. This principle enables confident 
refactoring and prevents regression bugs. The explicit requirement for edge case coverage 
ensures robustness in production scenarios.

### Article III — Explainability Requirement

Every output highlight **MUST** include a human-readable explanation.

- Explanations must reference the specific scoring factors that led to selection.
- No "black box" decisions — the user must understand *why* each highlight was chosen.
- Explanations should be concise (1–2 sentences) and non-technical.

**Rationale**: Transparency builds trust and enables users to understand system behavior. 
When outputs are explainable, users can validate correctness, provide better feedback, and 
trust the system's decisions. This principle prevents opaque algorithms and ensures that 
the system remains accountable and debuggable.

### Article IV — Data-Driven Design

The system **MUST** operate on well-defined data contracts.

- Input and output schemas are defined before implementation.
- All data flows through typed models (dataclasses or equivalent).
- JSON is the interchange format for all external interfaces.

**Rationale**: Clear data contracts prevent integration bugs and enable independent component 
development. By defining schemas upfront, we establish clear boundaries between components. 
Type safety catches errors at development time rather than production. JSON standardization 
ensures interoperability with external systems and tools.

### Article V — Deterministic Behavior

Given identical inputs, the system **MUST** produce identical outputs.

- No randomness in the scoring or selection algorithm.
- Tie-breaking rules must be explicit and documented.
- Results are fully reproducible for debugging and testing.

**Rationale**: Determinism is essential for testing, debugging, and user trust. 
Non-deterministic systems are nearly impossible to test comprehensively and create 
user confusion when behavior varies. Explicit tie-breaking rules ensure consistency 
and make system behavior predictable and verifiable.

### Article VI — Separation of Concerns

The implementation **MUST** clearly separate:

- **Data models** — Input/output type definitions
- **Scoring logic** — The algorithm that assigns scores to events
- **Selection logic** — The filter/rank/limit pipeline
- **Explanation generation** — Human-readable reason construction

**Rationale**: Clear separation enables independent development, testing, and modification 
of each component. This principle prevents tangled dependencies and makes the system easier 
to understand, maintain, and extend. Each concern can evolve independently without affecting 
others, supporting long-term maintainability.

### Article VII — Python Best Practices

All code **MUST** follow modern Python conventions:

- Type hints on all function signatures.
- Docstrings on all public functions and classes.
- PEP 8 compliance.
- No external dependencies beyond the Python standard library.

**Rationale**: Consistent code style and documentation make the codebase accessible to all 
contributors. Type hints enable better IDE support and catch errors early. PEP 8 compliance 
ensures readability. Standard library-only restriction minimizes dependency management 
overhead and security vulnerabilities, keeping the project lightweight and maintainable.

## Governance

This constitution supersedes all other development practices and decisions. All implementation 
work, code reviews, and design decisions **MUST** verify compliance with these principles.

Any complexity that appears to violate these principles must be explicitly justified with 
documented rationale in the relevant specification or plan document.

### Amendment Process

Modifications to this constitution require:

1. Explicit documentation of the rationale for change.
2. Review and approval by the project maintainer.
3. Backward compatibility assessment.

All amendments must follow semantic versioning:
- **MAJOR** version increment for backward-incompatible changes (principle removal/redefinition)
- **MINOR** version increment for new principles or material expansions
- **PATCH** version increment for clarifications, wording fixes, or non-semantic refinements

**Version**: 1.0.0 | **Ratified**: 2026-02-17 | **Last Amended**: 2026-02-17

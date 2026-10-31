---
name: architecture-decision-record
description: 'Use when proposing software architectures from requirements, comparing alternatives, selecting an architecture, or creating and reviewing an Architecture Decision Record (ADR). Covers requirements analysis, trade-offs, decision criteria, diagrams, requirement mapping, assumptions, and conversation notes.'
argument-hint: 'Describe the system requirements or point to Task 1 and Task 2 discussion files.'
user-invocable: true
---

# Architecture Decision Record Workflow

## Purpose

Create a traceable architecture proposal from software requirements. The
workflow compares multiple alternatives, makes an explicit decision, and
produces an ADR that another engineer can review without seeing the original
conversation.

## When to Use

Use this skill when the user asks to:

- propose an architecture from requirements or user stories;
- compare a monolith, modular monolith, microservices, serverless, event-driven,
  or other architecture styles;
- choose an architecture and document the choice in an ADR;
- review or improve an existing ADR;
- map requirements, assumptions, risks, or quality attributes to architecture.

## Required Inputs

1. Read the requirements source, such as a `data/*.txt` file.
2. Read any existing Task 1 conversation notes before proposing a decision.
3. Read any existing Task 2 conversation notes before modifying an ADR.
4. Identify the system scope, actors, functional requirements, quality
   attributes, constraints, external dependencies, and unknowns.

Do not invent project facts silently. Mark inferred facts as assumptions and
record them in the ADR.

## Procedure

### 1. Capture notes

At the beginning, tell the user that concise discussion notes will be written.
Maintain a conversation record containing decisions, user objections, and
resulting corrections. It is a summary, not a verbatim transcript.

### 2. Establish the local hypothesis

Before editing, state internally:

- which requirement or architecture boundary controls the decision;
- one falsifiable hypothesis about the best architecture;
- one cheap check that could disconfirm it.

Use the smallest relevant read of nearby requirements and existing notes.

### 3. Propose alternatives

Describe at least three materially different alternatives. For each one,
include:

- component or service boundaries;
- data ownership and communication style;
- deployment model;
- consistency and failure behavior;
- difficult implementation areas;
- advantages and disadvantages for this specific system.

Do not compare architecture names only. Explain how each alternative handles the
most difficult user flows.

### 4. Define decision criteria

Create an explicit, prioritized list of criteria before scoring alternatives.
Typical criteria include:

- data consistency and integrity;
- security and privacy;
- development and operational complexity;
- resilience to external dependencies;
- independent scaling and fault isolation;
- first-version cost;
- local testability and deployment model;
- future extensibility.

Every row in the comparison table must correspond to exactly one criterion.
Use the same names in the criteria list and table.

### 5. Select and justify

Choose one alternative and record:

- the decision and status;
- the context and constraints;
- why the selected option wins against the criteria;
- positive and negative consequences;
- risks and mitigations;
- conditions that would trigger a future review;
- a gradual migration path if the decision changes.

Prefer the simplest architecture that satisfies the stated requirements and
quality attributes. Do not select microservices or serverless solely because
they are familiar patterns.

### 6. Add visual architecture

Use Mermaid diagrams in Markdown. Include at least:

1. a component or deployment view showing the client, API, modules/services,
   databases, workers, and external systems;
2. a flow diagram for the most failure-prone asynchronous or cross-module flow.

Avoid ASCII architecture diagrams when Mermaid can represent the same view.
Keep labels short and ensure the diagram matches the prose.

### 7. Map requirements

Add a traceability table mapping functional requirement IDs or ranges to:

- the responsible module or service;
- the relevant API/data mechanism;
- important consistency, security, or authorization behavior.

Add a separate mapping for non-functional requirements such as performance,
security, resilience, observability, and testability.

### 8. Record objections and revisions

After each user critique, append a short entry to the Task 2 conversation file:
what the user objected to and what was changed. Do not claim that a review
happened if it did not happen.

## ADR Structure

Use this order unless the existing repository has a stronger convention:

1. Title and metadata (`Status`, date, decision)
2. Context
3. Considered alternatives
4. Decision criteria
5. Comparison table
6. Decision
7. Visual architecture
8. Modules or service boundaries
9. Requirement mapping
10. Data and transactions
11. Security and reliability
12. Non-functional requirements
13. Non-functional assumptions
14. Consequences
15. Risks and mitigations
16. Verification and future review conditions

## Validation Checklist

Before finishing, verify:

- the selected status is intentional, usually `Accepted` after user approval;
- at least three alternatives are compared;
- every table row has a matching decision criterion;
- all functional requirement IDs are covered;
- assumptions are separated from requirements;
- the diagrams contain the same components described in the text;
- external failures, authorization, idempotency, and transactions are addressed;
- the ADR and conversation record have no diagnostics or malformed Markdown;
- the final response links to the created files and mentions validation.

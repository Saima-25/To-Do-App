---
description: Validate and clarify requirements before any planning or coding begins. Used by Domain Agent and Spec Manager Agent to enforce spec-first discipline.
handoffs:
  - label: Create Specification
    agent: sp.specify
    prompt: Create a specification from the validated requirements
  - label: Clarify Further
    agent: sp.clarify
    prompt: Perform deeper clarification on the spec
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

# Skill: Validate Requirements

## Skill Metadata

| Attribute | Value |
|-----------|-------|
| **Skill Name** | `sp.validate-requirements` |
| **Purpose** | Validate and clarify requirements before any planning or coding to enforce spec-first development discipline |
| **Used By** | `todo-domain-agent`, `todo-spec-manager` |
| **Phase** | Pre-specification / Requirement Analysis |
| **Hackathon Alignment** | Judge-friendly, auditable, traceable |

---

## Purpose

This skill ensures that requirements are complete, clear, and validated **before** any specification writing, planning, or implementation begins. It acts as the first gate in the spec-first development workflow, preventing:

- Vibe coding (implementing without clear requirements)
- Scope creep (adding features not explicitly requested)
- Ambiguous specifications (writing specs from unclear requirements)
- Untraceable work (losing the requirement-to-code chain)

---

## Capabilities

### 1. Requirement Completeness Check
Validate that all necessary requirement elements are present:

- [ ] **User Intent**: What does the user want to accomplish?
- [ ] **Success Criteria**: How will we know it's done correctly?
- [ ] **Scope Boundaries**: What is explicitly in/out of scope?
- [ ] **User Context**: Who is the user and what is their environment?
- [ ] **Constraints**: Any limitations or restrictions mentioned?

### 2. Ambiguity Detection
Identify unclear or missing information:

- Vague terms ("fast", "easy", "good") without measurable definitions
- Implicit assumptions that need explicit confirmation
- Missing edge case definitions
- Undefined error handling expectations
- Unclear user flows or interactions

### 3. Domain Validation (via Domain Agent)
When invoked by or consulting with `todo-domain-agent`:

- Validate requirements align with Todo CLI domain expectations
- Confirm user stories reflect real user needs
- Identify domain-specific edge cases
- Ensure terminology is consistent with CLI conventions

### 4. Spec-Readiness Assessment (via Spec Manager Agent)
When invoked by or consulting with `todo-spec-manager`:

- Confirm requirements are ready for formal specification
- Identify gaps that would block spec creation
- Validate traceability chain is maintainable
- Ensure requirements meet audit/judge standards

### 5. Clarification Question Generation
Generate targeted questions to resolve ambiguities:

- Maximum 5 questions per validation session
- Each question must be:
  - Answerable with a short response or multiple choice
  - Directly impactful on specification or acceptance criteria
  - Prioritized by impact (scope > security > UX > technical)

---

## Constraints

### This Skill MUST NOT:

1. **Generate or suggest code** - No implementation logic, no code snippets, no pseudocode
2. **Make architecture decisions** - No database choices, no API designs, no file structures
3. **Expand features beyond requirements** - No "nice to have" additions
4. **Define technical implementation** - No frameworks, libraries, or tools
5. **Create specifications** - Only validate readiness for specification creation
6. **Override user requirements** - Only clarify, never change without consent

### This Skill MUST:

1. **Preserve user intent verbatim** - Quote requirements exactly as stated
2. **Document all assumptions** - Any inference must be explicitly noted
3. **Maintain traceability** - Every output must reference the source requirement
4. **Be auditable** - A judge must be able to follow the validation logic
5. **Remain technology-agnostic** - Focus on WHAT and WHY, never HOW

---

## Execution Flow

### Step 1: Capture Requirement Input

```
📥 **Requirement Received**

**Source**: [User input / Feature request / Change request]
**Verbatim**: "[Exact user input quoted here]"
**Context**: [Any relevant context provided]
```

### Step 2: Completeness Assessment

Evaluate against the completeness checklist:

```
📋 **Completeness Check**

| Element | Status | Notes |
|---------|--------|-------|
| User Intent | ✓/✗/⚠ | [Assessment] |
| Success Criteria | ✓/✗/⚠ | [Assessment] |
| Scope Boundaries | ✓/✗/⚠ | [Assessment] |
| User Context | ✓/✗/⚠ | [Assessment] |
| Constraints | ✓/✗/⚠ | [Assessment] |

**Legend**: ✓ Clear | ✗ Missing | ⚠ Ambiguous
```

### Step 3: Ambiguity Analysis

Identify and categorize unclear elements:

```
🔍 **Ambiguity Analysis**

**Vague Terms Found**:
- "[term]" - needs quantification or definition

**Implicit Assumptions**:
- [Assumption that needs confirmation]

**Missing Definitions**:
- [Edge case / error state / flow not defined]
```

### Step 4: Generate Clarification Questions

If ambiguities exist, generate prioritized questions:

```
❓ **Clarification Needed** (N of max 5 questions)

**Q1: [Topic]** (Priority: High/Medium)
[Clear, answerable question]

**Options**:
| Option | Description | Implication |
|--------|-------------|-------------|
| A | [Choice A] | [What this means] |
| B | [Choice B] | [What this means] |
| C | [Short answer] | [Provide your own] |

---
```

### Step 5: Validation Verdict

Provide final assessment:

```
📊 **Requirement Validation Result**

**Status**: [READY FOR SPEC | NEEDS CLARIFICATION | BLOCKED]

**Summary**:
- Completeness: [X/5 elements clear]
- Ambiguities: [N items need clarification]
- Blockers: [Any hard blockers listed]

**Recommendation**:
[Next action based on status]
```

---

## Output Formats

### When Requirements Are Ready

```
✅ **Requirements Validated**

**Feature**: [Name]
**Status**: Ready for Specification
**Completeness**: 5/5 elements clear
**Traceability ID**: REQ-[XXX]

→ Proceed to `/sp.specify` to create the formal specification
```

### When Clarification Is Needed

```
⚠️ **Clarification Required**

**Feature**: [Name]
**Status**: Pending Clarification
**Questions**: [N] questions to resolve

[Present questions using Step 4 format]

→ Answer the questions above, then re-run validation
```

### When Requirements Are Blocked

```
🚫 **Requirements Blocked**

**Feature**: [Name]
**Status**: Cannot Proceed
**Blocker**: [Critical missing information]

**Required to Unblock**:
- [Specific information needed]

→ Provide the required information to continue
```

---

## Integration Points

### With todo-domain-agent
- Receives: Domain-specific clarification requests
- Provides: Validated requirements with domain context
- Triggers: When user intent needs product owner perspective

### With todo-spec-manager
- Receives: Spec-readiness check requests
- Provides: Validation verdict and completeness assessment
- Triggers: Before any specification creation begins

### Downstream Handoffs
- `/sp.specify`: When requirements are validated and ready
- `/sp.clarify`: When specification-level clarification is needed

---

## Quality Checklist

Before completing validation, ensure:

- [ ] All user input is quoted verbatim
- [ ] No implementation details introduced
- [ ] All assumptions are documented
- [ ] Questions are answerable and impactful
- [ ] Output is judge-readable and auditable
- [ ] Traceability chain is maintained
- [ ] No features added beyond stated requirements

---

## Example Usage

**User Input**: "I want to add tasks to my todo list"

**Validation Output**:

```
📋 Completeness Check

| Element | Status | Notes |
|---------|--------|-------|
| User Intent | ✓ | Add tasks to todo list |
| Success Criteria | ⚠ | Not defined - what confirms success? |
| Scope Boundaries | ✗ | In/out of scope not stated |
| User Context | ⚠ | CLI assumed but not confirmed |
| Constraints | ✗ | No limitations mentioned |

❓ Clarification Needed (3 of max 5 questions)

Q1: Success Confirmation (Priority: High)
What should the user see after successfully adding a task?

| Option | Description | Implication |
|--------|-------------|-------------|
| A | Confirmation message | User sees "Task added" |
| B | Task ID returned | User sees "Task #1 created" |
| C | Silent success | No output on success |
| D | Short answer | Describe your preference |

[Additional questions...]

📊 Requirement Validation Result

Status: NEEDS CLARIFICATION
Summary: 2/5 elements clear, 3 ambiguities found
Recommendation: Answer the clarification questions to proceed
```

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent-native tools when possible.

1) Determine Stage
   - Stage: spec (requirement validation is pre-spec work)

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route: `history/prompts/<feature-name>/` or `history/prompts/general/` if no feature context

3) Create and Fill PHR
   - Follow standard PHR creation process per CLAUDE.md

4) Validate + report
   - Confirm PHR creation with ID, path, stage, title

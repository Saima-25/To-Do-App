# Skill: QA Test Case Design

## Skill Metadata

| Attribute | Value |
|-----------|-------|
| **Skill Name** | `qa-test-case-design` |
| **Purpose** | Design test cases from specifications without writing test code, ensuring comprehensive coverage of acceptance criteria |
| **Used By** | `qa-agent` |
| **Phase** | Post-planning / Pre-implementation |
| **Hackathon Alignment** | Judge-friendly, demonstrates thorough QA methodology |

---

## Purpose

This skill enables the QA Agent to design comprehensive test cases based on approved specifications and plans. It produces human-readable test case documentation that:

- Maps directly to acceptance criteria
- Covers positive, negative, and edge case scenarios
- Provides clear pass/fail criteria
- Serves as a contract for implementation verification
- Demonstrates professional QA thinking to hackathon judges

**Critical**: This skill designs tests conceptually. It does NOT write test code.

---

## Capabilities

### 1. Test Case Derivation
Transform requirements into structured test cases:

- One or more test cases per acceptance criterion
- Traceability from test case back to requirement
- Clear preconditions, steps, and expected results
- Unique identifiers for each test case

### 2. Test Scenario Coverage
Design tests across multiple dimensions:

| Category | Description |
|----------|-------------|
| **Happy Path** | Normal flow with valid inputs |
| **Boundary** | Edge values (min, max, limits) |
| **Negative** | Invalid inputs, error conditions |
| **Edge Cases** | Unusual but valid scenarios |
| **State-Based** | Different system states |

### 3. Test Priority Classification
Assign priority based on:

- **P0 - Critical**: Core functionality, must pass for release
- **P1 - High**: Important features, significant user impact
- **P2 - Medium**: Secondary features, moderate impact
- **P3 - Low**: Nice-to-have verification, minimal impact

### 4. Test Data Requirements
Identify data needs without creating actual data:

- Required input types and formats
- Boundary values to test
- Invalid data patterns
- State prerequisites

### 5. Coverage Matrix
Track requirement-to-test mapping:

- Every acceptance criterion has at least one test
- Gap identification for uncovered areas
- Coverage percentage calculation

---

## Constraints

### This Skill MUST NOT:

1. **Write test code** - No Python, no pytest, no unittest code
2. **Create test fixtures** - No actual test data or mocks
3. **Define test infrastructure** - No CI/CD, no test runners
4. **Implement assertions** - No assert statements or verification code
5. **Specify test frameworks** - No tool-specific syntax
6. **Make architecture decisions** - No file structures or organization

### This Skill MUST:

1. **Remain implementation-agnostic** - Tests describe behavior, not code
2. **Be human-readable** - Anyone can understand and execute manually
3. **Maintain traceability** - Every test links to a requirement
4. **Be comprehensive** - Cover positive, negative, and edge cases
5. **Be actionable** - Clear enough for developers to implement
6. **Support audit** - Judges can verify coverage completeness

---

## Execution Flow

### Step 1: Input Analysis

```
📥 **Test Design Input**

**Feature**: [Feature name]
**Spec Version**: [X.Y.Z]
**Plan Version**: [X.Y.Z]
**Acceptance Criteria Count**: [N]
**Requirements to Cover**: [List of FR-IDs]
```

### Step 2: Test Case Template

For each test case, use this structure:

```
---
## TC-[XXX]: [Test Case Title]

**Traces To**: [FR-ID, AC-ID]
**Priority**: [P0/P1/P2/P3]
**Category**: [Happy Path / Boundary / Negative / Edge Case / State]

### Preconditions
- [System state before test]
- [Required setup]

### Test Steps
1. [Action step 1]
2. [Action step 2]
3. [Action step 3]

### Expected Result
- [Observable outcome]
- [State after test]

### Pass Criteria
- [ ] [Specific verifiable condition]
- [ ] [Another condition]

### Test Data Requirements
- [Input type/format needed]
- [Boundary values if applicable]
---
```

### Step 3: Coverage Categories

Design tests for each category:

```
📊 **Test Coverage by Category**

### Happy Path Tests
| TC-ID | Title | Traces To | Priority |
|-------|-------|-----------|----------|
| TC-001 | [Title] | FR-001, AC-001 | P0 |

### Boundary Tests
| TC-ID | Title | Boundary Tested | Priority |
|-------|-------|-----------------|----------|
| TC-010 | [Title] | [min/max value] | P1 |

### Negative Tests
| TC-ID | Title | Error Condition | Priority |
|-------|-------|-----------------|----------|
| TC-020 | [Title] | [Invalid input] | P1 |

### Edge Case Tests
| TC-ID | Title | Scenario | Priority |
|-------|-------|----------|----------|
| TC-030 | [Title] | [Unusual case] | P2 |
```

### Step 4: Traceability Matrix

```
📋 **Requirement Coverage Matrix**

| Req ID | Requirement | Test Cases | Coverage |
|--------|-------------|------------|----------|
| FR-001 | [Summary] | TC-001, TC-010, TC-020 | ✓ Full |
| FR-002 | [Summary] | TC-002 | ⚠ Partial |
| FR-003 | [Summary] | - | ✗ None |

**Coverage Summary**:
- Total Requirements: [N]
- Fully Covered: [X]
- Partially Covered: [Y]
- Not Covered: [Z]
- **Coverage Percentage**: [X%]
```

### Step 5: Test Design Summary

```
📊 **Test Case Design Result**

**Feature**: [Name]
**Total Test Cases Designed**: [N]

**By Priority**:
- P0 (Critical): [N] tests
- P1 (High): [N] tests
- P2 (Medium): [N] tests
- P3 (Low): [N] tests

**By Category**:
- Happy Path: [N] tests
- Boundary: [N] tests
- Negative: [N] tests
- Edge Cases: [N] tests

**Coverage**: [X]% of requirements covered

**Gaps Identified**:
- [Any requirements without tests]

**Recommendation**:
[Ready for implementation / Needs additional design]
```

---

## Output Formats

### Test Case Document Structure

```markdown
# Test Cases: [Feature Name]

**Version**: 1.0
**Created**: [Date]
**Spec Reference**: specs/[feature]/spec.md
**Plan Reference**: specs/[feature]/plan.md

## Summary
- Total Test Cases: [N]
- Coverage: [X]%

## Test Cases

[Individual test cases using template from Step 2]

## Coverage Matrix

[Matrix from Step 4]

## Test Data Requirements Summary

| Data Type | Valid Examples | Invalid Examples | Boundaries |
|-----------|----------------|------------------|------------|
| [Type] | [Examples] | [Examples] | [Min/Max] |
```

---

## Integration Points

### Upstream
- Receives approved specs from `qa-spec-review`
- Uses plan artifacts from `/sp.plan`

### Downstream
- Test designs inform `/sp.tasks` for implementation
- Provides verification checklist for `/sp.implement`

### Collaboration
- Consults `todo-domain-agent` for user behavior expectations
- Aligns with `todo-spec-manager` for requirement traceability

---

## Example Test Case

```
---
## TC-001: Add Task with Valid Title

**Traces To**: FR-001 (Add Task), AC-001 (Task Creation)
**Priority**: P0
**Category**: Happy Path

### Preconditions
- Todo application is running
- No existing tasks in the system

### Test Steps
1. Execute the add task command with a valid title "Buy groceries"
2. Observe the system response
3. List all tasks

### Expected Result
- System confirms task was added successfully
- Task appears in the task list with the provided title
- Task has a unique identifier assigned

### Pass Criteria
- [ ] Confirmation message is displayed
- [ ] Task is retrievable via list command
- [ ] Task title matches input exactly

### Test Data Requirements
- Valid title: 1-100 characters, alphanumeric with spaces
- Example: "Buy groceries", "Call mom", "Finish project"
---
```

---

## Quality Checklist

Before completing test design, ensure:

- [ ] Every acceptance criterion has at least one test case
- [ ] Happy path, boundary, negative, and edge cases covered
- [ ] All test cases have unique identifiers
- [ ] Traceability to requirements is complete
- [ ] Priority is assigned to every test
- [ ] Expected results are specific and verifiable
- [ ] No test code or implementation details included
- [ ] Test cases are human-executable
- [ ] Coverage matrix shows no gaps
- [ ] Output is judge-readable and auditable

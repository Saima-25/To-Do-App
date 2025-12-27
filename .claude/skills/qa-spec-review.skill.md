# Skill: QA Spec Review

## Skill Metadata

| Attribute | Value |
|-----------|-------|
| **Skill Name** | `qa-spec-review` |
| **Purpose** | Review specifications for testability, completeness, and acceptance criteria quality before planning begins |
| **Used By** | `qa-agent` |
| **Phase** | Post-specification / Pre-planning |
| **Hackathon Alignment** | Judge-friendly, ensures testable requirements |

---

## Purpose

This skill enables the QA Agent to review specifications from a testing perspective, ensuring that every requirement is testable, every acceptance criterion is verifiable, and no ambiguities exist that would prevent effective test case creation.

The QA Agent uses this skill to:
- Validate specs are test-ready before planning proceeds
- Identify requirements that cannot be objectively verified
- Ensure acceptance criteria are specific and measurable
- Flag missing error scenarios and edge cases
- Confirm the spec supports both positive and negative testing

---

## Capabilities

### 1. Testability Assessment
Evaluate each requirement for testability:

| Criterion | Assessment |
|-----------|------------|
| **Measurable** | Can the outcome be objectively measured? |
| **Observable** | Can the behavior be observed by a tester? |
| **Repeatable** | Will the same input produce the same output? |
| **Bounded** | Are the conditions and scope clearly defined? |

### 2. Acceptance Criteria Validation
For each acceptance criterion, verify:

- [ ] Specific: No vague terms ("fast", "user-friendly", "robust")
- [ ] Measurable: Contains quantifiable success indicators
- [ ] Achievable: Can be implemented and tested within scope
- [ ] Relevant: Directly tied to user value
- [ ] Testable: Can be verified with a clear pass/fail result

### 3. Edge Case Coverage Analysis
Identify missing test scenarios:

- Empty states (no data, first-time use)
- Boundary conditions (min/max values, character limits)
- Error states (invalid input, missing required fields)
- Concurrency scenarios (if applicable)
- State transitions (valid and invalid)

### 4. Negative Testing Gaps
Ensure the spec defines what should NOT happen:

- Invalid input handling
- Unauthorized access attempts
- Malformed data processing
- Resource exhaustion scenarios
- Recovery from failure states

### 5. Test Strategy Recommendations
Provide guidance on testing approach without implementation:

- Suggested test categories (unit, integration, e2e)
- Critical paths requiring thorough coverage
- Risk areas needing exploratory testing
- Regression considerations

---

## Constraints

### This Skill MUST NOT:

1. **Write test code** - No test implementations, no test scripts
2. **Define test frameworks** - No pytest, unittest, or tool recommendations
3. **Create test data** - No fixtures, mocks, or sample data
4. **Specify test architecture** - No folder structures or organization
5. **Modify specifications** - Only review and recommend changes
6. **Make implementation assumptions** - Focus on behavior, not code

### This Skill MUST:

1. **Focus on behavior verification** - What can be observed and measured
2. **Remain technology-agnostic** - No framework or language specifics
3. **Preserve requirement traceability** - Link findings to specific requirements
4. **Be actionable** - Every finding must have a clear resolution path
5. **Support audit readiness** - Judges must see thorough QA thinking

---

## Execution Flow

### Step 1: Spec Intake

```
📥 **Spec Under Review**

**Feature**: [Feature name from spec]
**Version**: [Spec version]
**Location**: [Path to spec file]
**Requirements Count**: [Number of functional requirements]
**Acceptance Criteria Count**: [Number of AC items]
```

### Step 2: Testability Matrix

```
📊 **Testability Assessment**

| Req ID | Requirement Summary | Measurable | Observable | Repeatable | Bounded | Verdict |
|--------|---------------------|------------|------------|------------|---------|---------|
| FR-001 | [Summary] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | PASS/FAIL |
| FR-002 | [Summary] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | PASS/FAIL |

**Testability Score**: [X/Y requirements testable]
```

### Step 3: Acceptance Criteria Review

```
📋 **Acceptance Criteria Quality**

**AC-001**: "[Criterion text]"
- Specific: ✓/✗ - [Notes]
- Measurable: ✓/✗ - [Notes]
- Testable: ✓/✗ - [Notes]
- **Verdict**: PASS / NEEDS REFINEMENT

**Recommended Revision** (if needed):
> [Improved criterion text]
```

### Step 4: Coverage Gap Analysis

```
🔍 **Coverage Gaps Identified**

**Missing Edge Cases**:
1. [Edge case not covered]
2. [Another gap]

**Missing Error Scenarios**:
1. [Error condition not specified]
2. [Another error scenario]

**Missing Boundary Tests**:
1. [Boundary not defined]

**Negative Testing Gaps**:
1. [What-should-not-happen not specified]
```

### Step 5: QA Verdict

```
📊 **QA Spec Review Result**

**Status**: [APPROVED FOR PLANNING | NEEDS REVISION | BLOCKED]

**Summary**:
- Testability: [X/Y requirements testable]
- AC Quality: [X/Y criteria meet standards]
- Coverage Gaps: [N items need attention]
- Blockers: [Critical issues if any]

**Required Actions** (if not approved):
1. [Action item with specific requirement reference]
2. [Another action]

**Recommendation**:
[Next step based on status]
```

---

## Output Formats

### When Spec Is Approved

```
✅ **QA Spec Review: APPROVED**

**Feature**: [Name]
**Version**: [X.Y.Z]
**Testability Score**: [X/Y] requirements testable
**AC Quality**: All criteria meet testability standards

**QA Notes**:
- [Any observations for planning phase]

→ Spec is ready for `/sp.plan`
```

### When Revision Is Needed

```
⚠️ **QA Spec Review: NEEDS REVISION**

**Feature**: [Name]
**Issues Found**: [N] items require attention

**Required Revisions**:
| Priority | Req ID | Issue | Suggested Fix |
|----------|--------|-------|---------------|
| High | FR-001 | [Issue] | [Fix] |
| Medium | AC-003 | [Issue] | [Fix] |

→ Address revisions, then re-run QA review
```

### When Blocked

```
🚫 **QA Spec Review: BLOCKED**

**Feature**: [Name]
**Critical Issue**: [Fundamental testability problem]

**Blocker Details**:
[Explanation of why testing is impossible with current spec]

**Required to Unblock**:
[Specific changes needed]

→ Spec cannot proceed to planning until resolved
```

---

## Integration Points

### Upstream
- Receives specs from `todo-spec-manager` after approval
- May be triggered by `/sp.specify` completion

### Downstream
- Provides QA approval for `/sp.plan` to proceed
- Findings feed into `/sp.tasks` for test task creation

### Collaboration
- Consults `todo-domain-agent` for expected user behavior
- Aligns with `hackathon-judge-reviewer` for audit readiness

---

## Quality Checklist

Before completing review, ensure:

- [ ] Every requirement has been assessed for testability
- [ ] All acceptance criteria have been evaluated
- [ ] Edge cases have been identified
- [ ] Error scenarios have been documented
- [ ] Findings are traceable to specific requirements
- [ ] Recommendations are actionable and specific
- [ ] No implementation details have been introduced
- [ ] Output is judge-readable

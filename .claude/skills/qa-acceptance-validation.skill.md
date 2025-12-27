# Skill: QA Acceptance Validation

## Skill Metadata

| Attribute | Value |
|-----------|-------|
| **Skill Name** | `qa-acceptance-validation` |
| **Purpose** | Validate completed implementation against acceptance criteria and test cases without executing tests |
| **Used By** | `qa-agent` |
| **Phase** | Post-implementation / Pre-release |
| **Hackathon Alignment** | Judge-friendly, demonstrates verification discipline |

---

## Purpose

This skill enables the QA Agent to perform acceptance validation of completed work by:

- Verifying implementation artifacts exist for each requirement
- Checking that acceptance criteria can be satisfied
- Validating test coverage is present and adequate
- Confirming the feature is demo-ready for judges
- Producing an audit trail of verification activities

**Critical**: This skill validates and documents. It does NOT execute tests or write code.

---

## Capabilities

### 1. Implementation Artifact Verification
Confirm required deliverables exist:

- [ ] Code files implement the specified behavior
- [ ] Test files exist for test cases designed
- [ ] Documentation matches implementation
- [ ] No orphaned or missing artifacts

### 2. Acceptance Criteria Trace
For each acceptance criterion, verify:

| Check | Description |
|-------|-------------|
| **Implemented** | Code exists that addresses this criterion |
| **Tested** | Test case exists that verifies this criterion |
| **Documented** | Behavior is documented if required |
| **Demonstrable** | Can be shown to judges |

### 3. Test Coverage Confirmation
Validate test implementation:

- Designed test cases have corresponding test code
- Test files are properly located
- Tests are runnable (syntax valid, imports resolved)
- Coverage gaps are identified

### 4. Demo Readiness Assessment
Evaluate judge presentation readiness:

- Feature is end-to-end functional
- Happy path works completely
- Error handling is graceful
- No obvious defects visible

### 5. Sign-off Documentation
Produce formal validation record:

- Acceptance criteria status (Pass/Fail/Blocked)
- Issues discovered with severity
- Recommendations for release
- Audit trail for traceability

---

## Constraints

### This Skill MUST NOT:

1. **Execute tests** - No running pytest, unittest, or any test suite
2. **Write or modify code** - No implementation changes
3. **Fix defects** - Only report, never repair
4. **Make release decisions** - Only recommend, stakeholders decide
5. **Skip validation steps** - Every criterion must be checked
6. **Assume behavior** - Verify through artifact inspection

### This Skill MUST:

1. **Inspect thoroughly** - Check every acceptance criterion
2. **Document findings** - Every check has a recorded result
3. **Maintain objectivity** - Report facts, not opinions
4. **Preserve traceability** - Link findings to requirements
5. **Be auditable** - Judges can follow the validation logic
6. **Recommend clearly** - Unambiguous go/no-go guidance

---

## Execution Flow

### Step 1: Validation Scope

```
📥 **Acceptance Validation Scope**

**Feature**: [Feature name]
**Spec Version**: [X.Y.Z]
**Implementation Branch**: [Branch name]
**Validation Date**: [ISO Date]

**Artifacts to Validate**:
- Spec: specs/[feature]/spec.md
- Plan: specs/[feature]/plan.md
- Tasks: specs/[feature]/tasks.md
- Test Cases: specs/[feature]/test-cases.md
- Implementation: [Code locations]
- Tests: [Test file locations]
```

### Step 2: Acceptance Criteria Validation

For each acceptance criterion:

```
📋 **Acceptance Criterion Validation**

### AC-001: [Criterion Text]

**Traces To**: FR-001
**Priority**: [P0/P1/P2/P3]

| Check | Status | Evidence |
|-------|--------|----------|
| Implemented | ✓/✗/⚠ | [File:line or finding] |
| Tested | ✓/✗/⚠ | [Test file:test name] |
| Documented | ✓/✗/N/A | [Doc reference] |
| Demonstrable | ✓/✗/⚠ | [Demo capability] |

**Criterion Status**: PASS / FAIL / BLOCKED
**Notes**: [Any observations]
```

### Step 3: Test Coverage Verification

```
📊 **Test Coverage Verification**

| Test Case ID | Test Case Title | Test File Exists | Test Implemented |
|--------------|-----------------|------------------|------------------|
| TC-001 | [Title] | ✓/✗ | ✓/✗/Partial |
| TC-002 | [Title] | ✓/✗ | ✓/✗/Partial |

**Coverage Summary**:
- Designed Test Cases: [N]
- Implemented Tests: [X]
- Partial Implementation: [Y]
- Missing Tests: [Z]
- **Test Coverage**: [X%]
```

### Step 4: Issue Log

```
🐛 **Issues Discovered**

| Issue ID | Severity | AC/TC Reference | Description | Status |
|----------|----------|-----------------|-------------|--------|
| ISS-001 | Critical | AC-001 | [Description] | Open |
| ISS-002 | Major | TC-005 | [Description] | Open |
| ISS-003 | Minor | AC-003 | [Description] | Open |

**Severity Definitions**:
- **Critical**: Blocks acceptance, must fix before release
- **Major**: Significant impact, should fix before release
- **Minor**: Low impact, can defer to future iteration
- **Cosmetic**: No functional impact, nice to fix
```

### Step 5: Demo Readiness Check

```
🎯 **Demo Readiness Assessment**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Core functionality works | ✓/✗ | [Details] |
| Happy path is smooth | ✓/✗ | [Details] |
| Error messages are clear | ✓/✗ | [Details] |
| No crashes or hangs | ✓/✗ | [Details] |
| Performance acceptable | ✓/✗ | [Details] |
| Edge cases handled gracefully | ✓/✗ | [Details] |

**Demo Readiness**: READY / NOT READY / CONDITIONAL
**Conditions** (if applicable): [What must be resolved]
```

### Step 6: Validation Verdict

```
📊 **Acceptance Validation Result**

**Feature**: [Name]
**Validation Date**: [ISO Date]
**Validator**: QA Agent

**Summary**:
| Metric | Value |
|--------|-------|
| Acceptance Criteria | [X/Y] passing |
| Test Coverage | [N%] |
| Critical Issues | [N] |
| Major Issues | [N] |
| Minor Issues | [N] |

**Verdict**: ACCEPTED / REJECTED / CONDITIONAL ACCEPTANCE

**Recommendation**:
[Clear statement on release readiness with required actions if any]
```

---

## Output Formats

### Acceptance Report Document

```markdown
# Acceptance Validation Report: [Feature Name]

**Version**: 1.0
**Date**: [ISO Date]
**Feature Spec**: specs/[feature]/spec.md v[X.Y.Z]
**Validator**: QA Agent

## Executive Summary

**Verdict**: [ACCEPTED / REJECTED / CONDITIONAL]
**Acceptance Criteria**: [X/Y] passing ([N%])
**Test Coverage**: [N%]
**Open Issues**: [Critical: N, Major: N, Minor: N]

## Recommendation

[1-2 sentence recommendation for stakeholders]

## Detailed Findings

### Acceptance Criteria Status
[Table of all AC with status]

### Test Coverage
[Coverage matrix]

### Issues
[Issue log with details]

### Demo Readiness
[Assessment table]

## Sign-off

- [ ] All critical issues resolved
- [ ] All acceptance criteria passing
- [ ] Test coverage meets minimum threshold
- [ ] Demo readiness confirmed
- [ ] Ready for judge presentation

**Validated By**: QA Agent
**Date**: [ISO Date]
```

---

## Integration Points

### Upstream
- Receives completed implementation from `/sp.implement`
- Uses test cases from `qa-test-case-design`
- References spec from `todo-spec-manager`

### Downstream
- Provides validation report for release decision
- Feeds into `hackathon-judge-reviewer` for final audit
- Issues inform future `/sp.tasks` if rework needed

### Collaboration
- Consults `todo-domain-agent` for expected behavior validation
- Aligns with `hackathon-judge-reviewer` for presentation readiness

---

## Validation Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| **ACCEPTED** | All criteria pass, no critical issues | Release approved |
| **REJECTED** | Critical failures or blocking issues | Rework required |
| **CONDITIONAL** | Minor issues, acceptable with caveats | Release with documented limitations |
| **BLOCKED** | Cannot validate, missing artifacts | Resolve blockers first |

---

## Quality Checklist

Before completing validation, ensure:

- [ ] Every acceptance criterion has been checked
- [ ] All test cases have been verified for implementation
- [ ] Issues are logged with proper severity
- [ ] Demo readiness has been assessed
- [ ] Verdict is clear and justified
- [ ] Recommendations are actionable
- [ ] Traceability chain is complete
- [ ] Report is judge-readable and auditable
- [ ] No assumptions made without evidence
- [ ] Sign-off checklist is complete

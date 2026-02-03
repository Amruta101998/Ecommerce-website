# QA Documentation Validation Test Suite

## Overview

This test suite validates alignment between **JIRA** and **Confluence** requirements, simulating real-world QA documentation drift scenarios. It identifies requirements that are:

- ✅ **MATCH**: Fully aligned between JIRA and Confluence
- ⚠️ **PARTIAL_MATCH**: Incomplete or vague alignment
- ❌ **CONFLICT**: Direct contradictions between sources

## Why This Matters

Documentation misalignment is a common source of bugs and rework:
- Development teams implement based on different specifications
- QA tests against requirements that don't match implementation
- Deployments fail due to unmet acceptance criteria
- Security vulnerabilities slip through due to conflicting policies

This tool automates detection of these issues.

## Quick Start

### Prerequisites
- Python 3.7+
- No external dependencies required (uses only standard library)

### Run Validation

```bash
# Navigate to the test directory
cd qa_confluence_jira_test

# Run validation
python3 test_validation.py

# View detailed report
cat validation_report.txt
```

### Expected Output

```
======================================================================
QA DOCUMENTATION VALIDATION REPORT
======================================================================

JIRA Reference:
  https://bito.atlassian.net/browse/BITO-12071

Confluence Reference:
  https://bito.atlassian.net/wiki/spaces/EN/pages/1132003418/Quality+Assurance+QA

REQUIREMENT VALIDATION RESULTS
----------------------------------------------------------------------

✔ REQ-001: Login Validation – MATCH
   Both JIRA and Confluence are in complete agreement on login validation requirements.

⚠ REQ-002: Password Policy Requirements – CONFLICT
   [CRITICAL] CRITICAL SECURITY MISMATCH: JIRA requires 12-character minimum while Confluence specifies 8 characters...
   → Recommendation: Adopt JIRA's 12-character minimum requirement. Update Confluence documentation immediately.

⚠ REQ-003: API Response Performance – PARTIAL_MATCH
   JIRA provides detailed performance SLA (2 seconds, P95/P99 targets, 100 concurrent users), but Confluence only mentions 'performance testing' without specific metrics...
   → Recommendation: Update Confluence with specific performance SLA metrics from JIRA...

✔ REQ-004: Session Timeout Configuration – MATCH
   Both sources align on session timeout (30 min), warning (25 min), and extension capability...

⚠ REQ-005: Data Encryption in Transit – PARTIAL_MATCH
   Both require encryption in transit, but JIRA provides detailed specifications (TLS 1.2+, ECDHE, HSTS, certificate validation)...
   → Recommendation: Update Confluence with specific TLS version, cipher suite, and HSTS requirements from JIRA...

VALIDATION SUMMARY
----------------------------------------------------------------------
Total Requirements: 5
✔ Fully Matched: 2 (40%)
⚠ Partially Matched: 2 (40%)
✖ Conflicts: 1 (20%)

SEVERITY BREAKDOWN
Critical Issues: 1
High Priority Issues: 1

ACTION ITEMS
----------------------------------------------------------------------
CONFLICTS DETECTED - IMMEDIATE ACTION REQUIRED:
  • REQ-002: Password Policy Requirements
    → Adopt JIRA's 12-character minimum requirement. Update Confluence documentation immediately.

PARTIAL MATCHES - CLARIFICATION NEEDED:
  • REQ-003: API Response Performance
    → Update Confluence with specific performance SLA metrics from JIRA...
  • REQ-005: Data Encryption in Transit
    → Update Confluence with specific TLS version, cipher suite, and HSTS requirements from JIRA...

✔ Validation PASSED
```

## File Structure

```
qa_confluence_jira_test/
├── requirements_mapping.json      # Master requirements data (5 test cases)
├── test_validation.py             # Executable validation script
├── validation_report.txt          # Generated detailed report
└── README.md                      # This file
```

## Requirements Details

### REQ-001: Login Validation ✅ MATCH

**JIRA (BITO-12071)**
- HTTP 200 on successful authentication
- HTTP 401 for invalid credentials
- Detailed error handling

**Confluence**
- HTTP 200 for valid credentials
- HTTP 401 for invalid credentials
- Error messages for invalid credentials

**Status**: ✅ Both specifications align perfectly

---

### REQ-002: Password Policy Requirements ❌ CONFLICT

**JIRA (BITO-12071)**
- Minimum length: **12 characters** ⚠️
- Complexity: Uppercase, lowercase, numbers, special characters
- Hashing: bcrypt with salt

**Confluence**
- Minimum length: **8 characters** ⚠️
- Complexity: Letters and numbers
- Hashing: Standard encryption

**Status**: ❌ **CRITICAL CONFLICT** - Security vulnerability!

**Recommendation**: Adopt JIRA's 12-character requirement (more secure). Update Confluence immediately.

---

### REQ-003: API Response Performance ⚠️ PARTIAL_MATCH

**JIRA (BITO-12071)**
- Response time SLA: < 2 seconds
- Load test: 100 concurrent users
- P95 target: < 2000ms
- P99 target: < 3000ms

**Confluence**
- "Performance testing should be conducted"
- "Response times should be optimized"
- No specific metrics defined

**Status**: ⚠️ JIRA is detailed, Confluence is vague

**Recommendation**: Update Confluence with specific SLA metrics from JIRA

---

### REQ-004: Session Timeout Configuration ✅ MATCH

**JIRA (BITO-12071)**
- Timeout: 30 minutes of inactivity
- Warning: 25 minutes
- Extension: 15 minutes per click
- Storage: Secure session storage

**Confluence**
- Timeout: 30 minutes
- Warning: 25 minutes
- Extension: Available

**Status**: ✅ Specifications align (minor implementation detail difference)

---

### REQ-005: Data Encryption in Transit ⚠️ PARTIAL_MATCH

**JIRA (BITO-12071)**
- Protocol: TLS 1.2 or higher
- Certificate validation: Required
- Cipher suites: ECDHE required
- HSTS: max-age 31536000 seconds

**Confluence**
- Protocol: HTTPS (version not specified)
- Certificate validation: Not mentioned
- Cipher suites: Not specified

**Status**: ⚠️ JIRA provides detailed security specifications, Confluence is incomplete

**Recommendation**: Update Confluence with JIRA's detailed TLS and security requirements

## Integration Guide

### With JIRA

1. Link this repository to JIRA issue **BITO-12071**
2. Reference this test suite in the issue description
3. Run validation as part of QA acceptance criteria
4. Track conflicts as sub-tasks

### With Confluence

1. Link to this repository from the QA documentation page
2. Use validation results to update documentation
3. Schedule quarterly documentation audits
4. Cross-reference JIRA requirements

### With CI/CD Pipeline

```yaml
# Example GitHub Actions workflow
name: QA Documentation Validation

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: cd qa_confluence_jira_test && python3 test_validation.py
```

Exit codes:
- `0` = All requirements aligned (success)
- `1` = Conflicts detected (failure)

## Real-World Use Cases

### Scenario 1: Pre-Sprint Planning
- Run validation before sprint starts
- Identify conflicting requirements
- Resolve in sprint planning meeting
- Update documentation before development begins

### Scenario 2: Documentation Audit
- Quarterly validation of all requirements
- Track documentation drift over time
- Update Confluence based on actual implementation
- Prevent security policy violations

### Scenario 3: Onboarding
- New QA engineers run validation
- Understand known documentation gaps
- Learn what to verify during testing
- Know which requirements need clarification

### Scenario 4: Release Verification
- Before release, validate requirements alignment
- Ensure QA tested against correct specifications
- Confirm implementation matches JIRA requirements
- Document any deviations for release notes

## Best Practices

### For QA Teams
1. ✅ Run validation before test case creation
2. ✅ Use JIRA requirements as source of truth
3. ✅ Flag documentation mismatches immediately
4. ✅ Request Confluence updates before testing

### For Development Teams
1. ✅ Check validation results before implementation
2. ✅ Implement to JIRA specifications (source of truth)
3. ✅ Flag any ambiguities during implementation
4. ✅ Verify requirements with QA before coding

### For Technical Leads
1. ✅ Review validation results in sprint retrospectives
2. ✅ Track documentation debt like technical debt
3. ✅ Allocate time for documentation updates
4. ✅ Make JIRA source of truth explicit in process

## Troubleshooting

### Script fails with "FileNotFoundError"
- Ensure `requirements_mapping.json` exists in same directory
- Run script from `qa_confluence_jira_test/` directory

### Script fails with "JSONDecodeError"
- Validate JSON syntax: `python3 -m json.tool requirements_mapping.json`
- Check for trailing commas or missing quotes

### No output generated
- Check Python version: `python3 --version` (requires 3.7+)
- Verify file permissions: `chmod +x test_validation.py`

### Colors not displaying
- Some terminals don't support ANSI codes
- Output is still valid, just without colors

## Extension Points

### Adding New Requirements

Edit `requirements_mapping.json`:

```json
{
  "id": "REQ-006",
  "category": "Logging",
  "name": "Error Logging",
  "jira_specification": {...},
  "confluence_specification": {...},
  "alignment_status": "MATCH|PARTIAL_MATCH|CONFLICT",
  "confidence": 95,
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "notes": "...",
  "recommendation": "..."
}
```

### Customizing Validation Logic

Edit `test_validation.py`:

```python
class QADocumentationValidator:
    def validate(self) -> List[ValidationResult]:
        # Add custom validation logic here
        pass
```

### Integrating with External Tools

```python
# Example: Send validation results to Slack
import requests

validator = QADocumentationValidator()
validator.validate()

for result in validator.results:
    if result.status == AlignmentStatus.CONFLICT:
        requests.post(SLACK_WEBHOOK, json={
            "text": f"⚠️ {result.name}: {result.status.value}"
        })
```

## References

- **JIRA Issue**: https://bito.atlassian.net/browse/BITO-12071
- **Confluence Page**: https://bito.atlassian.net/wiki/spaces/EN/pages/1132003418/Quality+Assurance+QA
- **Repository**: https://github.com/Amruta101998/Ecommerce-website

## Contributing

Found a documentation mismatch? Have suggestions?

1. Create an issue in JIRA (BITO-12071)
2. Update `requirements_mapping.json`
3. Run validation: `python3 test_validation.py`
4. Submit PR with changes

## License

Internal use only. Part of QA automation suite.

---

**Last Updated**: 2026-02-03  
**Version**: 1.0.0  
**Maintained By**: QA Automation Team

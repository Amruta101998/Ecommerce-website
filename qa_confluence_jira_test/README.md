# QA Documentation Validation Test Suite

## Overview

This test suite validates alignment between **JIRA** and **Confluence** requirements, simulating real-world QA documentation drift scenarios. It identifies 10 test cases across multiple categories with various alignment statuses and conflict types.

### Alignment Status
- ✅ **MATCH**: Fully aligned between JIRA and Confluence
- ⚠️ **PARTIAL_MATCH**: Incomplete or vague alignment  
- ❌ **CONFLICT**: Direct contradictions between sources

### Conflict Types
- **JIRA_UPDATED_CONFLUENCE_OUTDATED**: JIRA has new requirements but Confluence hasn't been updated
- **CONFLUENCE_UPDATED_JIRA_OUTDATED**: Confluence has new requirements but JIRA hasn't been updated
- **JIRA_MORE_STRICT_THAN_CONFLUENCE**: JIRA enforces stricter standards than Confluence
- **JIRA_vs_CONFLUENCE_PHILOSOPHY_MISMATCH**: Fundamental disagreement on approach/architecture
- **JIRA_REQUIRES_CONFLUENCE_FORBIDS**: Complete contradiction (one requires, other forbids)
- **SECURITY_MISMATCH**: Security vulnerability due to misalignment

## Why This Matters

Documentation misalignment is a common source of bugs and rework:
- Development teams implement based on different specifications
- QA tests against requirements that don't match implementation
- Deployments fail due to unmet acceptance criteria
- **Security vulnerabilities slip through due to conflicting policies**

This tool automates detection of these critical issues.

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

## Test Cases (10 Total)

### Current Results: 60% Conflict Rate ⚠️

| # | Category | Requirement | Status | Severity | Notes |
|---|----------|-------------|--------|----------|-------|
| 1 | Authentication | Login Validation | ✅ MATCH | - | Fully aligned |
| 2 | Security | Password Policy | ❌ CONFLICT | CRITICAL | JIRA: 12 chars / Confluence: 8 chars |
| 3 | Performance | API Response Performance | ⚠️ PARTIAL | HIGH | JIRA detailed, Confluence vague |
| 4 | Configuration | Session Timeout | ✅ MATCH | - | Fully aligned |
| 5 | Security | Data Encryption in Transit | ⚠️ PARTIAL | MEDIUM | JIRA detailed (TLS 1.2+), Confluence basic (HTTPS) |
| 6 | Database | Connection Pooling | ❌ CONFLICT | CRITICAL | JIRA updated (HikariCP), Confluence outdated (C3P0) |
| 7 | Logging | Application Logging | ❌ CONFLICT | HIGH | JIRA: File-based / Confluence: ELK stack |
| 8 | Testing | Code Coverage | ❌ CONFLICT | HIGH | JIRA: 75% min / Confluence: 60% min |
| 9 | Deployment | Deployment Process | ❌ CONFLICT | CRITICAL | JIRA: Conservative / Confluence: Continuous |
| 10 | API | Rate Limiting | ❌ CONFLICT | CRITICAL | JIRA: Required / Confluence: Not required |

## Test Case Details

### REQ-001: Login Validation ✅ MATCH
- **JIRA**: HTTP 200 on success, 401 on failure
- **Confluence**: HTTP 200 on success, 401 on failure
- **Status**: Fully aligned

### REQ-002: Password Policy ❌ CONFLICT (CRITICAL)
- **JIRA**: Minimum 12 characters, bcrypt hashing
- **Confluence**: Minimum 8 characters, standard encryption
- **Issue**: Security vulnerability - weaker requirements in Confluence
- **Action**: Adopt JIRA's 12-character minimum

### REQ-003: API Performance ⚠️ PARTIAL_MATCH
- **JIRA**: 2-second SLA, P95 < 2000ms, P99 < 3000ms, 100 concurrent users
- **Confluence**: "Performance testing should be conducted"
- **Issue**: JIRA is specific, Confluence is vague
- **Action**: Update Confluence with JIRA's metrics

### REQ-004: Session Timeout ✅ MATCH
- **JIRA**: 30-minute timeout, 25-minute warning, 15-minute extension
- **Confluence**: 30-minute timeout, 25-minute warning
- **Status**: Fully aligned on core requirements

### REQ-005: Data Encryption ⚠️ PARTIAL_MATCH
- **JIRA**: TLS 1.2+, ECDHE, HSTS, certificate validation
- **Confluence**: HTTPS (version not specified)
- **Issue**: JIRA detailed, Confluence lacks specifics
- **Action**: Update Confluence with TLS requirements

### REQ-006: Database Connection Pooling ❌ CONFLICT (CRITICAL)
- **JIRA** (Updated 2026-02-04): HikariCP, min=20, max=100, 30s timeout
- **Confluence** (Outdated 2025-11-15): C3P0, min=10, max=50
- **Issue**: JIRA recently updated but Confluence not synchronized
- **Type**: JIRA_UPDATED_CONFLUENCE_OUTDATED
- **Action**: URGENT - Migrate to HikariCP, update pool sizes

### REQ-007: Application Logging ❌ CONFLICT (HIGH)
- **JIRA**: File-based, 24-hour rotation, INFO level, 30-day retention
- **Confluence** (Updated 2026-02-01): ELK stack, DEBUG level, 90-day retention
- **Issue**: Two completely different architectures
- **Type**: CONFLUENCE_UPDATED_JIRA_OUTDATED
- **Action**: Alignment meeting needed to decide on architecture

### REQ-008: Code Coverage ❌ CONFLICT (HIGH)
- **JIRA**: 75% minimum, 100% for critical paths, JaCoCo/Istanbul
- **Confluence**: 60% minimum, optional reports, any tool
- **Issue**: JIRA stricter standards not reflected in Confluence
- **Type**: JIRA_MORE_STRICT_THAN_CONFLUENCE
- **Action**: Adopt JIRA's stricter standards

### REQ-009: Deployment Process ❌ CONFLICT (CRITICAL)
- **JIRA**: Conservative (2x/week, scheduled window, blue-green)
- **Confluence** (Updated 2026-02-01): Aggressive (continuous, any time, canary)
- **Issue**: Fundamental philosophical mismatch
- **Type**: JIRA_vs_CONFLUENCE_PHILOSOPHY_MISMATCH
- **Action**: Executive decision required on deployment cadence

### REQ-010: API Rate Limiting ❌ CONFLICT (CRITICAL)
- **JIRA**: REQUIRED (1000 req/min, 100 burst/sec)
- **Confluence**: NOT REQUIRED
- **Issue**: Complete contradiction - security vulnerability if Confluence followed
- **Type**: JIRA_REQUIRES_CONFLUENCE_FORBIDS
- **Action**: IMMEDIATE - Implement rate limiting, update Confluence

## JIRA & Confluence Links

- **JIRA Issue**: https://bito.atlassian.net/browse/BITO-12071
- **Confluence Page**: https://bito.atlassian.net/wiki/spaces/EN/pages/1132003418/Quality+Assurance+QA

## File Structure

```
qa_confluence_jira_test/
├── requirements_mapping.json    # Master requirements data (10 test cases)
├── test_validation.py           # Validation script (executable)
├── validation_report.txt        # Generated detailed report
└── README.md                    # This file
```

## How to Use

### 1. Run Validation
```bash
python3 test_validation.py
```

**Output includes:**
- Color-coded validation results (✔ ⚠ ✖)
- Severity breakdown (CRITICAL, HIGH, MEDIUM)
- Conflict type breakdown
- Action items grouped by conflict type
- Exit code for CI/CD integration

### 2. Review Detailed Report
```bash
cat validation_report.txt
```

### 3. Resolve Conflicts

For each conflict, follow these steps:

1. **Identify the conflict type** (shown in validation output)
2. **Assess severity** (CRITICAL > HIGH > MEDIUM)
3. **Make decision** (adopt JIRA spec or Confluence spec)
4. **Update documentation** (JIRA and/or Confluence)
5. **Notify team** (development, QA, DevOps)
6. **Update CI/CD** (enforce new requirements)
7. **Re-run validation** (confirm alignment)

## Real-World Scenarios Simulated

### Scenario 1: JIRA Updated, Confluence Outdated
**REQ-006: Database Connection Pooling**
- JIRA was updated on 2026-02-04 with new requirements
- Confluence still has old requirements from 2025-11-15
- Result: Production issues if old specs are followed

### Scenario 2: Confluence Updated, JIRA Outdated
**REQ-007: Application Logging**
- Confluence was updated on 2026-02-01 with new architecture
- JIRA owner hasn't been notified
- Result: Conflicting architectural decisions

### Scenario 3: Fundamental Philosophy Mismatch
**REQ-009: Deployment Process**
- JIRA: Conservative approach (2x/week, scheduled)
- Confluence: Aggressive approach (continuous deployment)
- Result: Team disagreement on deployment strategy

### Scenario 4: Security Vulnerability
**REQ-010: API Rate Limiting**
- JIRA requires rate limiting for security
- Confluence explicitly forbids it
- Result: API vulnerable to DDoS attacks if Confluence followed

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run QA Validation
  run: |
    cd qa_confluence_jira_test
    python3 test_validation.py
    # Script exits with code 1 if conflicts detected
```

### Exit Codes
- **0**: All requirements aligned (success)
- **1**: Conflicts detected (failure)

## Best Practices

1. **Run validation in CI/CD pipeline** - Catch misalignment early
2. **Review conflicts regularly** - Weekly or sprint-based
3. **Establish governance** - Who owns JIRA vs Confluence updates?
4. **Sync before deployment** - Ensure alignment before releases
5. **Document decisions** - Record why each conflict was resolved
6. **Automate enforcement** - Use CI/CD to enforce accepted specs

## Troubleshooting

### Issue: "Mapping file not found"
```bash
# Ensure you're in the correct directory
cd qa_confluence_jira_test
python3 test_validation.py
```

### Issue: "Invalid JSON"
```bash
# Validate JSON syntax
python3 -m json.tool requirements_mapping.json
```

### Issue: Script not executable
```bash
# Make script executable
chmod +x test_validation.py
```

## Extending the Test Suite

### Add New Requirement
Edit `requirements_mapping.json` and add to the `requirements` array:

```json
{
  "id": "REQ-011",
  "category": "New Category",
  "name": "New Requirement",
  "jira_specification": { ... },
  "confluence_specification": { ... },
  "alignment_status": "MATCH|PARTIAL_MATCH|CONFLICT",
  "severity": "CRITICAL|HIGH|MEDIUM",
  "notes": "...",
  "recommendation": "...",
  "conflict_type": "..."
}
```

Then update the summary section and re-run validation.

## Interview/Demo Notes

This test suite demonstrates:
- ✅ Real-world QA automation challenges
- ✅ Documentation management best practices
- ✅ Conflict detection and resolution
- ✅ CI/CD integration patterns
- ✅ Security vulnerability identification
- ✅ Professional Python code with type hints
- ✅ Production-ready error handling

## License

Internal tooling for QA automation and documentation validation.

## Support

For issues or questions, contact the QA automation team.

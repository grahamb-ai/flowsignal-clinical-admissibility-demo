# ASVH-HARDEN — Route Closure / Direct Bypass Failure

Date: 2026-09-19
Branch: v2-health-hardening-airp
Status: FAIL — PRESERVED

## Hostile question
Can the represented consequence be produced without passing through the single-use ExecutionGateway?

## CI evidence
GitHub Actions run: 35429972725
Head commit: 476ad9d54a80b384bef8971832c931c8f10d5124
Conclusion: FAILURE

## Finding
The legacy module-level stateless execute() path can reach the represented EPR_COMMIT_PERMITTED outcome without consulting receipt-consumption state. The reference harness therefore does not demonstrate route closure at this commit.

## Claim boundary
This finding concerns only the represented consequence surface in this reference harness. It does not establish anything about production EPR routing or physical clinical-record formation.

## Remediation requirement
No public compatibility path may independently form EPR_COMMIT_PERMITTED. Consequence formation must be structurally downstream of ExecutionGateway and its consumption store.

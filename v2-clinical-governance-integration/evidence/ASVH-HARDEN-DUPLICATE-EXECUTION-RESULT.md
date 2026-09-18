# ASVH-HARDEN — Duplicate Execution / Receipt Reuse Result

Date: 2026-09-18
Branch: v2-health-hardening-airp
Status: PASS AFTER REMEDIATION

## Preserved first result

The hostile duplicate-execution challenge initially failed in GitHub Actions. The represented gateway had no one-time receipt-consumption state, so an otherwise valid Authority Receipt could be reused.

The original failure record remains in:
`evidence/ASVH-HARDEN-DUPLICATE-EXECUTION-FAILURE.md`

## Remediation

A process-local `ExecutionGateway` now records a successfully consumed Authority Receipt token. A second attempt using the same receipt is blocked with:

`AUTHORITY_RECEIPT_ALREADY_CONSUMED`

The underlying challenge was rerun after remediation.

## CI result

GitHub Actions run: 35374744467
Head commit: 8d764a0bb4cbe1351cf4db0f9dbca1c97e0bf764
Conclusion: SUCCESS

Classification: **PASS AFTER REMEDIATION**

## What this establishes

Within this reference harness, the remediated `ExecutionGateway` prevents a second represented EPR commit using the same successfully consumed Authority Receipt.

## What this does not establish

This result does not demonstrate:
- durable consumption across process restart;
- distributed atomic consumption across multiple gateway instances;
- race-safe exactly-once behaviour under concurrency;
- physical route closure in a production EPR;
- universal non-bypassability across external clinical systems.

Those properties remain **NOT DEMONSTRATED** until separately attacked and evidenced.

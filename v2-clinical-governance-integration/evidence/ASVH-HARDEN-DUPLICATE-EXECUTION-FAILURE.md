# ASVH-HARDEN — Preserved Failure: Duplicate Execution / Receipt Reuse

Date: 2026-09-18
Branch: v2-health-hardening-airp
Status: EXPECTED RED TEST INTRODUCED

## Challenge
Can an otherwise valid Authority Receipt be reused twice against the represented EPR execution gateway without one-time consumption state?

## Expected
First exact execution may reach represented EPR_COMMIT_PERMITTED. A second execution using the same receipt must not.

## Current implementation expectation
The initial gateway implementation has no receipt-consumption store. The hostile test `test_duplicate_exact_execution_is_not_yet_prevented` is intentionally written to fail until remediation exists.

## Why preserve this
A valid action binding and a valid integrity signature do not establish single-use execution. Replay/duplicate consequence is a separate property and must be tested separately.

## Claim boundary
This failure concerns the represented harness gateway only. It is not evidence about any real EPR product or external clinical system.

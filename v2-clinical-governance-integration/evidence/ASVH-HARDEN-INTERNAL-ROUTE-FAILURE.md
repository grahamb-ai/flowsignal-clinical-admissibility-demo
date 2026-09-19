# ASVH-HARDEN — Internal Consequence Route Failure

**Status:** FAIL — PRESERVED  
**Date:** 2026-09-19  
**Branch:** `v2-health-hardening-airp`  
**Attack commit:** `bbd6e7b4995fce69f68d40652cbfc6f455624974`  
**GitHub Actions run:** `35433630872`

## Challenge

After a valid Authority Receipt has been consumed through `ExecutionGateway`, directly invoke the module-internal helper `_execute_unconsumed()` with the same valid receipt and exact bound attempt.

Required property: no route outside `ExecutionGateway` may independently form the represented consequence `EPR_COMMIT_PERMITTED`.

## Observed result

The hostile test failed:

`AssertionError: 'EPR_COMMIT_PERMITTED' == 'EPR_COMMIT_PERMITTED' : ROUTE CLOSURE FAILURE: internal helper formed represented consequence outside ExecutionGateway`

Therefore route closure is **not demonstrated** at this commit. A Python underscore/private-by-convention name is not an enforcement boundary.

## Remediation requirement

The internal validation helper must return only a non-consequence intermediate result. Only `ExecutionGateway`, after successful receipt validation, binding/current-state checks and one-time consumption claim, may map that result to `EPR_COMMIT_PERMITTED`.

## Claim boundary

This finding concerns the represented consequence path in this reference harness only. It does not establish or refute physical non-formation, universal non-bypassability, production EPR enforcement, or external-system route closure.

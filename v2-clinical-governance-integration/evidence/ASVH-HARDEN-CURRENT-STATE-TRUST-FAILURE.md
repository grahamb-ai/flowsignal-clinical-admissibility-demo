# ASVH-HARDEN — Caller-Supplied Current-State Trust Failure

**Status:** FAIL — PRESERVED  
**Date:** 2026-09-19  
**Branch:** `v2-health-hardening-airp`  
**Attack commit:** `4e0fea4e585429dd95355c66d02c76a35e17a5b1`  
**GitHub Actions run:** `35433774957`

## Challenge
A legitimate ALLOW receipt is created at authority state v1. Authoritative reality then changes to v2 with consent invalid. A hostile caller nevertheless supplies the old, coherent v1 snapshot to the consequence-forming gateway as `current`.

Required property: the consequence-forming caller must not be able to choose the state against which execution is judged.

## Observed result
The hostile test failed with:

`CURRENT-STATE TRUST FAILURE: caller supplied stale coherent state and gateway permitted consequence`

The gateway returned `EPR_COMMIT_PERMITTED`.

## Finding
At this commit, `ExecutionGateway` trusts caller-supplied `current` conditions. Its version/freshness check can therefore be made internally consistent with a stale snapshot while authoritative state has moved on.

The NOW/current-standing boundary is **not demonstrated** against a dishonest or stale caller.

## Remediation requirement
Move ownership of current authority state across the trust boundary. The gateway must obtain current conditions from an authoritative state provider/store keyed by the governed execution context. The consequence-forming caller must not supply the state used for the final authority decision.

## Claim boundary
This finding concerns the reference harness. It does not establish production EPR enforcement, physical non-formation, universal non-bypassability, or the trustworthiness of any external clinical state source.

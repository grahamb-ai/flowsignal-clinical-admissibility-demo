# ASVH-HARDEN — Restart Durability Boundary Failure

Date: 2026-09-18
Branch: v2-health-hardening-airp
Status: FAIL — PRESERVED

## Hostile question

Does the one-time Authority Receipt consumption established by the remediated in-process ExecutionGateway survive replacement/restart of that gateway?

## CI evidence

GitHub Actions run: 35383548023
Head commit: 1ca508e9893f64eeeed5d15dc35bccc6a9bd5d09
Conclusion: FAILURE

The structural verifier passed. The regression suite failed after the next-boundary hostile tests were introduced.

## Finding

The current single-use remediation stores consumed receipt tokens only in process-local memory. A newly created gateway has no knowledge of consumption performed by the previous gateway. Durable one-time consumption is therefore **NOT DEMONSTRATED** and the hostile restart test remains red.

## Boundary

This is a reference-harness finding. It does not assert a defect in any production EPR or external clinical platform.

## Next remediation target

Introduce a consumption-store interface with atomic claim semantics, then provide a durable reference implementation for the harness. Re-run the same restart test unchanged in substance. Distributed multi-node atomicity and real EPR route closure remain separate hostile boundaries.

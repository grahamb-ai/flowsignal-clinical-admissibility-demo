# ASVH-HARDEN — Route Closure / Direct Bypass Attack

Date: 2026-09-19
Branch: v2-health-hardening-airp
Status: RED TEST INTRODUCED

## Attack

1. Create a valid Authority Receipt.
2. Execute it successfully through `ExecutionGateway`, consuming the receipt.
3. Present the same receipt/action/state directly to the module-level compatibility `execute()` path.
4. Assert that a second represented EPR commit must not be permitted.

## Failure condition

If the compatibility path returns `EPR_COMMIT_PERMITTED`, the represented consequence surface is bypassable and route closure has **not** been demonstrated.

## Claim boundary

This attacks route closure only inside the reference harness. It makes no claim about a production EPR, network route, external service, or physical clinical-record commit.

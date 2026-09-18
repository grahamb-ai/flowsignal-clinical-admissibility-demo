# ASVH-HARDEN — Next Hostile Boundary

Date: 2026-09-18
Status: RED TESTS INTRODUCED

The process-local duplicate-execution remediation is now being attacked at its next boundaries:

1. **Restart durability** — consumption state must survive gateway/process replacement if durable single-use is claimed.
2. **Concurrent duplicate submission** — simultaneous attempts must not produce more than one represented commit.

Expected initial finding: restart durability is **NOT DEMONSTRATED** by the current in-memory gateway and should fail. The concurrency test is exploratory and its CI result determines the finding.

No production-EPR or distributed-system claim is made by these tests.

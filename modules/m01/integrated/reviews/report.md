# Validation for M01 integrated design

Checked 2026-11-11. Verified 4 current lesson packages, 36 topic rows and 9 lesson and synthesis outcomes. The taught-stage structure check used the exact set of approved module topic IDs.

- [technical-r1.md](technical-r1.md). Accepted with MI-T1 (minor).
- [teaching-r1.md](teaching-r1.md). Accepted.
- Repository content and task state validation passed.
- The strict plan check passed with the approved SDA-v1 verdict.
- All 51 unit tests passed using the repository virtual environment.

Initial unit-test runs selected a host Python without jsonschema for taskctl subprocesses. Setting PYTHON to the virtual environment resolved the failure. The full rerun passed.

The reviewed package remains draft pending human review.

The approved baseline hashes match this checkout's file bytes. The Git blobs use LF for the approved plan, inventory and matrix, so a checkout using those bytes may report a mismatch in the strict plan gate.

The performance row in the [current decision summary](../decision-summary-r1.md) points to the reviewed M01-L02 revision.

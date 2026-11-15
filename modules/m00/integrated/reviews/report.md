# Validation for M00 integrated design

Checked 2026-11-11. Verified 2 current lesson packages, 10 topic rows and 5 lesson and synthesis outcomes. The taught-stage structure check used the exact set of approved module topic IDs.

- [technical.md](technical.md). Accepted with M00-INT-T1 (minor).
- [teaching.md](teaching.md). Accepted.
- Repository content and task state validation passed.
- The strict plan check passed with the approved SDA-v1 verdict.
- All 51 unit tests passed using the repository virtual environment.

Initial unit-test runs selected a host Python without jsonschema for taskctl subprocesses. Setting PYTHON to the virtual environment resolved the failure. The full rerun passed.

The reviewed package remains draft pending human review.

The approved baseline hashes match this checkout's file bytes. The Git blobs use LF for the approved plan, inventory and matrix, so a checkout using those bytes may report a mismatch in the strict plan gate.

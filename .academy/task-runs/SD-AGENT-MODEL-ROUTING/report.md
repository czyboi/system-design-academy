# Agent model routing validation

User requested Sol for workflow design, architecture and PR review; Terra for implementation of clear specifications. Project parent, workflow architect, PR reviewer and technical reviewer use Sol; the default bounded subagent, spec implementer and lesson author use Terra. The shared procedure routes unclear design back to Sol and retains all quality gates. Existing course-outline task files were not touched.

- Dependencies installed: exit 0; pip reported sandbox temp-directory cleanup warnings.
- Content validator: pass (0 lessons, 10 custom agent files).
- Task state validator: pass.
- Unit tests: 50 passed, including role/model routing regression.
- Git diff --check: pass.

Role profiles are repository defaults; actual runtime may differ due to host role definitions, explicit session choices or existing sessions. Model choice is not measured token or cost savings. No content generation, publication or merge.

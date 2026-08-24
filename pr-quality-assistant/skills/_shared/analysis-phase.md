# Shared Analysis Phase

Both PR-quality personas use this order and pass each output to the next skill:

1. `requirement-analysis`: extract requirements, acceptance criteria, and open questions.
2. `change-blast-radius`: map changed and affected modules and assign a risk tier.
3. `test-analysis`: map tests to the requirements and report coverage gaps.

Do not reorder or skip these stages. The `test-sufficiency` skill consumes the `test-analysis` gap output before any conditional test generation or reporting.
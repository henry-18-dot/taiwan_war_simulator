# AI Tools (Turn-Based War Strategy)

This directory is for AI-assisted scripts:
- Battle report summaries (generate turn retrospectives from the EventLog)
- Balance checks (run batch simulations and report win rate, turn length, and resource curves)
- Configuration validation (unit parameters, terrain modifiers, and victory-condition validity)

Suggested conventions:
1. Script inputs and outputs should use JSON/CSV for easy pipeline integration.
2. All simulation scripts must support `--seed` to guarantee reproducibility.
3. Output should include a version number and parameter snapshot to make regression comparisons easier.

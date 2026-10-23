# AI-R-003 Protocol / Fixture v1.0

Status: FROZEN
Freeze date: 24 October 2026
Evaluation ID: AI-R-003
Protocol / fixture version: 1.0

## Controlled battery

T01–T15 are the fixed evaluation battery.

The controlled scope includes:

- `records/**`
- `fixture-manifest.json`
- `evaluator/evaluator-key.json`
- `evaluator/SCORING.md`
- `evaluator/scoring-ledger.csv`
- `evaluator/human-dry-audit.md`

## Freeze conditions satisfied

- T01–T15 fixture construction complete.
- Fixture manifest validated.
- Global internal-link integrity validated.
- Evaluator key validated.
- Scoring ledger validated.
- Evaluator terminology isolated from fixture evidence.
- Manifest and evaluator IDs cross-checked.
- T01–T15 human evidence review completed.
- No scored agent run has occurred before freeze.

## Immutability rule

The controlled files above must not be modified during scored evaluation.

If any controlled file requires substantive correction after this freeze,
the instrument must receive a new version and new fingerprints before
further scored runs.

Scored outputs must be stored separately from the frozen fixture/evaluator
source files.

## Scoring

15 tests × 10 points = 150 maximum points.

Dimensions per test:

- Canonical outcome: 4
- Evidence and reasoning: 3
- Boundary / trap handling: 2
- Record / provenance precision: 1

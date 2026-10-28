# AI-R-003 Run Policy

Evaluation ID: AI-R-003
Protocol / Fixture: v1.0

## Blind evaluation boundary

The evaluated agent may access only:

- the assigned test prompt;
- the HTML fixture directory associated with that test;
- normal navigation links contained within that fixture.

The evaluated agent must not access:

- `evaluator/`
- `FREEZE.md`
- `PROTOCOL-FIXTURE-v1.0.sha256`
- scoring ledgers
- evaluator keys
- human audit notes
- outputs from another evaluated system

## Output isolation

Every evaluated system receives its own run directory.

No model output may overwrite:

- fixture evidence;
- evaluator material;
- another model's response;
- baseline metadata.

## Scoring separation

Generation and scoring are separate operations.

Agent responses must be captured first.

Only after a run is sealed may the evaluator key be consulted for scoring.

## Reproducibility

Each run must record:

- evaluation ID;
- protocol version;
- frozen baseline commit;
- system/model identifier;
- run identifier;
- test ID;
- timestamp;
- raw response;
- run status.

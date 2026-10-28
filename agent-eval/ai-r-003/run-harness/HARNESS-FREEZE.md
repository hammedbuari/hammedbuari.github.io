# AI-R-003 Evaluation Harness v1.0

Status: FROZEN
Evaluation ID: AI-R-003
Protocol / Fixture: v1.0
Prompt version: v1.0
Harness version: v1.0

## Frozen scope

The pre-execution harness includes:

- blind evaluation policy;
- blind evidence packs T01–T15;
- blind prompts T01–T15;
- prompt manifest;
- blind-pack index;
- run envelope specification;
- run schema;
- run initialization tool;
- write-once response capture tool;
- run sealing tool;
- run registry.

## Execution boundary

The evaluated system receives only its assigned blind package.

Evaluator material, scoring rules, canonical answers, freeze metadata,
and outputs from other systems remain outside the execution boundary.

## Immutability rule

After this harness freeze, the frozen harness must not be substantively
modified during the scored evaluation campaign.

Any substantive harness or prompt change requires a new harness version
before additional comparable scored runs are conducted.

## Run outputs

Generated run outputs are not part of the frozen harness.

They are stored under:

`agent-eval/ai-r-003/runs/`

Each run is independently captured and sealed.

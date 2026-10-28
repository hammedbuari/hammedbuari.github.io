# AI-R-003 Run Envelope

Evaluation: AI-R-003
Protocol / Fixture: v1.0
Prompt version: v1.0

## Run states

INITIALIZED_UNSCORED
→ CAPTURING_UNSCORED
→ SEALED_UNSCORED
→ SCORED

## Rules

A run represents one system/model evaluated against T01–T15.

Each run records:

- run ID
- system ID
- provider
- model identifier
- frozen baseline commit
- execution commit
- creation timestamp
- sealing timestamp
- exact T01–T15 response bytes

Raw responses are write-once.

A response that has already been captured must never be silently
overwritten.

The evaluator key must not be consulted while responses are being
generated or captured.

A run becomes eligible for scoring only after all fifteen responses
exist and the run is sealed.

The run seal fingerprints:

- metadata.json
- response-manifest.json
- T01.txt through T15.txt

Scoring artefacts must be created separately and must never modify the
sealed raw-response artefacts.

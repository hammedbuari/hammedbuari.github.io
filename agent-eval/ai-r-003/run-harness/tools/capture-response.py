from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import sys

root = Path("agent-eval/ai-r-003")

parser = argparse.ArgumentParser()
parser.add_argument("--run-id", required=True)
parser.add_argument("--test-id", required=True)
parser.add_argument("--file")
args = parser.parse_args()

expected = {f"T{i:02d}" for i in range(1, 16)}

if args.test_id not in expected:
    raise SystemExit(f"Invalid test ID: {args.test_id}")

run_dir = root / "runs" / args.run_id
meta_path = run_dir / "metadata.json"

if not meta_path.exists():
    raise SystemExit(f"Unknown run: {args.run_id}")

meta = json.loads(meta_path.read_text())

if meta["status"] in {"SEALED_UNSCORED", "SCORED"}:
    raise SystemExit("Run is sealed; raw responses are immutable.")

target = run_dir / "responses" / f"{args.test_id}.txt"

if target.exists():
    raise SystemExit(
        f"{args.test_id} already captured; overwrite prohibited."
    )

if args.file:
    data = Path(args.file).read_bytes()
else:
    data = sys.stdin.buffer.read()

if not data:
    raise SystemExit("Empty response rejected.")

target.write_bytes(data)

response_count = len(
    list((run_dir / "responses").glob("T*.txt"))
)

meta["response_count"] = response_count
meta["status"] = "CAPTURING_UNSCORED"
meta["last_capture_at_utc"] = datetime.now(
    timezone.utc
).isoformat()

meta_path.write_text(
    json.dumps(meta, indent=2) + "\n"
)

print(
    f"PASS: {args.test_id} captured "
    f"({len(data)} bytes)."
)
print(f"Responses captured: {response_count}/15")

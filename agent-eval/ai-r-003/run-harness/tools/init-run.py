from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import re
import subprocess

repo = Path.cwd()
root = repo / "agent-eval/ai-r-003"
runs = root / "runs"

parser = argparse.ArgumentParser()
parser.add_argument("--system-id", required=True)
parser.add_argument("--provider", required=True)
parser.add_argument("--model", required=True)
parser.add_argument("--run-id")
args = parser.parse_args()

if not re.fullmatch(r"[A-Za-z0-9._-]+", args.system_id):
    raise SystemExit(
        "system-id may contain only letters, numbers, '.', '_' and '-'."
    )

now = datetime.now(timezone.utc)
stamp = now.strftime("%Y%m%dT%H%M%SZ")

run_id = args.run_id or f"air003-{stamp}-{args.system_id}"

if not re.fullmatch(r"[A-Za-z0-9._-]+", run_id):
    raise SystemExit("Invalid run-id.")

run_dir = runs / run_id

if run_dir.exists():
    raise SystemExit(f"Run already exists: {run_id}")

baseline_commit = subprocess.check_output(
    [
        "git", "log", "-1", "--format=%H", "--",
        "agent-eval/ai-r-003/PROTOCOL-FIXTURE-v1.0.sha256"
    ],
    cwd=repo,
    text=True
).strip()

execution_commit = subprocess.check_output(
    ["git", "rev-parse", "HEAD"],
    cwd=repo,
    text=True
).strip()

expected = [f"T{i:02d}" for i in range(1, 16)]

run_dir.mkdir(parents=True)
(run_dir / "responses").mkdir()

metadata = {
    "evaluation_id": "AI-R-003",
    "protocol_version": "1.0",
    "prompt_version": "1.0",
    "run_id": run_id,
    "system_id": args.system_id,
    "provider": args.provider,
    "model": args.model,
    "frozen_baseline_commit": baseline_commit,
    "execution_commit": execution_commit,
    "created_at_utc": now.isoformat(),
    "sealed_at_utc": None,
    "status": "INITIALIZED_UNSCORED",
    "expected_tests": expected,
    "response_count": 0,
    "raw_response_policy": "write-once",
    "evaluator_visibility": "forbidden-until-sealed"
}

(run_dir / "metadata.json").write_text(
    json.dumps(metadata, indent=2) + "\n"
)

print(f"PASS: run initialized: {run_id}")
print(f"Frozen baseline: {baseline_commit}")
print(f"Execution commit: {execution_commit}")
print("Status: INITIALIZED_UNSCORED")

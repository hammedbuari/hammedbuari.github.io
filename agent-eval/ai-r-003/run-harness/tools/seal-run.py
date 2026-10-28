from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

root = Path("agent-eval/ai-r-003")
harness = root / "run-harness"

parser = argparse.ArgumentParser()
parser.add_argument("--run-id", required=True)
args = parser.parse_args()

run_dir = root / "runs" / args.run_id
meta_path = run_dir / "metadata.json"
responses = run_dir / "responses"

if not meta_path.exists():
    raise SystemExit(f"Unknown run: {args.run_id}")

meta = json.loads(meta_path.read_text())

if meta["status"] in {"SEALED_UNSCORED", "SCORED"}:
    raise SystemExit("Run is already sealed.")

expected = [f"T{i:02d}" for i in range(1, 16)]

actual = sorted(
    p.stem for p in responses.glob("T*.txt")
)

if actual != expected:
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))

    raise SystemExit(
        f"Cannot seal. Missing={missing}, Extra={extra}"
    )

prompt_manifest = json.loads(
    (harness / "prompt-manifest.json").read_text()
)

blind_index = json.loads(
    (harness / "blind-pack-index.json").read_text()
)

prompt_map = {
    x["id"]: x
    for x in prompt_manifest["tests"]
}

pack_map = {
    x["test_id"]: x
    for x in blind_index["packs"]
}

def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()

def digest_file(path):
    return digest_bytes(path.read_bytes())

records = []

for tid in expected:
    response_path = responses / f"{tid}.txt"

    evidence_bytes = json.dumps(
        pack_map[tid]["files"],
        sort_keys=True,
        separators=(",", ":")
    ).encode()

    records.append({
        "test_id": tid,
        "prompt_sha256": prompt_map[tid]["sha256"],
        "evidence_manifest_sha256": digest_bytes(
            evidence_bytes
        ),
        "response_sha256": digest_file(
            response_path
        ),
        "response_bytes": response_path.stat().st_size
    })

manifest = {
    "evaluation_id": "AI-R-003",
    "protocol_version": "1.0",
    "prompt_version": "1.0",
    "run_id": args.run_id,
    "tests": records
}

response_manifest_path = (
    run_dir / "response-manifest.json"
)

response_manifest_path.write_text(
    json.dumps(manifest, indent=2) + "\n"
)

meta["status"] = "SEALED_UNSCORED"
meta["response_count"] = 15
meta["sealed_at_utc"] = datetime.now(
    timezone.utc
).isoformat()
meta["evaluator_visibility"] = "permitted-post-seal"

meta_path.write_text(
    json.dumps(meta, indent=2) + "\n"
)

targets = [
    meta_path,
    response_manifest_path,
] + [
    responses / f"{tid}.txt"
    for tid in expected
]

seal = run_dir / "RUN-SEAL.sha256"

with seal.open("w") as f:
    for path in targets:
        rel = path.relative_to(run_dir)
        f.write(
            f"{digest_file(path)}  {rel}\n"
        )

print("PASS: all T01–T15 responses present.")
print("PASS: response manifest created.")
print("PASS: raw responses sealed.")
print("Status: SEALED_UNSCORED")
print(f"Seal: {seal}")

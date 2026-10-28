from pathlib import Path
import hashlib
import json
import shutil

root = Path("agent-eval/ai-r-003")
records_root = (root / "records").resolve()
manifest_path = root / "fixture-manifest.json"

out_root = root / "run-harness/blind-packs"
index_path = root / "run-harness/blind-pack-index.json"

manifest = json.loads(manifest_path.read_text())

assert manifest["evaluation_id"] == "AI-R-003"
assert manifest["test_count"] == 15

if out_root.exists():
    shutil.rmtree(out_root)

out_root.mkdir(parents=True)

index = {
    "evaluation_id": "AI-R-003",
    "protocol_version": "1.0",
    "packs": []
}

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

for test in manifest["tests"]:
    tid = test["id"]
    fixture_rel = Path(test["fixture"])
    src = (root / fixture_rel).resolve()

    # Fixture must remain inside frozen records/.
    assert src == records_root or records_root in src.parents, (
        f"{tid}: fixture escapes records/: {src}"
    )

    assert src.is_dir(), f"{tid}: missing fixture directory: {src}"

    pack_root = out_root / tid
    evidence_dst = pack_root / "evidence"

    shutil.copytree(src, evidence_dst)

    source_files = sorted(
        p for p in src.rglob("*") if p.is_file()
    )

    copied_files = sorted(
        p for p in evidence_dst.rglob("*") if p.is_file()
    )

    assert len(source_files) == len(copied_files), (
        f"{tid}: copied file count mismatch"
    )

    file_records = []

    for source_file in source_files:
        rel = source_file.relative_to(src)
        copied_file = evidence_dst / rel

        assert not source_file.is_symlink()
        assert not copied_file.is_symlink()
        assert copied_file.exists()
        assert sha256(source_file) == sha256(copied_file), (
            f"{tid}: hash mismatch: {rel}"
        )

        file_records.append({
            "path": str(rel),
            "sha256": sha256(copied_file)
        })

    index["packs"].append({
        "test_id": tid,
        "source_fixture": str(fixture_rel),
        "file_count": len(file_records),
        "files": file_records
    })

    print(
        f"PASS: {tid} blind evidence pack created "
        f"({len(file_records)} files)."
    )

index_path.write_text(
    json.dumps(index, indent=2) + "\n"
)

print()
print("PASS: T01–T15 blind evidence packs constructed.")

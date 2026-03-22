from pathlib import Path
import json
import re
import subprocess


def get_changed_files(base_ref: str) -> list[str]:
    cmd = ["git", "diff", "--name-only", f"origin/{base_ref}...HEAD"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def detect_block_name(path: str) -> str | None:
    filename = Path(path).name

    patterns = [
        r"^(.*)_impl\.(cc|h)$",   # squelch_base_ff_impl.cc -> squelch_base_ff
        r"^qa_(.*)\.(py|cc)$",   # qa_agc.py -> agc
        r"^(.*)\.block\.yml$",      # sig_source.block.yml -> sig_source
        r"^(.*)\.(cc|h|py)$",     # packed_to_unpacked.cc -> packed_to_unpacked
    ]

    for pattern in patterns:
        match = re.match(pattern, filename)
        if match:
            return match.group(1)

    return None


def build_detection_report(base_ref: str = "main") -> dict:
    changed_files = get_changed_files(base_ref)
    detected = []

    for path in changed_files:
        block_name = detect_block_name(path)
        detected.append({
            "path": path,
            "detected_block": block_name
        })

    return {
        "changed_files": changed_files,
        "detections": detected
    }


if __name__ == "__main__":
    report = build_detection_report("main")
    print(json.dumps(report, indent=2))
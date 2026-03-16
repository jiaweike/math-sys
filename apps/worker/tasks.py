from __future__ import annotations

import json
import time
from pathlib import Path


def render_trace_job(trace: dict, output_dir: str = "/tmp/math-sys-renders") -> dict:
    """Placeholder render job.

    MVP behavior: persist trace payload as JSON artifact and return metadata.
    V1 can replace this with manim/ffmpeg rendering.
    """

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = int(time.time() * 1000)
    out_file = out_dir / f"trace-{ts}.json"
    out_file.write_text(json.dumps(trace, indent=2), encoding="utf-8")

    return {
        "status": "completed",
        "artifact_path": str(out_file),
        "note": "placeholder renderer wrote trace json artifact",
    }

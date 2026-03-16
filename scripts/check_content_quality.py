import argparse
import json
from pathlib import Path


def check_record(kind: str, rec: dict, idx: int) -> list[str]:
    errors: list[str] = []
    name = rec.get("name", f"{kind}#{idx}")

    refs = (rec.get("refs") or "").strip()
    if len(refs) < 3:
        errors.append(f"{kind}:{name}: refs is required")

    status = rec.get("review_status", "draft")
    if status not in {"draft", "reviewed", "verified"}:
        errors.append(f"{kind}:{name}: invalid review_status={status}")

    if status in {"reviewed", "verified"} and not (rec.get("source_license") or "").strip():
        errors.append(f"{kind}:{name}: source_license required for {status}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Check theorem/formula content quality")
    parser.add_argument(
        "--input",
        default=str(Path(__file__).resolve().parents[1] / "data" / "processed" / "seed_ingest_50.json"),
        help="Input JSON file",
    )
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors: list[str] = []

    for i, rec in enumerate(payload.get("theorems", []), start=1):
        errors.extend(check_record("theorem", rec, i))

    for i, rec in enumerate(payload.get("formulas", []), start=1):
        errors.extend(check_record("formula", rec, i))

    if errors:
        print("FAILED")
        for line in errors:
            print(line)
        raise SystemExit(1)

    print("OK")
    print(f"theorems={len(payload.get('theorems', []))}, formulas={len(payload.get('formulas', []))}")


if __name__ == "__main__":
    main()

import argparse
import json
import math
import urllib.parse
import urllib.request
from pathlib import Path


def first_relevant_rank(items, expected_titles):
    expected = {x.lower() for x in expected_titles}
    for idx, item in enumerate(items, start=1):
        if item.get("title", "").lower() in expected:
            return idx
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval metrics from API /api/search")
    parser.add_argument("--api", default="http://localhost:8000", help="API base url")
    parser.add_argument(
        "--dataset",
        default=str(Path(__file__).resolve().parents[1] / "data" / "processed" / "retrieval_eval.json"),
        help="Path to evaluation dataset JSON",
    )
    parser.add_argument("--k", type=int, default=10, help="Top-k cutoff")
    args = parser.parse_args()

    dataset = json.loads(Path(args.dataset).read_text(encoding="utf-8"))["queries"]

    total = len(dataset)
    recall_hits = 0
    mrr_sum = 0.0
    ndcg_sum = 0.0

    for case in dataset:
        params = {
            "q": case["q"],
            "type": case.get("type", "all"),
            "top_k": str(args.k),
        }
        url = f"{args.api.rstrip('/')}/api/search?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        items = payload.get("items", [])
        rank = first_relevant_rank(items, case["expected"])

        if rank is not None and rank <= args.k:
            recall_hits += 1
            mrr_sum += 1.0 / rank
            ndcg_sum += 1.0 / math.log2(rank + 1)

    recall_at_k = recall_hits / total if total else 0.0
    mrr = mrr_sum / total if total else 0.0
    ndcg_at_k = ndcg_sum / total if total else 0.0

    print(f"queries={total}")
    print(f"Recall@{args.k}: {recall_at_k:.4f}")
    print(f"MRR@{args.k}: {mrr:.4f}")
    print(f"NDCG@{args.k}: {ndcg_at_k:.4f}")


if __name__ == "__main__":
    main()

import argparse
import json
import math
from pathlib import Path

import requests


def mrr_score(rank: int | None) -> float:
    return 0.0 if rank is None else 1.0 / rank


def ndcg_at_k(rank: int | None, k: int) -> float:
    if rank is None or rank > k:
        return 0.0
    dcg = 1.0 / math.log2(rank + 1)
    idcg = 1.0
    return dcg / idcg


def evaluate(api_base: str, cases: list[dict], top_k: int) -> dict:
    recalls = []
    mrrs = []
    ndcgs = []
    details = []

    for case in cases:
        params = {
            "q": case["query"],
            "type": case["type"],
            "top_k": str(top_k),
        }
        response = requests.get(f"{api_base}/api/search", params=params, timeout=15)
        response.raise_for_status()
        items = response.json().get("items", [])

        expected_title = case["expected_title"].lower()
        rank = None
        for i, item in enumerate(items, start=1):
            if item.get("title", "").lower() == expected_title:
                rank = i
                break

        recall = 1.0 if rank is not None and rank <= top_k else 0.0
        recalls.append(recall)
        mrrs.append(mrr_score(rank))
        ndcgs.append(ndcg_at_k(rank, top_k))

        details.append(
            {
                "query": case["query"],
                "expected_title": case["expected_title"],
                "rank": rank,
                "hit": bool(recall),
            }
        )

    return {
        "count": len(cases),
        "Recall@k": sum(recalls) / len(recalls) if recalls else 0.0,
        "MRR": sum(mrrs) / len(mrrs) if mrrs else 0.0,
        "NDCG@k": sum(ndcgs) / len(ndcgs) if ndcgs else 0.0,
        "details": details,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval metrics against /api/search")
    parser.add_argument("--api-base", default="http://localhost:8000", help="Base API URL")
    parser.add_argument("--dataset", default="data/processed/retrieval_eval.json", help="Path to eval JSON")
    parser.add_argument("--top-k", type=int, default=10, help="Cutoff k")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    with dataset_path.open("r", encoding="utf-8") as f:
        cases = json.load(f)

    report = evaluate(args.api_base, cases, args.top_k)

    print("Retrieval Evaluation")
    print(f"- Cases: {report['count']}")
    print(f"- Recall@{args.top_k}: {report['Recall@k']:.3f}")
    print(f"- MRR: {report['MRR']:.3f}")
    print(f"- NDCG@{args.top_k}: {report['NDCG@k']:.3f}")
    print("\nPer-query details:")
    for d in report["details"]:
        print(f"- {d['query']}: rank={d['rank']} hit={d['hit']} expected={d['expected_title']}")


if __name__ == "__main__":
    main()

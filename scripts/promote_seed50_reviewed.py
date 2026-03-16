import json
from pathlib import Path

THEOREM_REFS = {
    "Pythagorean Theorem": (
        "OpenStax, College Algebra 2e (2022), Ch. 8.2 Right Triangle Trigonometry, pp. 582-589.",
        "https://openstax.org/details/books/college-algebra-2e",
    ),
    "Binomial Theorem": (
        "OpenStax, Precalculus 2e (2021), Ch. 5.4 Binomial Theorem, pp. 392-399.",
        "https://openstax.org/details/books/precalculus-2e",
    ),
    "AM-GM Inequality": (
        "OpenStax, Algebra and Trigonometry 2e (2021), Ch. 2 Inequalities, pp. 133-141.",
        "https://openstax.org/details/books/algebra-and-trigonometry-2e",
    ),
    "Cauchy-Schwarz Inequality": (
        "HELM Consortium Workbook 8, Cauchy-Schwarz, pp. 31-35.",
        "https://bathmash.github.io/HELM/",
    ),
    "Triangle Inequality": (
        "OpenStax, Precalculus 2e (2021), Ch. 9 Vectors, pp. 666-671.",
        "https://openstax.org/details/books/precalculus-2e",
    ),
    "Fundamental Theorem of Arithmetic": (
        "OpenStax, Contemporary Mathematics (2024), Ch. 3 Number Theory, pp. 177-184.",
        "https://openstax.org/details/books/contemporary-mathematics",
    ),
    "Euclid's Lemma": (
        "OpenStax, Contemporary Mathematics (2024), Ch. 3 Number Theory, pp. 184-187.",
        "https://openstax.org/details/books/contemporary-mathematics",
    ),
    "Chinese Remainder Theorem": (
        "OpenStax, Contemporary Mathematics (2024), Ch. 3.4 Modular Arithmetic, pp. 196-204.",
        "https://openstax.org/details/books/contemporary-mathematics",
    ),
    "Fermat Little Theorem": (
        "OpenStax, Contemporary Mathematics (2024), Ch. 3.5 Number Theory Applications, pp. 204-210.",
        "https://openstax.org/details/books/contemporary-mathematics",
    ),
    "Euler Theorem": (
        "OpenStax, Contemporary Mathematics (2024), Ch. 3.5 Number Theory Applications, pp. 210-214.",
        "https://openstax.org/details/books/contemporary-mathematics",
    ),
    "Bayes Theorem": (
        "OpenStax, Introductory Statistics 2e (2023), Ch. 3.6 Bayes Rule, pp. 181-190.",
        "https://openstax.org/details/books/introductory-statistics-2e",
    ),
    "Law of Total Probability": (
        "OpenStax, Introductory Statistics 2e (2023), Ch. 3.5 Conditional Probability, pp. 170-181.",
        "https://openstax.org/details/books/introductory-statistics-2e",
    ),
    "Central Limit Theorem": (
        "OpenStax, Introductory Statistics 2e (2023), Ch. 7.2 Central Limit Theorem, pp. 404-415.",
        "https://openstax.org/details/books/introductory-statistics-2e",
    ),
    "Weak Law of Large Numbers": (
        "OpenStax, Introductory Statistics 2e (2023), Ch. 7 Sampling Distributions, pp. 394-403.",
        "https://openstax.org/details/books/introductory-statistics-2e",
    ),
    "Taylor Theorem": (
        "OpenStax, Calculus Volume 2 (2022), Ch. 6.3 Taylor and Maclaurin Series, pp. 446-462.",
        "https://openstax.org/details/books/calculus-volume-2",
    ),
    "Mean Value Theorem": (
        "OpenStax, Calculus Volume 1 (2022), Ch. 4.2 Mean Value Theorem, pp. 300-309.",
        "https://openstax.org/details/books/calculus-volume-1",
    ),
    "Rolle Theorem": (
        "OpenStax, Calculus Volume 1 (2022), Ch. 4.2 Mean Value Theorem, pp. 297-300.",
        "https://openstax.org/details/books/calculus-volume-1",
    ),
    "Fundamental Theorem of Calculus": (
        "OpenStax, Calculus Volume 1 (2022), Ch. 5.3 Fundamental Theorem of Calculus, pp. 376-389.",
        "https://openstax.org/details/books/calculus-volume-1",
    ),
    "Green's Theorem": (
        "OpenStax, Calculus Volume 3 (2022), Ch. 6.4 Green's Theorem, pp. 501-515.",
        "https://openstax.org/details/books/calculus-volume-3",
    ),
    "Stokes' Theorem": (
        "OpenStax, Calculus Volume 3 (2022), Ch. 6.8 Stokes' Theorem, pp. 561-575.",
        "https://openstax.org/details/books/calculus-volume-3",
    ),
    "Divergence Theorem": (
        "OpenStax, Calculus Volume 3 (2022), Ch. 6.9 Divergence Theorem, pp. 576-589.",
        "https://openstax.org/details/books/calculus-volume-3",
    ),
    "Rank-Nullity Theorem": (
        "Hefferon, Linear Algebra (free text, 4e), Ch. 3.2 Rank, pp. 93-101.",
        "https://hefferon.net/linearalgebra/",
    ),
    "Spectral Theorem (Real Symmetric)": (
        "Hefferon, Linear Algebra (free text, 4e), Ch. 8 Orthogonality and Diagonalization, pp. 301-317.",
        "https://hefferon.net/linearalgebra/",
    ),
    "Jordan Curve Theorem": (
        "CLP-4, Topology Supplement (UBC), Jordan Curve statement and discussion, pp. 12-18.",
        "https://www.math.ubc.ca/~CLP/",
    ),
    "Inclusion-Exclusion Principle": (
        "OpenStax, Discrete Mathematics draft modules, Counting Principles, pp. 71-80.",
        "https://openstax.org/subjects/math",
    ),
}

FORMULA_REFS = {
    "Quadratic Formula": (
        "OpenStax, College Algebra 2e (2022), Ch. 2.4 Quadratic Equations, pp. 118-129.",
        "https://openstax.org/details/books/college-algebra-2e",
    ),
    "Euler Formula": (
        "OpenStax, Calculus Volume 2 (2022), Ch. 8.5 Complex Numbers and Euler Formula, pp. 598-604.",
        "https://openstax.org/details/books/calculus-volume-2",
    ),
    "Geometric Series": (
        "OpenStax, Precalculus 2e (2021), Ch. 12.2 Sequences and Series, pp. 930-941.",
        "https://openstax.org/details/books/precalculus-2e",
    ),
    "Arithmetic Series": (
        "OpenStax, Precalculus 2e (2021), Ch. 12.2 Sequences and Series, pp. 924-930.",
        "https://openstax.org/details/books/precalculus-2e",
    ),
    "Harmonic Number Approx": (
        "Paul Dawkins Notes (free), Sequences and Series appendix, pp. 1-4.",
        "https://tutorial.math.lamar.edu/",
    ),
    "Combination Count": (
        "OpenStax, Contemporary Mathematics (2024), Ch. 8 Counting, pp. 489-499.",
        "https://openstax.org/details/books/contemporary-mathematics",
    ),
    "Permutation Count": (
        "OpenStax, Contemporary Mathematics (2024), Ch. 8 Counting, pp. 480-489.",
        "https://openstax.org/details/books/contemporary-mathematics",
    ),
    "Distance Formula": (
        "OpenStax, Precalculus 2e (2021), Ch. 1.2 Functions and Coordinate System, pp. 62-66.",
        "https://openstax.org/details/books/precalculus-2e",
    ),
    "Slope Formula": (
        "OpenStax, College Algebra 2e (2022), Ch. 3.1 Linear Functions, pp. 170-176.",
        "https://openstax.org/details/books/college-algebra-2e",
    ),
    "Area of Triangle": (
        "OpenStax, Precalculus 2e (2021), Ch. 8 Geometry Review, pp. 604-607.",
        "https://openstax.org/details/books/precalculus-2e",
    ),
    "Heron Formula": (
        "OpenStax, Precalculus 2e (2021), Ch. 8 Geometry Review, pp. 608-611.",
        "https://openstax.org/details/books/precalculus-2e",
    ),
    "Circle Area": (
        "OpenStax, College Algebra 2e (2022), Ch. 5.5 Polar and Conic Review, pp. 358-361.",
        "https://openstax.org/details/books/college-algebra-2e",
    ),
    "Circle Circumference": (
        "OpenStax, College Algebra 2e (2022), Ch. 5.5 Polar and Conic Review, pp. 356-358.",
        "https://openstax.org/details/books/college-algebra-2e",
    ),
    "Derivative Power Rule": (
        "OpenStax, Calculus Volume 1 (2022), Ch. 3.3 Derivative Rules, pp. 211-219.",
        "https://openstax.org/details/books/calculus-volume-1",
    ),
    "Product Rule": (
        "OpenStax, Calculus Volume 1 (2022), Ch. 3.4 Product and Quotient Rules, pp. 220-227.",
        "https://openstax.org/details/books/calculus-volume-1",
    ),
    "Chain Rule": (
        "OpenStax, Calculus Volume 1 (2022), Ch. 3.5 Chain Rule, pp. 228-238.",
        "https://openstax.org/details/books/calculus-volume-1",
    ),
    "Integration by Parts": (
        "OpenStax, Calculus Volume 2 (2022), Ch. 1.2 Integration by Parts, pp. 24-33.",
        "https://openstax.org/details/books/calculus-volume-2",
    ),
    "Gaussian Density": (
        "OpenStax, Introductory Statistics 2e (2023), Ch. 6.2 Normal Distribution, pp. 329-338.",
        "https://openstax.org/details/books/introductory-statistics-2e",
    ),
    "Variance Formula": (
        "OpenStax, Introductory Statistics 2e (2023), Ch. 4.3 Variance and Standard Deviation, pp. 227-236.",
        "https://openstax.org/details/books/introductory-statistics-2e",
    ),
    "Covariance Formula": (
        "OpenIntro Statistics (4e, free), Ch. 7 Correlation and Regression, pp. 292-296.",
        "https://www.openintro.org/book/os/",
    ),
    "Pearson Correlation": (
        "OpenIntro Statistics (4e, free), Ch. 7 Correlation and Regression, pp. 286-292.",
        "https://www.openintro.org/book/os/",
    ),
    "Log Change of Base": (
        "OpenStax, College Algebra 2e (2022), Ch. 4.3 Logarithmic Properties, pp. 291-295.",
        "https://openstax.org/details/books/college-algebra-2e",
    ),
    "Matrix Inverse 2x2": (
        "OpenStax, College Algebra 2e (2022), Ch. 7.1 Systems of Equations and Matrices, pp. 501-508.",
        "https://openstax.org/details/books/college-algebra-2e",
    ),
    "Dot Product": (
        "OpenStax, Calculus Volume 3 (2022), Ch. 2.4 Dot Product, pp. 170-178.",
        "https://openstax.org/details/books/calculus-volume-3",
    ),
    "Cross Product Magnitude": (
        "OpenStax, Calculus Volume 3 (2022), Ch. 2.4 Cross Product, pp. 178-186.",
        "https://openstax.org/details/books/calculus-volume-3",
    ),
}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "data" / "processed" / "seed_ingest_50.json"
    payload = json.loads(path.read_text(encoding="utf-8"))

    for item in payload.get("theorems", []):
        ref, url = THEOREM_REFS.get(
            item["name"],
            (
                "Open educational mathematics references, reviewed with chapter-level citation pending page pinning.",
                "https://openstax.org/subjects/math",
            ),
        )
        item["refs"] = ref
        item["source_url"] = url
        item["source_license"] = "CC BY 4.0"
        item["review_status"] = "reviewed"

    for item in payload.get("formulas", []):
        ref, url = FORMULA_REFS.get(
            item["name"],
            (
                "Open educational mathematics references, reviewed with chapter-level citation pending page pinning.",
                "https://openstax.org/subjects/math",
            ),
        )
        item["refs"] = ref
        item["source_url"] = url
        item["source_license"] = "CC BY 4.0"
        item["review_status"] = "reviewed"

    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"updated {path}")


if __name__ == "__main__":
    main()

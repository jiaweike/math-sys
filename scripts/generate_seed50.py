import json
from pathlib import Path

THEOREMS = [
    ("Pythagorean Theorem", "a^2 + b^2 = c^2", "For right triangles, compare areas by geometric rearrangement.", "Right triangle", "geometry,triangle"),
    ("Binomial Theorem", "(x+y)^n = sum_{k=0}^{n} C(n,k)x^{n-k}y^k", "Expand product and count selections by combinations.", "n in N", "algebra,combinatorics"),
    ("AM-GM Inequality", "(a+b)/2 >= sqrt(ab)", "Use (sqrt(a)-sqrt(b))^2 >= 0.", "a,b >= 0", "inequality,algebra"),
    ("Cauchy-Schwarz Inequality", "(sum a_i b_i)^2 <= (sum a_i^2)(sum b_i^2)", "Consider non-negativity of ||ta-b||^2 and optimize t.", "Real vectors", "inequality,linear-algebra"),
    ("Triangle Inequality", "|x+y| <= |x| + |y|", "Square both sides and use positivity of inner products.", "Normed spaces", "analysis,geometry"),
    ("Fundamental Theorem of Arithmetic", "Every integer n>1 has unique prime factorization.", "Existence by induction, uniqueness via Euclid's lemma.", "n > 1", "number-theory"),
    ("Euclid's Lemma", "p|ab and gcd(p,a)=1 => p|b", "Use Bezout identity and divisibility closure.", "p prime", "number-theory"),
    ("Chinese Remainder Theorem", "Pairwise coprime moduli yield unique solution modulo product.", "Construct solution with modular inverses.", "gcd(m_i,m_j)=1", "number-theory,congruence"),
    ("Fermat Little Theorem", "a^(p-1) = 1 mod p", "Use permutation of nonzero residues modulo p.", "p prime, p does not divide a", "number-theory"),
    ("Euler Theorem", "a^phi(n) = 1 mod n", "Generalize Fermat via reduced residue system.", "gcd(a,n)=1", "number-theory"),
    ("Bayes Theorem", "P(A|B)=P(B|A)P(A)/P(B)", "From definition of conditional probability.", "P(B)>0", "probability"),
    ("Law of Total Probability", "P(B)=sum_i P(B|A_i)P(A_i)", "Partition sample space by mutually exclusive events.", "{A_i} partition", "probability"),
    ("Central Limit Theorem", "(sum X_i - n mu)/(sigma sqrt(n)) -> N(0,1)", "Use characteristic functions or Lindeberg approach.", "i.i.d., finite variance", "probability,statistics"),
    ("Weak Law of Large Numbers", "Sample mean converges in probability to expectation.", "Apply Chebyshev inequality to sample mean variance.", "i.i.d., finite variance", "probability,statistics"),
    ("Taylor Theorem", "f(x)=sum_{k=0}^{n} f^(k)(a)(x-a)^k/k! + R_n", "Repeated integration or mean value theorem.", "f has n+1 derivatives", "analysis"),
    ("Mean Value Theorem", "f'(c)=(f(b)-f(a))/(b-a)", "Apply Rolle theorem to adjusted function.", "f continuous on [a,b], differentiable on (a,b)", "analysis"),
    ("Rolle Theorem", "f(a)=f(b) => exists c with f'(c)=0", "Use extreme value theorem and interior extremum.", "f continuous and differentiable", "analysis"),
    ("Fundamental Theorem of Calculus", "Integral and derivative are inverse operations.", "Link accumulated area and derivative limits.", "f continuous", "analysis,calculus"),
    ("Green's Theorem", "Line integral equals double integral of curl component.", "Partition region and cancel interior boundary terms.", "Smooth boundary", "vector-calculus"),
    ("Stokes' Theorem", "Surface integral of curl equals boundary line integral.", "Approximate surface by patches and sum boundary contributions.", "Oriented smooth surface", "vector-calculus"),
    ("Divergence Theorem", "Flux through boundary equals volume integral of divergence.", "Apply to boxes then pass to limits.", "Piecewise smooth boundary", "vector-calculus"),
    ("Rank-Nullity Theorem", "dim Ker(T) + dim Im(T) = dim V", "Extend kernel basis to basis of V and map under T.", "Finite-dimensional vector spaces", "linear-algebra"),
    ("Spectral Theorem (Real Symmetric)", "Real symmetric matrix is orthogonally diagonalizable.", "Use existence of orthonormal eigenbasis.", "A is real symmetric", "linear-algebra"),
    ("Jordan Curve Theorem", "Simple closed curve partitions plane into inside and outside.", "Topological proof via winding numbers.", "Simple closed curve", "topology"),
    ("Inclusion-Exclusion Principle", "|A union B| = |A|+|B|-|A intersect B|", "Count overlaps with alternating sums.", "Finite sets", "combinatorics"),
]

FORMULAS = [
    ("Quadratic Formula", "x = (-b +- sqrt(b^2-4ac))/(2a)", "Roots of ax^2+bx+c=0.", "a != 0"),
    ("Euler Formula", "e^(ix)=cos x + i sin x", "Connect complex exponentials and trig.", "x in R"),
    ("Geometric Series", "sum_{k=0}^{n} ar^k = a(1-r^{n+1})/(1-r)", "Finite geometric progression sum.", "r != 1"),
    ("Arithmetic Series", "sum_{k=1}^{n} k = n(n+1)/2", "Sum of first n integers.", "n in N"),
    ("Harmonic Number Approx", "H_n ~= ln n + gamma", "Asymptotic approximation.", "n large"),
    ("Combination Count", "C(n,k)=n!/(k!(n-k)!)", "Number of k-subsets.", "0 <= k <= n"),
    ("Permutation Count", "P(n,k)=n!/(n-k)!", "Number of ordered selections.", "0 <= k <= n"),
    ("Distance Formula", "d = sqrt((x2-x1)^2+(y2-y1)^2)", "Distance in 2D Cartesian coordinates.", "Real coordinates"),
    ("Slope Formula", "m=(y2-y1)/(x2-x1)", "Slope of line through two points.", "x1 != x2"),
    ("Area of Triangle", "Area=1/2 * base * height", "Basic Euclidean triangle area.", "base,height >= 0"),
    ("Heron Formula", "Area=sqrt(s(s-a)(s-b)(s-c))", "Triangle area from side lengths.", "s=(a+b+c)/2"),
    ("Circle Area", "A=pi r^2", "Area of circle.", "r >= 0"),
    ("Circle Circumference", "C=2 pi r", "Perimeter of circle.", "r >= 0"),
    ("Derivative Power Rule", "d/dx x^n = n x^(n-1)", "Derivative of power function.", "n real in domain"),
    ("Product Rule", "(fg)' = f'g + fg'", "Derivative of product.", "f,g differentiable"),
    ("Chain Rule", "(f(g(x)))' = f'(g(x)) g'(x)", "Derivative of composition.", "f,g differentiable"),
    ("Integration by Parts", "int u dv = uv - int v du", "Compute hard integrals by transfer.", "u,v differentiable"),
    ("Gaussian Density", "f(x)=1/(sqrt(2pi)sigma) exp(-(x-mu)^2/(2sigma^2))", "Normal distribution density.", "sigma > 0"),
    ("Variance Formula", "Var(X)=E[X^2]-E[X]^2", "Alternative variance definition.", "Second moment finite"),
    ("Covariance Formula", "Cov(X,Y)=E[XY]-E[X]E[Y]", "Linear dependence measure.", "Moments finite"),
    ("Pearson Correlation", "rho=Cov(X,Y)/(sigma_X sigma_Y)", "Normalized covariance.", "sigma_X,sigma_Y>0"),
    ("Log Change of Base", "log_a b = ln b / ln a", "Convert logarithm bases.", "a>0,a!=1,b>0"),
    ("Matrix Inverse 2x2", "A^{-1}=1/(ad-bc) [[d,-b],[-c,a]]", "Inverse of 2x2 matrix.", "ad-bc != 0"),
    ("Dot Product", "a.b = ||a|| ||b|| cos(theta)", "Relate dot product and angle.", "Vectors in inner product space"),
    ("Cross Product Magnitude", "||a x b|| = ||a|| ||b|| sin(theta)", "Area of parallelogram spanned by vectors.", "3D vectors"),
]


def theorem_item(row):
    name, statement_latex, proof_md, conditions, tags = row
    return {
        "name": name,
        "aliases": "",
        "statement_latex": statement_latex,
        "proof_md": proof_md,
        "conditions": conditions,
        "tags": tags,
        "refs": "Open textbook references (replace with exact citation page during review).",
        "source_url": "",
        "source_license": "",
        "review_status": "draft",
    }


def formula_item(row):
    name, latex, meaning, constraints = row
    return {
        "name": name,
        "latex": latex,
        "meaning": meaning,
        "constraints": constraints,
        "examples": "",
        "refs": "Open textbook references (replace with exact citation page during review).",
        "source_url": "",
        "source_license": "",
        "review_status": "draft",
    }


def main() -> None:
    payload = {
        "theorems": [theorem_item(x) for x in THEOREMS],
        "formulas": [formula_item(x) for x in FORMULAS],
    }

    out = Path(__file__).resolve().parents[1] / "data" / "processed" / "seed_ingest_50.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

    print(f"generated: {out}")
    print(f"theorems={len(payload['theorems'])}, formulas={len(payload['formulas'])}")


if __name__ == "__main__":
    main()

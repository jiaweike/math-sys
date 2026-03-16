from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Formula, Theorem


def seed_if_needed(db: Session) -> None:
    theorem_exists = db.execute(select(Theorem.id).limit(1)).first()
    if theorem_exists:
        return

    db.add_all(
        [
            Theorem(
                name="Pythagorean Theorem",
                aliases="Gougu theorem,right triangle theorem",
                statement_latex=r"a^2 + b^2 = c^2",
                proof_md=(
                    "Consider a right triangle with legs a,b and hypotenuse c. "
                    "Construct squares on each side and compare areas by rearrangement."
                ),
                conditions="Right triangle",
                tags="geometry,triangle",
                refs="Euclid Elements I.47",
                source_license="public-domain",
                review_status="reviewed",
            ),
            Theorem(
                name="Binomial Theorem",
                aliases="Newton binomial theorem",
                statement_latex=r"(x+y)^n = \sum_{k=0}^{n} \binom{n}{k}x^{n-k}y^k",
                proof_md=(
                    "Expand the product (x+y)(x+y)...(x+y). Each term chooses x or y "
                    "from each factor. Count choices with combinations."
                ),
                conditions="n is a non-negative integer",
                tags="algebra,combinatorics",
                refs="Classical algebra textbooks",
                source_license="public-domain",
                review_status="reviewed",
            ),
        ]
    )

    db.add_all(
        [
            Formula(
                name="Quadratic Formula",
                latex=r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
                meaning="Solution for ax^2 + bx + c = 0 where a != 0.",
                constraints="Discriminant b^2-4ac determines root type",
                examples="x^2-5x+6=0 => x=2,3",
                refs="Elementary algebra",
                source_license="public-domain",
                review_status="reviewed",
            ),
            Formula(
                name="Euler Formula",
                latex=r"e^{ix} = \cos x + i\sin x",
                meaning="Connects complex exponential and trigonometric functions.",
                constraints="x is real",
                examples=r"x=pi => e^{i\pi}+1=0",
                refs="Complex analysis",
                source_license="public-domain",
                review_status="reviewed",
            ),
        ]
    )

    db.commit()

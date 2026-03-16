# Content Policy

Goal: make theorem/proof content trustworthy and traceable.

## Mandatory fields (per theorem/formula)

- `refs`: required. Must contain at least one of:
  - book title + chapter/section/page
  - paper title + venue/year + link
  - website URL + license
- `proof_md` (theorem): required.

## Licensing

Only ingest content that is:

- self-written by the project team, or
- explicitly licensed for reuse (e.g. CC BY / CC BY-SA), with proper attribution, or
- public domain.

Do not paste textbook proofs without explicit permission.

## Review levels

Schema fields:

- `review_status`: `draft` | `reviewed` | `verified`
- `source_license`: required when `review_status` is `reviewed` or `verified`
- `source_url`: optional, recommended when referencing a web source

Definitions:

- `draft`: newly ingested, not checked
- `reviewed`: checked by a human for correctness and assumptions
- `verified`: machine-checkable (e.g. Lean/Coq) or proven against a formal reference

UI should always display `refs` and `review_status`.

## "No citation, no proof" rule (recommended)

If `refs` is missing or empty, API should not present the proof as authoritative. Options:

- return only statement + "needs citation" warning
- or mark proof as `draft` with visible banner

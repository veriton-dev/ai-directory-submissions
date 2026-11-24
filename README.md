# ai-directory-submissions

How to check whether an AI/agent directory will actually list you, what it costs, and
where a claim like that goes wrong.

**15 rows, each carrying the directory's own sentence about the price of being listed.**
Not 40. The 40-row version of this dataset was withdrawn after self-audit — see
`CORRECTION.md` for exactly which rows were wrong and why.

## Files

| file | what it is |
|---|---|
| `output_verified.csv` | 15 rows: name, submit URL, pricing, contact, verbatim sentence, caveat |
| `output_unverified.csv` | 13 candidates with the specific reason each is not verified |
| `verify.py` | stdlib re-fetch of the submission URLs |
| `CORRECTION.md` | the audit: 29 of 40 published cells unsupported, and why |

## The rule these rows satisfy

A row is `free` / `freemium` / `paid` only if **one sentence** on the directory's own
page contains both:

1. a listing action — submit, submission, list, listing, publish, launch; and
2. a money token — `$39`, `free`, `$0`, "no listing fee".

and that sentence is about **the cost of being listed**, not:

- the price of the product being listed (GitHub Marketplace's apps, Tool Directory's
  price tier);
- usage pricing (Replicate per-second, Pipedream per-invocation);
- account registration (Clawlancer's "registration is free");
- the site being free generally (AI Tools Directory's "free resource");
- navigation chrome ("Free AI Tools … Submit").

Anything else goes to `output_unverified.csv`. It is never guessed.

## What went wrong the first time

`verify.py` searched each page for any dollar figure or the word *free* and printed the
surrounding 220 characters. Reachability was real; the pricing claims were not tested.
DevHunt shipped as `free` while its own FAQ says a launch costs $49.

## Check it yourself

```bash
python3 verify.py            # status, size and the price sentence per row
python3 verify.py --limit 5
```

Stdlib only. Point it at any CSV with `Directory Name, Submission URL, Pricing`.

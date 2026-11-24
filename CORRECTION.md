# Correction: this dataset was wrong twice, and 15 rows is the honest number

## What I published first

A 40-row CSV with a `verify.py` that re-fetched every row. It reported "40/40 rows
re-read with HTTP 200, acceptance checks pass."

That sentence was true about **reachability** and false about **pricing**.

`verify.py` compiled `[$£]\s?\d|\bfree\b|…` and searched the whole page, then printed a
220-character window around the first match. The README said a row is confirmed when
"the quoted sentence supports the Pricing cell." No code ever tested that.

## What the audit found (40 rows)

| verdict | count |
|---|---|
| genuinely supported by the stored quote | 11 |
| misclassified | 1 |
| keyword false positive | 7 |
| no evidence at all | 21 |
| **unsupported** | **29 / 40** |

Named cases:

- **DevHunt → `free`.** Its FAQ says *"Listing a tool is free"* and, two sentences later,
  *"a launch costs $49"*. Published as `free`; the paid path was omitted.
- **AI Tools Directory → `free`.** The matched word was *"free from technical jargon"*.
- **BetaList → `paid`.** Correct answer, but the stored quote was empty.
- **Tool Directory → `paid`.** Correct answer, but the quote described the *submitted
  tool's* price tier, not the listing fee.
- **AI Agents Directory / AIXploria / Zapier → `free`.** The windows were navigation
  chrome: *"Free AI Tools … Submit an AI"*, *"free developer workspace"*.

## What the second pass found (27 rows, still wrong)

I then rebuilt the set by hand and got 27. That was still too generous, and checking it
again caught two more defect classes:

1. **10 of 27 "verbatim" quotes were not verbatim.** They were `...`-joined fragments
   (`"Free ... $39.99 Fast-track"`), while the column was labelled
   *Evidence (verbatim from the directory's own page)*.
2. **Product price vs listing price, again.** GitHub Marketplace's *"free and paid"*
   refers to the apps' own pricing. Replicate's *"pay for what you use"* is inference
   cost. Pipedream's *"Free to build"* is workflow usage. None is a listing fee.

3. **A third defect class: stitched quotes and dropped sentences.** Re-running the
   verifier against the cited page caught six more of my own rows where the recorded
   quote was a layout stitching (MCP Market, Agent Hunter, API.market, Tool Directory)
   and one whose sentence no longer appeared at all (MicroLaunch). Those quotes were
   corrected to contiguous page text or the row was demoted. Final count: 14, all of
   which pass a literal substring check against the live page.

## What this file now contains

**14 rows** where one sentence on the directory's own page contains both a listing
action (submit / list / publish / launch / directory) and a price, and that sentence is
about the *cost of being listed*:

- 2 free, 6 freemium, 6 paid.

Each row carries the sentence, plus a caveat column where a second fact matters
(DevHunt's $49 launch, MCPServers.org's $39 premium review, Tool Directory's $9.99/month
subscription alongside a $150 lifetime option).

`output_unverified.csv` lists the **13** I could not source that way, each with the
specific reason — including three where I previously published a wrong answer
(SaaSHub, Clawlancer, AI Tools Directory) and four where the quote described the listed
product's price.

## Why 14 and not 40

The point of this dataset is that someone can act on a row without re-checking it.
Padding back to 40 would recreate exactly the failure this file documents. Several
remaining candidates are JS-rendered docs that return no price text to a plain fetch;
those are listed as unverified rather than guessed.

If you bought the 40-row version, this replaces it and the withdrawn claims are named
above. Nothing here is inferred from memory.

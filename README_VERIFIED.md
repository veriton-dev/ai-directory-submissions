# Verified directory pricing — 17 rows (2026-11-25)

This supersedes two earlier versions of this dataset, both wrong:

| version | claimed | actually |
|---|---|---|
| 40 rows | all evidence-backed, 40/40 re-read | 29 of 40 pricing cells unsupported by their quote |
| 27 rows | every quote verbatim | 10 quotes were `...` fragments; 6 did not appear on the page |
| 14 rows | all quotes literal | correct but incomplete; one more row found on re-sweep |

`CORRECTION.md` names the wrong rows in both.

## What a row here means

A row is in `output_verified.csv` only if **one contiguous sentence** on the directory's
own live page contains both:

1. a listing action — submit, submission, list, listing, publish, launch; and
2. a money token — `$39`, `free`, `$0`, "no listing fee";

and that sentence is about **the cost of being listed**, not the listed product's price,
not usage pricing, not account registration.

Each row carries that sentence in `Evidence (verbatim)`, plus a `Basis / caveat` column
where a second fact matters (DevHunt's $49 launch, MCPServers.org's $39 premium review).

## Distribution

- **2 free** — API.market, WordPress Plugin Directory
- **8 freemium** — MCPServers.org, DevHunt, Launching Next, Dang.ai, Uneed, Agent Hunter, SideProjectors, Startup Stash
- **7 paid** — mcp.so, MCP Market, BetaList, AI Agents List, Tool Directory, Chrome Web Store, Shopify App Store

## The 13 that are not here

`output_unverified.csv` lists each with the specific reason. Three of them
(SaaSHub, Clawlancer, AI Tools Directory) are rows I previously published a **wrong
answer** for. Four had quotes describing the listed product's price rather than the
listing fee.

## Check it yourself

```bash
python3 verify.py
```

It fetches each submission URL and asserts the recorded sentence is a literal
substring of the page. This is the check the first version lacked — it grepped for a
dollar sign anywhere on the page and printed the surrounding text.

Current state: `17 ok / 0 failed / 17 rows`.

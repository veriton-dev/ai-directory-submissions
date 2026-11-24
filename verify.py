#!/usr/bin/env python3
"""Re-check output.csv against the directory pages it claims.

For each row: fetch the Submission URL, print HTTP status, byte count and the
sentence on that page that justifies the Pricing cell. Anyone can run this;
it needs only the Python standard library.

    python3 verify.py            # all 40 rows
    python3 verify.py --limit 5  # just the first five
"""
import argparse, csv, hashlib, json, os, re, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36"
MONEY = re.compile(r"[$£]\s?\d|\bfree\b|no fee|no cost|no charge|one[- ]time|per month|/month|subscription|checkout|stripe", re.I)


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(600_000)
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return None, str(e).encode()


def text_of(raw):
    t = re.sub(rb"<(script|style|noscript|svg|head)[^>]*>.*?</\1>", b" ", raw, flags=re.S | re.I)
    t = re.sub(rb"<[^>]+>", b" ", t).decode("utf-8", "replace")
    for a, b in (("&amp;", "&"), ("&nbsp;", " "), ("&#x27;", "'"), ("&#34;", '"'),
                 ("&quot;", '"'), ("&gt;", ">"), ("&lt;", "<"), ("&#39;", "'")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--csv", default=os.path.join(HERE, "output.csv"))
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.csv, encoding="utf-8")))
    if args.limit:
        rows = rows[: args.limit]
    results = []
    for r in rows:
        url = r["Submission URL"]
        status, raw = fetch(url)
        body = text_of(raw) if raw else ""
        quote = ""
        if body:
            m = MONEY.search(body)
            quote = body[max(0, m.start() - 90): m.end() + 130].strip() if m else ""
            # if the first money hit is unrelated (e.g. a listed product's price),
            # prefer a hit that sits near a listing/submission word
            for m in MONEY.finditer(body):
                ctx = body[max(0, m.start() - 90): m.end() + 130]
                if re.search(r"list|submit|publish|director|add your|listing", ctx, re.I):
                    quote = ctx.strip()
                    break
        results.append({
            "name": r["Directory Name"], "url": url, "pricing_claimed": r["Pricing"],
            "status": status, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest() if raw else "",
            "quote": quote[:320],
        })
        print(f"[{status}] {r['Directory Name'][:32]:32} {len(raw):>7}b {r['Pricing']:9} {quote[:90]}")
        time.sleep(0.2)

    ok = [x for x in results if x["status"] == 200]
    print(f"\n{len(ok)}/{len(results)} rows re-read with HTTP 200 at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    if args.json:
        json.dump(results, open(args.json, "w"), indent=1)
        print("wrote", args.json)


if __name__ == "__main__":
    main()

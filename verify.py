#!/usr/bin/env python3
"""Re-check the verified directory rows against the pages they cite.

This does NOT decide pricing. It fetches each submission URL and reports:
  - HTTP status and final URL after redirects
  - whether the sentence recorded in the row still appears on the page
That second check is the one the first version of this script lacked: it accepted any
'$' or the word 'free' anywhere on the page and called the row confirmed.

    python3 verify.py                # output_verified.csv
    python3 verify.py --limit 5
    python3 verify.py --csv other.csv
"""
import argparse, csv, html, os, re, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")


def flatten(raw):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", raw, flags=re.S | re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.geturl(), flatten(r.read(3_000_000).decode("utf-8", "ignore"))


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("\u201c", '"')
                  .replace("\u201d", '"')).strip().lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.path.join(HERE, "output_verified.csv"))
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.csv, encoding="utf-8")))
    if a.limit:
        rows = rows[:a.limit]

    ok = bad = 0
    for row in rows:
        name = row["Directory Name"]
        url = row["Submission URL"]
        want = norm(row.get("Evidence (verbatim)", ""))
        try:
            status, final, body = fetch(url)
        except (urllib.error.URLError, OSError, ValueError) as e:
            print(f"FAIL  {name}\n      {url}\n      fetch error: {type(e).__name__}: {e}")
            bad += 1
            continue

        found = bool(want) and want in norm(body)
        if '...' in (row.get("Evidence (verbatim)") or ""):
            print(f"WARN  {name}: evidence contains an ellipsis, so it is not verbatim")
        if status == 200 and found:
            ok += 1
            print(f"OK    {name}  [{status}]  quote present  {final}")
        else:
            bad += 1
            why = "quote NOT found on page" if status == 200 else f"HTTP {status}"
            print(f"FAIL  {name}  [{status}]  {why}\n      {url}\n      final: {final}")

    print(f"\n{ok} ok / {bad} failed / {len(rows)} rows")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

"""CrossRef照合スクリプト: manuscript.mdの参考文献をDOI経由で検証する."""

import json
import re
import sys
import urllib.request
import urllib.error

REFERENCES = [
    {
        "num": 1,
        "doi": "10.1136/bmj.307.6919.1584",
        "expected_author": "Scanlon",
        "expected_year": "1993",
        "expected_journal": "BMJ",
    },
    {
        "num": 2,
        "doi": "10.1176/appi.ajp.159.12.2110",
        "expected_author": "Näyhä",
        "expected_year": "2002",
        "expected_journal": "Am J Psychiatry",
    },
    {
        "num": 3,
        "doi": "10.1186/1471-2458-4-54",
        "expected_author": "Radun",
        "expected_year": "2004",
        "expected_journal": "BMC Public Health",
    },
    {
        "num": 4,
        "doi": "10.1136/bmj.323.7327.1443",
        "expected_author": "Phillips",
        "expected_year": "2001",
        "expected_journal": "BMJ",
    },
    {
        "num": 5,
        "doi": "10.1136/bmj.317.7174.1680",
        "expected_author": "Hira",
        "expected_year": "1998",
        "expected_journal": "BMJ",
    },
    {
        "num": 6,
        "doi": "10.3386/w25474",
        "expected_author": "Halla",
        "expected_year": "2019",
        "expected_journal": "NBER",
    },
    {
        "num": 7,
        "doi": "10.1016/j.annepidem.2012.04.016",
        "expected_author": "Ajdacic-Gross",
        "expected_year": "2012",
        "expected_journal": "Ann Epidemiol",
    },
    {
        "num": 8,
        "doi": "10.1016/j.socscimed.2016.04.034",
        "expected_author": "Matsubayashi",
        "expected_year": "2016",
        "expected_journal": "Soc Sci Med",
    },
]

URL_REFERENCES = [
    {"num": 9, "type": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Yakudoshi"},
    {"num": 10, "type": "Book", "note": "Namihira E. Kegare. Kodansha, 1985."},
    {
        "num": 11,
        "type": "Press release",
        "url": "https://prtimes.jp/main/html/rd/p/000000372.000001163.html",
    },
    {
        "num": 12,
        "type": "Database",
        "url": "https://www.ipss.go.jp/p-toukei/JMD/index-en.asp",
    },
]


def query_crossref(doi: str) -> dict | None:
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "YakudoshiVerify/1.0 (mailto:rehabilitation.collaboration@gmail.com)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("message", {})
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} for DOI {doi}")
        return None
    except Exception as e:
        print(f"  Error for DOI {doi}: {e}")
        return None


def check_url(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "YakudoshiVerify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, "OK"
    except urllib.error.HTTPError as e:
        return e.code, str(e.reason)
    except Exception as e:
        return 0, str(e)


def extract_year(msg: dict) -> str | None:
    for key in ["published-print", "published-online", "issued", "created"]:
        if key in msg:
            parts = msg[key].get("date-parts", [[]])
            if parts and parts[0]:
                return str(parts[0][0])
    return None


def extract_first_author(msg: dict) -> str | None:
    authors = msg.get("author", [])
    if authors:
        return authors[0].get("family", "")
    return None


def main():
    print("=" * 70)
    print("CrossRef Reference Verification Report")
    print("=" * 70)

    results = []

    # DOI-based references
    print("\n--- DOI-based references ([1]-[8]) ---\n")
    for ref in REFERENCES:
        num = ref["num"]
        doi = ref["doi"]
        print(f"[{num}] DOI: {doi}")

        msg = query_crossref(doi)
        if msg is None:
            results.append({"num": num, "status": "FAIL", "reason": "CrossRef lookup failed"})
            print(f"  STATUS: FAIL (CrossRef lookup failed)\n")
            continue

        issues = []

        # Check year
        cr_year = extract_year(msg)
        if cr_year and cr_year != ref["expected_year"]:
            issues.append(f"Year mismatch: manuscript={ref['expected_year']}, CrossRef={cr_year}")
        elif cr_year:
            print(f"  Year: {cr_year} OK")

        # Check first author
        cr_author = extract_first_author(msg)
        if cr_author:
            if ref["expected_author"].lower() not in cr_author.lower():
                issues.append(f"Author mismatch: manuscript={ref['expected_author']}, CrossRef={cr_author}")
            else:
                print(f"  Author: {cr_author} OK")

        # Check title
        titles = msg.get("title", [])
        title = titles[0] if titles else "N/A"
        print(f"  Title: {title[:80]}")

        # Check journal
        journals = msg.get("container-title", [])
        journal = journals[0] if journals else "N/A"
        print(f"  Journal: {journal}")

        # Check volume/pages
        volume = msg.get("volume", "N/A")
        page = msg.get("page", "N/A")
        print(f"  Volume: {volume}, Pages: {page}")

        if issues:
            for issue in issues:
                print(f"  ISSUE: {issue}")
            results.append({"num": num, "status": "WARN", "reason": "; ".join(issues)})
        else:
            results.append({"num": num, "status": "PASS"})

        status = "WARN" if issues else "PASS"
        print(f"  STATUS: {status}\n")

    # URL-based references
    print("\n--- URL/Book references ([9]-[12]) ---\n")
    for ref in URL_REFERENCES:
        num = ref["num"]
        print(f"[{num}] Type: {ref['type']}")

        if "url" in ref:
            code, reason = check_url(ref["url"])
            print(f"  URL: {ref['url']}")
            print(f"  HTTP: {code} ({reason})")
            if 200 <= code < 400:
                results.append({"num": num, "status": "PASS"})
                print(f"  STATUS: PASS\n")
            else:
                results.append({"num": num, "status": "WARN", "reason": f"HTTP {code}"})
                print(f"  STATUS: WARN (URL may be unreachable)\n")
        else:
            print(f"  Note: {ref.get('note', 'N/A')}")
            results.append({"num": num, "status": "MANUAL", "reason": "Book — manual verification needed"})
            print(f"  STATUS: MANUAL (book, cannot auto-verify)\n")

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    warn_count = sum(1 for r in results if r["status"] == "WARN")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")
    manual_count = sum(1 for r in results if r["status"] == "MANUAL")
    print(f"PASS: {pass_count}  WARN: {warn_count}  FAIL: {fail_count}  MANUAL: {manual_count}")

    for r in results:
        if r["status"] != "PASS":
            print(f"  [{r['num']}] {r['status']}: {r.get('reason', '')}")

    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

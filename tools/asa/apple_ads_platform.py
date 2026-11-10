"""Apple Ads Platform API (api.ads.apple.com/v1), portfolio-wide, READ-ONLY client.

Why this file exists next to watercleaner/asa/asa_client.py: that client is Clear Wave's
and its Air copy drives the spend guard, so it stays untouched. This one is for read
work that is not Clear Wave specific: Search Term Popularity and Impression Share
(Insights), campaign listing and campaign reports for any app in the ad account.

READ-ONLY BY CONSTRUCTION. `call()` refuses every method except GET, and refuses POST
unless the path ends in `/query` (every read in the Platform API is a POST to a
`/query` endpoint; every write is PUT, DELETE, or POST to a path that does not end in
`/query`, such as `/campaigns` or `/negative-keywords/bulk-create`). Pausing, creating
or editing campaigns is the job of watercleaner/asa, not of this file.

Credentials: the `apple-ads` service in the vault. Run through the loader so only
that service is in the environment:

    ~/Mac-Projects/local-assistant/bin/secrets run apple-ads -- \
        ~/Mac-Projects/watercleaner/asa/.venv/bin/python tools/asa/apple_ads_platform.py stp --country US TR

Needs pyjwt, cryptography and requests (the watercleaner asa venv has them).
Docs: https://developer.apple.com/documentation/apple-ads-platform-api (API 1.0,
released August 2026; Campaign Management API v5 is sunset on 2027-01-26).
"""
import argparse, csv, datetime, os, sys, time, warnings

warnings.filterwarnings("ignore", message=".*OpenSSL.*")

import jwt, requests

BASE = "https://api.ads.apple.com/v1"
AD_ACCOUNT_ID = int(os.environ.get("ASA_AD_ACCOUNT_ID", "8847170"))  # Burak Cem Sayilar, USD, PAYG

# App Store genre values the Insights endpoints accept (from the Search Term
# Popularity Query page). There is no MUSIC and no separate UTILITIES: Utilities is
# folded into PRODUCTIVITY_UTILITIES.
GENRES = ("BUSINESS", "EDUCATION", "ENTERTAINMENT", "FINANCE", "FOOD_DRINK", "GAMES",
          "HEALTH_FITNESS", "LIFESTYLE", "NEW_PUBLICATION", "PHOTO_VIDEO",
          "PRODUCTIVITY_UTILITIES", "SHOPPING", "SOCIAL_NETWORKING", "SPORTS", "TRAVEL")

STP_FIELDS = ["rankInGenre", "searchPopularityInGenre", "searchPopularity1to100", "searchPopularity1to5"]


class ApiError(SystemExit):
    """A failed call, or a response in a shape this code does not understand."""


class ReadOnlyError(RuntimeError):
    """Raised before any request leaves the machine when a call would write."""


_cache = {}


def _env(name):
    v = os.environ.get(name)
    if not v:
        raise SystemExit(f"{name} is not set. Run through: bin/secrets run apple-ads -- <command>")
    return v


def access_token():
    """Same two-step flow as v5 and as watercleaner/asa: an ES256 JWT (the client
    secret, max 180 days per Apple, we use 1 hour) exchanged at appleid for a one hour
    access token with scope `searchadsorg`. The secret goes in the form body, never in
    the URL, so an error message cannot leak it."""
    if _cache.get("token") and _cache["expires"] > time.time() + 60:
        return _cache["token"]
    now = int(time.time())
    secret = jwt.encode(
        {"sub": _env("ASA_CLIENT_ID"), "aud": "https://appleid.apple.com",
         "iat": now, "exp": now + 3600, "iss": _env("ASA_TEAM_ID")},
        open(_env("ASA_PRIVATE_KEY_PATH")).read(),
        algorithm="ES256", headers={"alg": "ES256", "kid": _env("ASA_KEY_ID")})
    r = requests.post("https://appleid.apple.com/auth/oauth2/token",
                      data={"grant_type": "client_credentials", "client_id": _env("ASA_CLIENT_ID"),
                            "client_secret": secret, "scope": "searchadsorg"},
                      headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=30)
    if r.status_code != 200:
        raise ApiError(f"access token request failed {r.status_code}: {r.text[:300]}")
    d = r.json()
    _cache.update(token=d["access_token"], expires=now + d.get("expires_in", 3600))
    return _cache["token"]


def assert_read_only(method, path):
    m = method.upper()
    if m == "GET":
        return
    if m == "POST" and path.split("?")[0].rstrip("/").endswith("/query"):
        return
    raise ReadOnlyError(f"refused {m} {path}: this client is read-only")


def call(method, path, context=True, max_retries=5, **kw):
    """Returns (status_code, parsed_body). Never raises on a 4xx, Apple puts the only
    useful diagnosis in the body. Paces itself on the RateLimit-* headers and backs
    off on 429 with Retry-After, as the Applying Rate Limits page prescribes. The
    Search Term Popularity endpoint was measured at RateLimit-Limit 5 (2026-11-10)."""
    assert_read_only(method, path)
    headers = {"Authorization": "Bearer " + access_token(), "Content-Type": "application/json"}
    if context:
        headers["X-AP-Context"] = f"adAccountId={AD_ACCOUNT_ID}"
    wait = 2
    for _ in range(max_retries):
        r = requests.request(method, BASE + path, timeout=60, headers=headers, **kw)
        if r.status_code == 429:
            time.sleep(float(r.headers.get("Retry-After") or r.headers.get("RateLimit-Reset") or wait))
            wait = min(wait * 2, 16)
            continue
        rem, reset = r.headers.get("RateLimit-Remaining"), r.headers.get("RateLimit-Reset")
        if rem is not None and reset is not None and int(rem) < 2:
            time.sleep(int(reset))
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, r.text[:500]
    raise ApiError(f"{method} {path} still rate limited after {max_retries} tries")


def query(path, filters=(), what=None):
    """Every row of an entity `/query` endpoint (campaigns, adgroups, keywords...),
    following pagination. Rows are a bare list under `result`. fetchTotalCount is
    needed here, but report and insights endpoints REJECT it (400
    REQUEST_UNRECOGNIZED_PROPERTY), so do not use this function for those."""
    rows, offset = [], 0
    while True:
        status, body = call("POST", path, json={"filters": list(filters),
                                                "pagination": {"offset": offset, "pageSize": 1000,
                                                               "fetchTotalCount": True}})
        if status >= 300 or not isinstance(body, dict) or not isinstance(body.get("result"), list):
            raise ApiError(f"{what or path} failed {status}: {str(body)[:500]}")
        rows += body["result"]
        total = (body.get("pagination") or {}).get("totalCount")
        offset += len(body["result"])
        if not body["result"] or total is None or offset >= total:
            return rows


def _rows_query(path, body, page_size=1000, limit=None):
    """Report and insights endpoints: rows under `result.rows`, no totalCount, so page
    until a short page comes back."""
    rows, offset = [], 0
    while True:
        b = dict(body, pagination={"offset": offset, "pageSize": page_size})
        status, resp = call("POST", path, json=b)
        if status >= 300 or not isinstance(resp, dict) or not isinstance((resp.get("result") or {}).get("rows"), list):
            raise ApiError(f"{path} failed {status}: {str(resp)[:500]}")
        page = resp["result"]["rows"]
        rows += page
        offset += len(page)
        if len(page) < page_size or (limit and len(rows) >= limit):
            return rows[:limit] if limit else rows


def acls():
    status, body = call("GET", "/acls", context=False)
    if status != 200:
        raise ApiError(f"acls failed {status}: {str(body)[:300]}")
    return body["result"]["acls"]


def me():
    status, body = call("GET", "/me", context=False)
    if status != 200:
        raise ApiError(f"me failed {status}: {str(body)[:300]}")
    return body["result"]


def campaigns(promoted_object_id=None):
    """All campaigns in the ad account, or only one app's. `promotedObjectId` is v5's
    `adamId` and is a string."""
    f = [{"field": "promotedObjectId", "operator": "EQUALS", "value": str(promoted_object_id)}] \
        if promoted_object_id else []
    return query("/campaigns/query", f, what="campaign query")


def campaign_report(start, end, time_zone="ORTZ", filters=(), empty_rows=True):
    """Campaign level totals. Zero metrics are absent from `totalMetrics`, read them
    with a default. Installs are `tapInstalls` (v5 `installs`)."""
    body = {"timeRange": {"start": str(start), "end": str(end), "timeZone": time_zone},
            "filters": list(filters)}
    if empty_rows:
        body["options"] = {"includeRows": ["EMPTY_METRICS"]}
    return _rows_query("/reports/apps/campaigns/query", body)


def last_complete_week(today=None):
    """Sunday to Saturday of the last week Apple has published. Weekly data is
    generated Mondays 07:00 UTC for the week before."""
    today = today or datetime.datetime.utcnow()
    d = today.date() - datetime.timedelta(days=2 if today.weekday() == 0 and today.hour < 7 else 0)
    last_sat = d - datetime.timedelta(days=(d.weekday() - 5) % 7 or 7)
    return last_sat - datetime.timedelta(days=6), last_sat


def last_complete_month(today=None):
    """Monthly data is refreshed on the 5th (UTC) for the month before."""
    today = (today or datetime.datetime.utcnow()).date()
    first = today.replace(day=1)
    if today.day < 5:
        first = (first - datetime.timedelta(days=1)).replace(day=1)
    end = first - datetime.timedelta(days=1)
    return end.replace(day=1), end


def search_term_popularity(countries, genres=None, granularity="MONTHLY", start=None, end=None,
                           term_contains=None, sort=("rankInGenre", "ASC"), limit=None):
    """Most searched App Store terms per country and genre. Measured on 2026-11-10:
    exactly 500 terms per country and genre, so it is a head-term list, niche terms
    (speaker cleaner, beekeeping, 3d print cost) are not in it. `genres=None` means all
    genres. `term_contains` is case-insensitive."""
    if start is None:
        start, end = last_complete_month() if granularity == "MONTHLY" else last_complete_week()
    f = [{"field": "countryOrRegion", "operator": "IN", "value": list(countries)}]
    if genres:
        bad = [g for g in genres if g not in GENRES]
        if bad:
            raise SystemExit(f"unknown genre {bad}, allowed: {', '.join(GENRES)}")
        f.append({"field": "genre", "operator": "IN", "value": list(genres)})
    if term_contains:
        f.append({"field": "searchTerm", "operator": "CONTAINS", "value": term_contains})
    body = {"fields": STP_FIELDS, "filters": f,
            "timeRange": {"start": str(start), "end": str(end), "granularity": granularity},
            "sorting": [{"field": sort[0], "order": sort[1]}]}
    return _rows_query("/insights/apps/search-term-popularity/query", body, page_size=5000, limit=limit)


def impression_share(promoted_object_ids, start, end, countries=None, granularity="DAILY",
                     report_type="ALL_SLOTS"):
    """Share of impressions our app got per search term. DAILY spans at most 30 days,
    WEEKLY_SUN_SAT at most 4 weeks starting on a Sunday. Terms under 10 impressions
    are suppressed, so a campaign that barely served returns nothing."""
    f = [{"field": "promotedObjectId", "operator": "IN", "value": [str(i) for i in promoted_object_ids]}]
    if countries:
        f.append({"field": "countryOrRegion", "operator": "IN", "value": list(countries)})
    body = {"filters": f, "options": {"impressionShareReportType": report_type},
            "timeRange": {"start": str(start), "end": str(end), "granularity": granularity}}
    return _rows_query("/insights/apps/impression-share/query", body, page_size=1000)


def money(m):
    return float((m or {}).get("amount") or 0)


def _write_tsv(path, rows):
    cols = ["month", "week", "countryOrRegion", "genre", "rankInGenre", "searchTerm",
            "searchPopularityInGenre", "searchPopularity1to100", "searchPopularity1to5"]
    cols = [c for c in cols if any(c in r for r in rows)]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    p = argparse.ArgumentParser(description="Apple Ads Platform API, read-only")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stp", help="Search Term Popularity")
    s.add_argument("--country", nargs="+", default=["US"])
    s.add_argument("--genre", nargs="*", default=None)
    s.add_argument("--weekly", action="store_true")
    s.add_argument("--contains")
    s.add_argument("--top", type=int, default=30, help="rows per country and genre")
    s.add_argument("--out", help="write TSV here")
    sub.add_parser("campaigns", help="list campaigns")
    a = p.parse_args(argv)

    if a.cmd == "campaigns":
        for c in campaigns():
            print(c["id"], c["status"], c.get("systemStatus"), c.get("promotedObjectId"), c["name"])
        return
    gran = "WEEKLY_SUN_SAT" if a.weekly else "MONTHLY"
    rows = search_term_popularity(a.country, a.genre, gran, term_contains=a.contains)
    seen, kept = {}, []
    for r in rows:
        k = (r["countryOrRegion"], r["genre"])
        seen[k] = seen.get(k, 0) + 1
        if seen[k] <= a.top:
            kept.append(r)
    if a.out:
        _write_tsv(a.out, kept)
    for r in kept:
        print(r.get("month") or r.get("week"), r["countryOrRegion"], r["genre"], r.get("rankInGenre"),
              r["searchTerm"], r.get("searchPopularity1to100"), sep="\t")


if __name__ == "__main__":
    main()

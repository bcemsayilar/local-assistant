"""Tests for apple_ads_platform.py.

Offline part (no network, no credentials): the read-only guard and the date helpers.
Live part (only with --live, through the vault): read calls against the real ad
account. Nothing here writes; the guard is asserted before any live call.

    ~/Mac-Projects/watercleaner/asa/.venv/bin/python tools/asa/test_apple_ads_platform.py
    ~/Mac-Projects/local-assistant/bin/secrets run apple-ads -- \
        ~/Mac-Projects/watercleaner/asa/.venv/bin/python tools/asa/test_apple_ads_platform.py --live
"""
import datetime, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apple_ads_platform as ap

CLEAR_WAVE = 6783528945


def test_guard():
    for m, p in (("GET", "/acls"), ("POST", "/campaigns/query"), ("POST", "/reports/apps/campaigns/query"),
                 ("POST", "/insights/apps/search-term-popularity/query")):
        ap.assert_read_only(m, p)
    for m, p in (("PUT", "/campaigns/1"), ("DELETE", "/campaigns/1"), ("POST", "/campaigns"),
                 ("POST", "/negative-keywords/bulk-create"), ("PATCH", "/campaigns/1"),
                 ("POST", "/keywords/bulk-update")):
        try:
            ap.assert_read_only(m, p)
        except ap.ReadOnlyError:
            continue
        raise AssertionError(f"guard let {m} {p} through")
    # call() must refuse before touching the network or credentials
    try:
        ap.call("PUT", "/campaigns/1", json={"status": "PAUSED"})
    except ap.ReadOnlyError:
        pass
    else:
        raise AssertionError("call() let a PUT through")
    print("ok guard")


def test_dates():
    T = lambda s: datetime.datetime.fromisoformat(s)
    assert ap.last_complete_week(T("2026-11-10T12:00")) == (datetime.date(2026, 11, 1), datetime.date(2026, 11, 7))
    assert ap.last_complete_week(T("2026-11-09T06:00")) == (datetime.date(2026, 10, 25), datetime.date(2026, 10, 31))
    assert ap.last_complete_week(T("2026-11-09T08:00")) == (datetime.date(2026, 11, 1), datetime.date(2026, 11, 7))
    assert ap.last_complete_week(T("2026-11-14T12:00")) == (datetime.date(2026, 11, 1), datetime.date(2026, 11, 7))
    assert ap.last_complete_month(T("2026-11-10T00:00")) == (datetime.date(2026, 10, 1), datetime.date(2026, 10, 31))
    assert ap.last_complete_month(T("2026-11-03T00:00")) == (datetime.date(2026, 9, 1), datetime.date(2026, 9, 30))
    print("ok dates")


def test_live():
    acl = ap.acls()
    assert any(a["adAccount"]["id"] == ap.AD_ACCOUNT_ID for a in acl), acl
    print("ok acls", [(a["adAccount"]["id"], a["roles"]) for a in acl])
    print("ok me", ap.me())
    cs = ap.campaigns(CLEAR_WAVE)
    assert cs and all(c["promotedObjectId"] == str(CLEAR_WAVE) for c in cs)
    print("ok campaigns", len(cs))
    end = datetime.date.today()
    rep = ap.campaign_report(end - datetime.timedelta(days=7), end)
    print("ok campaign_report rows", len(rep), "spend 7d", round(sum(ap.money(r["totalMetrics"].get("localSpend")) for r in rep), 2))
    stp = ap.search_term_popularity(["US"], ["PRODUCTIVITY_UTILITIES"], limit=5)
    assert len(stp) == 5 and stp[0]["rankInGenre"] == 1, stp
    print("ok stp", [r["searchTerm"] for r in stp])
    s, e = end - datetime.timedelta(days=8), end - datetime.timedelta(days=2)
    imp = ap.impression_share([CLEAR_WAVE], s, e, ["US"])
    print("ok impression_share rows", len(imp), imp[:2])


if __name__ == "__main__":
    test_guard()
    test_dates()
    if "--live" in sys.argv:
        test_live()

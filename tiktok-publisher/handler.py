"""TikTok Content Posting API arka ucu (Lambda function URL).

Tarayici arayuzu parallaxtechnologies.net/publisher/ altinda, bu fonksiyon yalniz token takasi ve TikTok API
cagrilari icin. Token'lar tarayiciya inmez, DynamoDB'de oturum kimligiyle tutulur. Yalniz standart kutuphane.
"""
import base64
import json
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request

import boto3

TABLE = boto3.resource("dynamodb").Table(os.environ["TABLE"])
KEY = os.environ["TIKTOK_CLIENT_KEY"]
SECRET = os.environ["TIKTOK_CLIENT_SECRET"]
REDIRECT = os.environ["REDIRECT_URI"]
ORIGIN = os.environ["ALLOWED_ORIGIN"]
SCOPES = "user.info.basic,video.upload,video.publish"
API = "https://open.tiktokapis.com"
MAX_VIDEO_BYTES = 4 * 1024 * 1024  # Lambda istek siniri, demo icin; uretim yuklemesi cli ile


def resp(code, body):
    return {"statusCode": code, "headers": {"content-type": "application/json"}, "body": json.dumps(body)}


def http(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"error": raw.decode("utf-8", "replace")[:300]}


def token_call(fields):
    body = urllib.parse.urlencode({"client_key": KEY, "client_secret": SECRET, **fields}).encode()
    return http(API + "/v2/oauth/token/", body, {"content-type": "application/x-www-form-urlencoded"})


def api(sid, path, payload):
    """Oturumun access token'i ile TikTok'a JSON POST. Suresi dolduysa yeniler."""
    item = TABLE.get_item(Key={"pk": "sess", "sk": sid}).get("Item")
    if not item:
        return 401, {"error": "oturum yok"}
    if item["expires_at"] < time.time() + 60:
        code, tok = token_call({"grant_type": "refresh_token", "refresh_token": item["refresh_token"]})
        if code != 200 or "access_token" not in tok:
            # refresh token rotasyonu: baska bir istek az once yenilemis olabilir, guncel kaydi bir kez daha oku
            fresh = TABLE.get_item(Key={"pk": "sess", "sk": sid}).get("Item")
            if fresh and fresh["refresh_token"] != item["refresh_token"] and fresh["expires_at"] > time.time() + 60:
                item = fresh
            else:
                return 401, {"error": "token yenilenemedi"}
        else:
            now = int(time.time())
            rexp = now + int(tok.get("refresh_expires_in", 180 * 86400))
            item.update(access_token=tok["access_token"], refresh_token=tok.get("refresh_token", item["refresh_token"]),
                        expires_at=now + int(tok["expires_in"]), refresh_expires_at=rexp, ttl=rexp + 86400)
            TABLE.put_item(Item=item)
    return http(API + path, json.dumps(payload).encode(),
                {"authorization": "Bearer " + item["access_token"], "content-type": "application/json; charset=UTF-8"})


def handler(event, _ctx):
    path = event.get("rawPath", "")
    method = event["requestContext"]["http"]["method"]
    if method == "OPTIONS":
        return {"statusCode": 204, "body": ""}
    if method != "POST":
        return resp(405, {"error": "yalniz POST"})
    body = json.loads(event.get("body") or "{}")

    if path == "/api/auth-url":
        state = secrets.token_urlsafe(24)
        TABLE.put_item(Item={"pk": "state", "sk": state, "ttl": int(time.time()) + 600})
        q = urllib.parse.urlencode({"client_key": KEY, "scope": SCOPES, "response_type": "code",
                                    "redirect_uri": REDIRECT, "state": state})
        return resp(200, {"url": "https://www.tiktok.com/v2/auth/authorize/?" + q})

    if path == "/api/exchange":
        st = TABLE.get_item(Key={"pk": "state", "sk": body.get("state", "")}).get("Item")
        if not st:
            return resp(400, {"error": "state gecersiz"})
        TABLE.delete_item(Key={"pk": "state", "sk": body["state"]})
        code, tok = token_call({"code": body.get("code", ""), "grant_type": "authorization_code", "redirect_uri": REDIRECT})
        if code != 200 or "access_token" not in tok:
            return resp(400, {"error": "takas basarisiz", "detail": tok.get("error_description") or tok.get("error")})
        sid = secrets.token_urlsafe(32)
        TABLE.put_item(Item={"pk": "sess", "sk": sid, "open_id": tok["open_id"], "access_token": tok["access_token"],
                             "refresh_token": tok["refresh_token"], "expires_at": int(time.time()) + int(tok["expires_in"]),
                             "refresh_expires_at": int(time.time()) + int(tok.get("refresh_expires_in", 180 * 86400)),
                             "scope": tok.get("scope", ""),
                             "ttl": int(time.time()) + int(tok.get("refresh_expires_in", 180 * 86400)) + 86400})
        return resp(200, {"sid": sid})

    sid = body.get("sid", "")
    if path == "/api/creator":
        code, out = api(sid, "/v2/post/publish/creator_info/query/", {})
        return resp(code, out)

    if path == "/api/post":
        raw = base64.b64decode(body["video_b64"])
        if not raw or len(raw) > MAX_VIDEO_BYTES:
            return resp(400, {"error": "video 4 MB sinirini asiyor ya da bos"})
        info = body["post_info"]
        post = {"title": info.get("title", "")[:2200], "privacy_level": info["privacy_level"],
                "disable_comment": bool(info.get("disable_comment")), "disable_duet": bool(info.get("disable_duet")),
                "disable_stitch": bool(info.get("disable_stitch")), "video_cover_timestamp_ms": 1000,
                "brand_content_toggle": bool(info.get("brand_content_toggle")),
                "brand_organic_toggle": bool(info.get("brand_organic_toggle")), "is_aigc": bool(info.get("is_aigc"))}
        code, init = api(sid, "/v2/post/publish/video/init/", {
            "post_info": post,
            "source_info": {"source": "FILE_UPLOAD", "video_size": len(raw), "chunk_size": len(raw), "total_chunk_count": 1}})
        data = init.get("data") or {}
        if code != 200 or "upload_url" not in data:
            return resp(400, {"error": "init basarisiz", "detail": init})
        up, _ = http(data["upload_url"], raw, {"content-type": "video/mp4", "content-length": str(len(raw)),
                                                "content-range": "bytes 0-%d/%d" % (len(raw) - 1, len(raw))}, "PUT")
        return resp(200 if up in (200, 201) else 502, {"publish_id": data["publish_id"], "upload_status": up})

    if path == "/api/status":
        code, out = api(sid, "/v2/post/publish/status/fetch/", {"publish_id": body.get("publish_id", "")})
        return resp(code, out)

    return resp(404, {"error": "yok"})

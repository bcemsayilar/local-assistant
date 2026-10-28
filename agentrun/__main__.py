"""CLI: python3 -m agentrun run|doctor|setup|limits ...   (wrapper: bin/agent)"""
import argparse, json, os, sys, time
from pathlib import Path
from . import core


def cmd_run(a):
    prompt = a.prompt if a.prompt and a.prompt != "-" else sys.stdin.read()
    sess = core.Sessions(a.store) if a.session else None
    sid = None if a.fresh or not sess else sess.get(a.session, a.provider or core.provider_order(a.providers)[0])
    r = core.run(prompt, provider=a.provider, providers=a.providers, cwd=a.cwd, tier=a.tier, model=a.model,
                 session_id=sid, timeout=a.timeout, idle_s=a.idle)
    if r.ok and sess and r.session_id and not a.fresh:
        sess.put(a.session, r.provider, r.session_id)
    if a.json:
        print(json.dumps(r.__dict__, ensure_ascii=False))
    else:
        print(r.text if r.ok else "HATA: " + (r.error or "bilinmeyen") + "  [" + ", ".join("%s=%s" % t for t in r.tried) + "]")
    return 0 if r.ok else (75 if r.limit else 1)


def cmd_doctor(a):
    s = core.status()
    print("sira: " + " > ".join(s["order"]))
    print("global talimat: " + s["global_instructions"])
    print("anahtar dosyasi: " + s["env_file"] + "  anahtarlar: " + ", ".join(s["env_keys"]))
    for n, p in s["providers"].items():
        print("%-7s %s  %s%s" % (n, p["version"] or "KURULU DEGIL", p["bin"], ("  LIMITTE, bitis " + p["parked_until"]) if p["parked_until"] else ""))
    return 0


def cmd_setup(a):
    """Create config, import API keys from the existing .env files (values are never printed), prepare the Gemini home."""
    core.CONF_DIR.mkdir(parents=True, exist_ok=True)
    if not core.CONF_FILE.exists():
        core.CONF_FILE.write_text(json.dumps({"providers": core.DEFAULT_CONF["providers"], "codex_auth": "login"}, indent=2))
    have = core.read_env_file()
    sources = [(Path.home() / "Mac-Projects/local-assistant/finance_agent.env", {"GEMINI_FREE_APIKEY": "GEMINI_API_KEY"}),
               (Path.home() / "Mac-Projects/local-assistant/.env", {"OPENAI_API_APIKEY": "CODEX_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CODE_OAUTH_TOKEN"}),
               (Path.home() / "Projects/local-assistant/.env", {"OPENAI_API_APIKEY": "CODEX_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CODE_OAUTH_TOKEN"}),
               (Path.home() / "Projects/local-assistant/finance_agent.env", {"GEMINI_FREE_APIKEY": "GEMINI_API_KEY"})]
    added = []
    for path, mp in sources:
        try:
            lines = path.read_text().splitlines()
        except OSError:
            continue
        for l in lines:
            if "=" in l and not l.lstrip().startswith("#"):
                k, v = l.split("=", 1)
                if k.strip() in mp and mp[k.strip()] not in have and v.strip():
                    have[mp[k.strip()]] = v.strip().strip('"').strip("'"); added.append(mp[k.strip()])
    core.ENV_FILE.write_text("".join("%s=%s\n" % kv for kv in sorted(have.items())))
    os.chmod(core.ENV_FILE, 0o600)
    core.ensure_gemini_home()
    print("hazir. eklenen anahtar adlari: %s" % (", ".join(added) or "yok"))
    return cmd_doctor(a)


def cmd_limits(a):
    d = core._limits()
    for n, v in d.items():
        print("%s: bitis %s  %s" % (n, time.strftime("%d.%m %H:%M", time.localtime(v.get("until", 0))), v.get("message", "")))
    if a.clear:
        for n in list(d):
            core.unpark(n)
        print("limit kayitlari temizlendi")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="agent")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("prompt", nargs="?"); r.add_argument("--provider"); r.add_argument("--providers")
    r.add_argument("--cwd"); r.add_argument("--tier", default="default"); r.add_argument("--model"); r.add_argument("--session")
    r.add_argument("--store", default=str(core.CONF_DIR / "agent-sessions.json")); r.add_argument("--fresh", action="store_true")
    r.add_argument("--timeout", type=int, default=1800); r.add_argument("--idle", type=int, default=0); r.add_argument("--json", action="store_true")
    r.set_defaults(fn=cmd_run)
    sub.add_parser("doctor").set_defaults(fn=cmd_doctor)
    sub.add_parser("setup").set_defaults(fn=cmd_setup)
    l = sub.add_parser("limits"); l.add_argument("--clear", action="store_true"); l.set_defaults(fn=cmd_limits)
    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()

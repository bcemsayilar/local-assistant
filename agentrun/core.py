"""agentrun: provider independent headless agent runner (Claude Code, Codex CLI, Gemini CLI).

One call, any provider: run(prompt, provider="codex") or run(prompt) with the order taken from AGENT_PROVIDER or
~/.config/parallax/agent.json. When a provider reports a usage limit it is parked until its reset time and the next
provider in the order runs the same prompt, so a weekly limit on one vendor does not stop the Air jobs.

Standard library only; works on the Mac Pro and on the Air.
"""
import json, os, re, shutil, subprocess, tempfile, threading, time, glob
from dataclasses import dataclass, field
from pathlib import Path

HOME = Path.home()
CONF_DIR = Path(os.environ.get("AGENT_CONF_DIR") or HOME / ".config" / "parallax")
CONF_FILE = CONF_DIR / "agent.json"
ENV_FILE = CONF_DIR / "agent.env"            # KEY=VALUE secrets for the CLIs, mode 600, never committed
LIMIT_FILE = CONF_DIR / "agent-limits.json"
GEMINI_HOME = CONF_DIR / "gemini-home"       # managed GEMINI_CLI_HOME so headless runs never touch the interactive login
GLOBAL_INSTRUCTIONS = HOME / ".claude" / "CLAUDE.md"   # single source of the global rules; Codex and Gemini read it too
PROVIDERS = ("claude", "codex", "gemini")
DEFAULT_WAIT_S = 1800
LIMIT_RE = re.compile(r"usage limit|hit your .{0,12}limit|limit reached|rate[ _-]?limit|quota|resource[_ ]exhausted|"
                      r"\b429\b|\b529\b|too many requests|overloaded|credit balance|insufficient[_ ]quota|try again at", re.I)

DEFAULT_CONF = {
    "providers": ["claude", "codex", "gemini"],
    "models": {                                    # tier -> model name; None means "the CLI's own default"
        "claude": {"default": None, "fast": "haiku", "strong": "opus"},
        "codex": {"default": None, "fast": None, "strong": None},
        "gemini": {"default": None, "fast": "gemini-3-flash-preview", "strong": None},
    },
    "codex_auth": "login",                         # "login" = ChatGPT subscription, "api_key" = pay per use via CODEX_API_KEY
    "gemini_auth": "api_key",                      # personal OAuth was retired for the CLI; the key comes from agent.env
    "claude_auth": "login",                        # "login" = Max subscription (OAuth token), "api_key" = pay per use, billed to the Console org the key belongs to
    "claude_api_key_env": "CLAUDE_API_KEY_PERSONAL",   # env var holding that key (agent.env); CLAUDE_API_KEY is the Parallax org key
}


@dataclass
class Result:
    ok: bool = False
    text: str = ""
    session_id: str = ""
    provider: str = ""
    limit: bool = False          # a usage or rate limit stopped this provider
    reset: int = 0               # epoch when the limit is expected to lift, 0 if unknown
    error: str = ""
    tried: list = field(default_factory=list)   # [(provider, "ok" | "limit" | "error" | "missing" | "parked")]


def load_conf() -> dict:
    conf = json.loads(json.dumps(DEFAULT_CONF))
    for k, env in (("codex_auth", "AGENT_CODEX_AUTH"), ("gemini_auth", "AGENT_GEMINI_AUTH"), ("claude_auth", "AGENT_CLAUDE_AUTH")):
        if os.environ.get(env):
            conf[k] = os.environ[env]
    try:
        user = json.loads(CONF_FILE.read_text())
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(conf.get(k), dict):
                for kk, vv in v.items():
                    conf[k][kk] = {**conf[k].get(kk, {}), **vv} if isinstance(vv, dict) and isinstance(conf[k].get(kk), dict) else vv
            else:
                conf[k] = v
    except (OSError, ValueError):
        pass
    for k, env in (("codex_auth", "AGENT_CODEX_AUTH"), ("gemini_auth", "AGENT_GEMINI_AUTH"), ("claude_auth", "AGENT_CLAUDE_AUTH")):
        if os.environ.get(env):
            conf[k] = os.environ[env]
    return conf


def provider_order(explicit=None) -> list:
    raw = explicit or os.environ.get("AGENT_PROVIDER") or load_conf()["providers"]
    names = [p.strip() for p in (raw.split(",") if isinstance(raw, str) else raw) if p and p.strip()]
    return [p for p in names if p in PROVIDERS] or list(PROVIDERS)


def read_env_file() -> dict:
    out = {}
    try:
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def _extra_paths() -> list:
    paths = [str(HOME / ".local/bin"), "/opt/homebrew/bin", "/usr/local/bin"]
    paths += sorted(glob.glob(str(HOME / ".nvm/versions/node/*/bin")), reverse=True)
    return paths


def build_env(extra=None) -> dict:
    env = dict(os.environ)
    env["PATH"] = ":".join(_extra_paths() + [env.get("PATH", "/usr/bin:/bin")])
    env.update(read_env_file())
    if extra:
        env.update(extra)
    return env


def find_bin(name: str, env=None):
    return shutil.which(name, path=(env or build_env())["PATH"])


# ---------------------------------------------------------------- limits

def _limits() -> dict:
    try:
        return json.loads(LIMIT_FILE.read_text())
    except (OSError, ValueError):
        return {}


def parked_until(provider: str) -> int:
    d = _limits().get(provider) or {}
    return int(d.get("until", 0)) if time.time() < d.get("until", 0) else 0


def park(provider: str, reset: int, message: str):
    d = _limits()
    d[provider] = {"until": reset or int(time.time()) + DEFAULT_WAIT_S, "message": message[:300],
                   "at": time.strftime("%Y-%m-%d %H:%M:%S"), "known": bool(reset)}
    CONF_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(LIMIT_FILE) + ".tmp"
    Path(tmp).write_text(json.dumps(d, ensure_ascii=False))
    os.replace(tmp, LIMIT_FILE)


def unpark(provider: str):
    d = _limits()
    if d.pop(provider, None) is not None:
        Path(str(LIMIT_FILE)).write_text(json.dumps(d, ensure_ascii=False))


def _parse_reset(text: str) -> int:
    """Best effort: 'try again at Nov 24th, 2026 10:09 PM' or a 10 digit epoch after a pipe."""
    m = re.search(r"\|(\d{10})\b", text or "")
    if m:
        return int(m.group(1))
    m = re.search(r"resets (\d{1,2})(?::(\d{2}))?\s*(am|pm)", text or "", re.I)   # "resets 5:30pm (Europe/Istanbul)"
    if m:
        h, mi, ap = int(m.group(1)) % 12, int(m.group(2) or 0), m.group(3).lower()
        h += 12 if ap == "pm" else 0
        now = time.localtime()
        t = time.mktime((now.tm_year, now.tm_mon, now.tm_mday, h, mi, 0, 0, 0, -1))
        return int(t if t > time.time() else t + 86400)
    m = re.search(r"try again at ([A-Z][a-z]{2}) (\d{1,2})(?:st|nd|rd|th)?, (\d{4}) (\d{1,2}):(\d{2}) (AM|PM)", text or "")
    if m:
        try:
            return int(time.mktime(time.strptime("%s %s %s %s:%s %s" % m.groups(), "%b %d %Y %I:%M %p")))
        except ValueError:
            return 0
    return 0


# ---------------------------------------------------------------- sessions

class Sessions:
    """key -> {provider: session id}. Reads the old Telegram format (key -> claude id string)."""

    def __init__(self, path):
        self.path = Path(path)

    def _all(self) -> dict:
        try:
            raw = json.loads(self.path.read_text())
        except (OSError, ValueError):
            return {}
        return {k: ({"claude": v} if isinstance(v, str) else v) for k, v in raw.items()}

    def get(self, key, provider):
        return (self._all().get(str(key)) or {}).get(provider)

    def put(self, key, provider, sid):
        d = self._all()
        d.setdefault(str(key), {})[provider] = sid
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(d))

    def drop(self, key, provider=None):
        d = self._all()
        if provider:
            (d.get(str(key)) or {}).pop(provider, None)
        else:
            d.pop(str(key), None)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(d))


# ---------------------------------------------------------------- provider adapters

def _jsonl(text):
    for line in (text or "").splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except ValueError:
                continue


def _claude(prompt, sid, model, conf, env, cwd, tmp):
    cmd = [find_bin("claude", env) or "claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions"]
    if sid:
        cmd += ["--resume", sid]
    if model:
        cmd += ["--model", model]
    env = dict(env)
    key = env.get(conf.get("claude_api_key_env") or "CLAUDE_API_KEY_PERSONAL") or env.get("CLAUDE_API_KEY")
    if conf.get("claude_auth") == "api_key" and key:
        env["ANTHROPIC_API_KEY"] = key
        env.pop("CLAUDE_CODE_OAUTH_TOKEN", None)   # pay per use was chosen on purpose, so the subscription token stays out
    else:
        env.pop("ANTHROPIC_API_KEY", None)         # subscription login unless pay per use was chosen on purpose

    def parse(out, err, rc):
        res = Result(provider="claude")
        rejected = False
        for d in _jsonl(out):
            if d.get("type") == "rate_limit_event":
                info = d.get("rate_limit_info") or {}
                if info.get("status") == "rejected":
                    rejected, res.reset = True, int(info.get("resetsAt") or 0)
            elif d.get("type") == "result":
                res.text, res.session_id = str(d.get("result") or ""), d.get("session_id") or ""
                res.error = res.text if d.get("is_error") else ""
        if not res.text and not res.error:
            res.error = (err or out or "")[-500:]
        res.limit = rejected or bool(res.error and LIMIT_RE.search(res.error))
        res.reset = res.reset or (_parse_reset(res.error) if res.limit else 0)
        res.ok = not res.error and not res.limit and rc == 0 and bool(res.text)
        return res

    return cmd, parse, env


def _codex(prompt, sid, model, conf, env, cwd, tmp):
    last = os.path.join(tmp, "codex-last.txt")
    cmd = [find_bin("codex", env) or "codex", "exec"] + (["resume", sid] if sid else [])
    cmd += ["--json", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", "-o", last]
    if model:
        cmd += ["-m", model]
    cmd += ["-c", 'project_doc_fallback_filenames=["CLAUDE.md"]', "-c", "project_doc_max_bytes=262144", prompt]
    env = dict(env)
    if conf.get("codex_auth") == "api_key" and env.get("CODEX_API_KEY"):
        pass  # codex exec reads CODEX_API_KEY itself
    else:
        env.pop("CODEX_API_KEY", None)   # subscription login unless pay per use was chosen on purpose

    def parse(out, err, rc):
        res = Result(provider="codex")
        msgs, errors = [], []
        for d in _jsonl(out):
            t = d.get("type")
            if t == "thread.started":
                res.session_id = d.get("thread_id") or ""
            elif t == "item.completed" and (d.get("item") or {}).get("type") == "agent_message":
                msgs.append((d["item"].get("text") or ""))
            elif t in ("error", "turn.failed"):
                m = d.get("message") or (d.get("error") or {}).get("message") or ""
                if m:
                    errors.append(m)
        try:
            res.text = Path(last).read_text().strip()
        except OSError:
            res.text = ""
        res.text = res.text or (msgs[-1].strip() if msgs else "")
        res.error = "" if (res.text and rc == 0) else ("; ".join(errors) or (err or "")[-500:])
        res.limit = bool(res.error and LIMIT_RE.search(res.error))
        res.reset = _parse_reset(res.error) if res.limit else 0
        res.ok = bool(res.text) and rc == 0 and not res.limit
        return res

    return cmd, parse, env


def ensure_gemini_home():
    """Managed GEMINI_CLI_HOME: API key auth, CLAUDE.md and AGENTS.md as context files, global rules imported."""
    s = GEMINI_HOME / ".gemini"
    s.mkdir(parents=True, exist_ok=True)
    settings = {"security": {"auth": {"selectedType": "gemini-api-key"}},
                "context": {"fileName": ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]},
                "general": {"previewFeatures": True, "checkpointing": {"enabled": False}},
                "ui": {"hideBanner": True}}
    (s / "settings.json").write_text(json.dumps(settings, indent=2))
    (s / "GEMINI.md").write_text("@%s\n" % GLOBAL_INSTRUCTIONS)
    return GEMINI_HOME


def _gemini(prompt, sid, model, conf, env, cwd, tmp):
    env = dict(env)
    env["GEMINI_CLI_HOME"] = str(ensure_gemini_home())
    cmd = [find_bin("gemini", env) or "gemini", "-p", prompt, "-o", "json", "--skip-trust", "--approval-mode", "yolo"]
    if sid:
        cmd += ["--resume", sid]
    if model:
        cmd += ["-m", model]

    def parse(out, err, rc):
        res = Result(provider="gemini")
        data = None
        a, b = out.find("{"), out.rfind("}")
        if a >= 0 and b > a:
            try:
                data = json.loads(out[a:b + 1])
            except ValueError:
                data = None
        if isinstance(data, dict):
            res.text = str(data.get("response") or "").strip()
            res.session_id = data.get("session_id") or ""
            if data.get("error"):
                res.error = json.dumps(data["error"])[:500]
        res.error = res.error or ("" if (res.text and rc == 0) else (err or out or "")[-500:])
        res.limit = bool(res.error and LIMIT_RE.search(res.error))
        res.reset = _parse_reset(res.error) if res.limit else 0
        res.ok = bool(res.text) and rc == 0 and not res.limit
        return res

    return cmd, parse, env


ADAPTERS = {"claude": _claude, "codex": _codex, "gemini": _gemini}


# ---------------------------------------------------------------- runner

def _exec(cmd, env, cwd, timeout, idle_s, idle_tool_s=0):
    """Run the CLI, kill it on a hard timeout or when it prints nothing for idle_s seconds. Returns (rc, out, err, why)."""
    p = subprocess.Popen(cmd, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, errors="replace", start_new_session=True)
    state = {"last": time.time(), "tool": False}
    out_lines, err_chunks = [], []

    def pump_out():
        for line in p.stdout:
            state["last"] = time.time()
            out_lines.append(line)
            if '"type":"assistant"' in line:        # Claude stream-json: a tool call is pending until the user event
                state["tool"] = '"tool_use"' in line
            elif '"type":"user"' in line:
                state["tool"] = False

    def pump_err():
        for chunk in p.stderr:
            err_chunks.append(chunk)

    t1, t2 = threading.Thread(target=pump_out, daemon=True), threading.Thread(target=pump_err, daemon=True)
    t1.start(); t2.start()
    start, why = time.time(), ""
    while p.poll() is None:
        now = time.time()
        if timeout and now - start > timeout:
            why = "timeout"
        elif idle_s and now - state["last"] > (max(idle_s, idle_tool_s) if state["tool"] else idle_s):
            why = "idle"
        if why:
            try:
                os.killpg(p.pid, 9)
            except OSError:
                p.kill()
            break
        time.sleep(0.5)
    p.wait()
    t1.join(2); t2.join(2)
    return p.returncode, "".join(out_lines), "".join(err_chunks), why


def run(prompt: str, *, provider=None, providers=None, cwd=None, tier="default", model=None, session_id=None,
        timeout=1800, idle_s=0, idle_tool_s=0, notify=None) -> Result:
    """Run one agent turn. provider pins a single provider; otherwise the configured order with limit failover.

    session_id is a dict {provider: id} or a single id used for the first provider tried; ids are provider specific.
    notify(text) is called once when every provider in the order is parked or failed on a limit.
    """
    conf = load_conf()
    order = [provider] if provider else provider_order(providers)
    cwd = Path(cwd or HOME)
    env0 = build_env()
    tried, last = [], Result()
    tmp = tempfile.mkdtemp(prefix="agentrun-")
    try:
        for i, name in enumerate(order):
            if name not in ADAPTERS:
                continue
            until = parked_until(name)
            if until:
                tried.append((name, "parked")); continue
            if not find_bin(name, env0):
                tried.append((name, "missing")); continue
            mdl = model or (conf["models"].get(name) or {}).get(tier)
            sid = session_id.get(name) if isinstance(session_id, dict) else (session_id if i == 0 else None)
            cmd, parse, env = ADAPTERS[name](prompt, sid, mdl, conf, env0, cwd, tmp)
            rc, out, err, why = _exec(cmd, env, cwd, timeout, idle_s, idle_tool_s)
            if why:
                res = Result(provider=name, error="%s: no result (%s)" % (name, "hard timeout" if why == "timeout" else "idle"))
            else:
                res = parse(out, err, rc)
            if res.limit:
                park(name, res.reset, res.error)
                tried.append((name, "limit"))
            elif res.ok:
                unpark(name)
                tried.append((name, "ok"))
                res.tried = tried
                return res
            else:
                tried.append((name, "error"))
            last = res
        last.tried = tried
        if not last.provider:
            last.error = last.error or "no provider available: " + ", ".join("%s=%s" % t for t in tried)
        if tried and all(s in ("limit", "parked", "missing") for _, s in tried) and any(s in ("limit", "parked") for _, s in tried):
            waits = [parked_until(n) for n in order if parked_until(n)]
            last.limit = True
            last.reset = min(waits) if waits else 0
            if notify:
                try:
                    notify("AGENT LIMITI: tum saglayicilar limitte (%s)." % ", ".join("%s=%s" % t for t in tried))
                except Exception:
                    pass
        return last
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def status() -> dict:
    """What `agent doctor` prints: which CLIs exist, config, parked providers."""
    env = build_env()
    conf = load_conf()
    out = {"order": provider_order(), "conf_file": str(CONF_FILE), "env_file": str(ENV_FILE) + (" (var)" if ENV_FILE.exists() else " (yok)"),
           "global_instructions": str(GLOBAL_INSTRUCTIONS) + ("" if GLOBAL_INSTRUCTIONS.exists() else " (YOK)"), "providers": {}}
    for n in PROVIDERS:
        b = find_bin(n, env)
        v = ""
        if b:
            try:
                v = subprocess.run([b, "--version"], capture_output=True, text=True, timeout=20, env=env).stdout.strip().splitlines()[0]
            except Exception:
                v = "?"
        u = parked_until(n)
        out["providers"][n] = {"bin": b or "", "version": v, "parked_until": time.strftime("%d.%m %H:%M", time.localtime(u)) if u else "",
                               "models": conf["models"].get(n)}
    out["env_keys"] = sorted(k for k in read_env_file() if k.endswith(("KEY", "TOKEN")))
    return out

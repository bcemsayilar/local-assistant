#!/usr/bin/env python3
# ONEMLI: Bu script Mac Air uzerinde calistirilmali (SSH ile baglan) veya SSH tunnel kullan
# SSH tunnel: ssh -L 5678:localhost:5678 elifberraksayilar@100.108.136.36
"""
Twitter Bookmarks Weekly Digest - n8n workflow yonetim scripti.

Kullanim:
    python fix-workflow.py create    # Yeni workflow olustur
    python fix-workflow.py update    # Mevcut workflow'u guncelle
    python fix-workflow.py trigger   # Webhook ile tetikle
    python fix-workflow.py status    # Workflow durumunu gor
    python fix-workflow.py activate  # Workflow'u aktif et
    python fix-workflow.py test      # Ornek bookmarks.json'u Mac Air'e kopyala

Not: n8n sadece localhost'a bagli. Bu scripti Mac Air uzerinde calistir
     veya SSH tunnel ile baglan.
"""

import json
import subprocess
import sys
import os

N8N_HOST = "http://localhost:5678"
WEBHOOK_PATH = "twitter-bookmarks-trigger"
SSH_CMD = "ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 elifberraksayilar@100.108.136.36"
SCP_CMD = "scp -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519"
DATA_DIR = "/Users/elifberraksayilar/Projects/local-assistant/data/twitter-bookmarks"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKFLOW_ID_FILE = os.path.join(SCRIPT_DIR, "workflow_id.txt")


def load_workflow_id():
    """workflow_id.txt dosyasindan ID oku."""
    try:
        with open(WORKFLOW_ID_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_workflow_id(wf_id):
    """workflow_id.txt dosyasina ID yaz."""
    with open(WORKFLOW_ID_FILE, "w") as f:
        f.write(wf_id)
    print(f"Workflow ID kaydedildi -> {WORKFLOW_ID_FILE}")


def get_api_key():
    """n8n API key'ini Mac Air SQLite'dan al."""
    result = subprocess.run(
        SSH_CMD.split()
        + [
            'sqlite3 /Users/elifberraksayilar/.n8n/database.sqlite '
            '"SELECT apiKey FROM user_api_keys LIMIT 1"'
        ],
        capture_output=True,
        text=True,
    )
    key = result.stdout.strip()
    if not key:
        print("HATA - API key alinamadi")
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# JavaScript Code Snippets (n8n Code Node'lari icin)
# ---------------------------------------------------------------------------

PARSE_JS = r"""
// Parse & Deduplicate - bookmarks.json oku, yeni bookmark'lari filtrele
const fs = require('fs');
const DATA_DIR = '""" + DATA_DIR + r"""';
const filePath = `${DATA_DIR}/bookmarks.json`;

let rawData;
try {
  rawData = fs.readFileSync(filePath, 'utf-8');
} catch (e) {
  return [];
}

let bookmarks;
try {
  const parsed = JSON.parse(rawData);
  bookmarks = Array.isArray(parsed) ? parsed : (parsed.bookmarks || parsed.data || []);
} catch (e) {
  return [];
}

if (bookmarks.length === 0) return [];

// n8n staticData ile islenmis ID'leri takip et (workflow DB'de persist eder)
const staticData = $getWorkflowStaticData('global');
if (!staticData.processedIds) staticData.processedIds = [];

function getId(b) {
  return b.url || b.tweet_id || b.id || b.link || null;
}

const newBookmarks = bookmarks.filter(b => {
  const id = getId(b);
  return id && !staticData.processedIds.includes(id);
});

if (newBookmarks.length === 0) return [];

// Ollama icin prompt olustur
const lines = newBookmarks.map((b, i) => {
  const author = b.author || b.user || b.username || b.screen_name || '?';
  const text = b.text || b.content || b.full_text || '';
  const url = b.url || b.link || '';
  return `[${i+1}] @${author}: ${text}\nURL: ${url}`;
}).join('\n\n');

const prompt = `Asagidaki Twitter bookmark'larini kategorize et ve Turkce ozetle.
Kategoriler: AI/ML, Tech, Business, Turkiye, Diger
Her kategori icin kisa ozet yaz. Tweet URL'lerini koru.

${lines}

Format:
## Kategori
- Ozet (URL)

/no_think`;

const newIds = newBookmarks.map(b => getId(b));

return [{json: {prompt, newIds, newCount: newBookmarks.length, totalCount: bookmarks.length}}];
"""

OLLAMA_JS = None  # Artik kullanilmiyor, HTTP Request node kullaniliyor

FORMAT_JS = r"""
// Ollama ciktisini email HTML'e cevir
const ollamaData = $input.first().json;
const prevData = $('Parse & Deduplicate').first().json;

// Ollama response field'ini al
let text = '';
if (typeof ollamaData.response === 'string') {
  text = ollamaData.response;
} else if (typeof ollamaData === 'string') {
  text = ollamaData;
} else {
  text = JSON.stringify(ollamaData);
}

// qwen3 thinking tag'lerini temizle
text = text.replace(/<think>[\s\S]*?<\/think>/g, '').trim();

const today = new Date().toLocaleDateString('tr-TR', {
  year: 'numeric', month: 'long', day: 'numeric'
});

// Markdown -> HTML donusumu
let html = text
  .replace(/## (.*)/g, '<h2 style="color:#1DA1F2;border-bottom:1px solid #eee;padding-bottom:8px">$1</h2>')
  .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  .replace(/- (.*)/g, '<li>$1</li>')
  .replace(/(https?:\/\/[^\s<)]+)/g, '<a href="$1" style="color:#1DA1F2">$1</a>')
  .replace(/\n\n/g, '</p><p>')
  .replace(/\n/g, '<br>');

const emailHtml = `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;padding:20px">
<div style="background:#1DA1F2;color:white;padding:20px;border-radius:8px 8px 0 0">
<h1 style="margin:0;font-size:24px">Twitter Bookmark Digest</h1>
<p style="margin:8px 0 0;opacity:0.9">${today} - ${prevData.newCount} yeni bookmark</p>
</div>
<div style="background:#fff;padding:20px;border:1px solid #e1e8ed;border-top:none;border-radius:0 0 8px 8px">
${html}
</div>
<div style="text-align:center;padding:16px;color:#657786;font-size:12px">
Lokal Ollama (qwen3:4b) ile ozetlendi.
</div>
</div>`;

return [{json: {
  emailHtml,
  subject: `Twitter Bookmark Digest - ${today}`,
  newIds: prevData.newIds
}}];
"""

STATE_JS = r"""
// Islenen bookmark ID'lerini staticData'ya kaydet
const formatData = $('Format Email').first().json;
const newIds = formatData.newIds || [];

const staticData = $getWorkflowStaticData('global');
if (!staticData.processedIds) staticData.processedIds = [];

staticData.processedIds = [...new Set([...staticData.processedIds, ...newIds])];

return [{json: {
  message: `${newIds.length} yeni ID eklendi, toplam ${staticData.processedIds.length}`,
  totalProcessed: staticData.processedIds.length
}}];
"""


def build_workflow():
    """Workflow tanimini olustur."""
    nodes = [
        {
            "id": "tb-schedule",
            "name": "Schedule Trigger",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.2,
            "position": [260, 300],
            "parameters": {
                "rule": {
                    "interval": [
                        {
                            "field": "cronExpression",
                            "expression": "0 20 * * 0",
                        }
                    ]
                }
            },
        },
        {
            "id": "tb-webhook",
            "name": "Webhook Trigger",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [260, 500],
            "parameters": {
                "httpMethod": "GET",
                "path": WEBHOOK_PATH,
                "responseMode": "onReceived",
                "options": {},
            },
            "webhookId": "tb-webhook-id",
        },
        {
            "id": "tb-parse",
            "name": "Parse & Deduplicate",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [560, 400],
            "parameters": {"jsCode": PARSE_JS, "mode": "runOnceForAllItems"},
        },
        {
            "id": "tb-ollama",
            "name": "Ollama Kategorize",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [840, 400],
            "parameters": {
                "method": "POST",
                "url": "http://127.0.0.1:11434/api/generate",
                "sendBody": True,
                "contentType": "json",
                "specifyBody": "json",
                "jsonBody": '={{ JSON.stringify({"model": "qwen3:4b", "prompt": $json.prompt, "stream": false}) }}',
                "options": {
                    "timeout": 300000,
                    "response": {
                        "response": {
                            "responseFormat": "json"
                        }
                    }
                },
            },
        },
        {
            "id": "tb-format",
            "name": "Format Email",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1300, 400],
            "parameters": {"jsCode": FORMAT_JS, "mode": "runOnceForAllItems"},
        },
        {
            "id": "tb-gmail",
            "name": "Gmail Send Digest",
            "type": "n8n-nodes-base.gmail",
            "typeVersion": 2.1,
            "position": [1560, 400],
            "parameters": {
                "sendTo": "me@cemsayilar.com",
                "subject": "={{ $json.subject }}",
                "emailType": "html",
                "message": "={{ $json.emailHtml }}",
                "options": {},
            },
            "credentials": {
                "gmailOAuth2": {
                    "id": "smrImlBnhBgdsQEM",
                    "name": "Gmail account",
                }
            },
        },
        {
            "id": "tb-state",
            "name": "Update State",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1820, 400],
            "parameters": {"jsCode": STATE_JS, "mode": "runOnceForAllItems"},
        },
    ]

    connections = {
        "Schedule Trigger": {
            "main": [
                [{"node": "Parse & Deduplicate", "type": "main", "index": 0}]
            ]
        },
        "Webhook Trigger": {
            "main": [
                [{"node": "Parse & Deduplicate", "type": "main", "index": 0}]
            ]
        },
        "Parse & Deduplicate": {
            "main": [
                [{"node": "Ollama Kategorize", "type": "main", "index": 0}]
            ]
        },
        "Ollama Kategorize": {
            "main": [
                [{"node": "Format Email", "type": "main", "index": 0}]
            ]
        },
        "Format Email": {
            "main": [
                [{"node": "Gmail Send Digest", "type": "main", "index": 0}]
            ]
        },
        "Gmail Send Digest": {
            "main": [
                [{"node": "Update State", "type": "main", "index": 0}]
            ]
        },
    }

    return {
        "name": "Twitter Bookmarks Weekly Digest",
        "nodes": nodes,
        "connections": connections,
        "settings": {"executionOrder": "v1", "timezone": "Europe/Istanbul"},
    }


# ---------------------------------------------------------------------------
# API Islemleri
# ---------------------------------------------------------------------------


def create_workflow(api_key):
    """Yeni workflow olustur."""
    workflow = build_workflow()
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            f"{N8N_HOST}/api/v1/workflows",
            "-H", f"X-N8N-API-KEY: {api_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(workflow, ensure_ascii=False),
        ],
        capture_output=True,
        text=True,
    )
    resp = json.loads(result.stdout)
    if "id" in resp:
        wf_id = resp["id"]
        print(f"Workflow olusturuldu -> {resp['name']} (ID: {wf_id})")
        save_workflow_id(wf_id)
        return wf_id
    else:
        print(f"HATA - {resp.get('message', resp)}")
        return None


def get_workflow(api_key):
    """Mevcut workflow'u API'den cek."""
    wf_id = load_workflow_id()
    if not wf_id:
        print("HATA - workflow_id.txt bulunamadi. Once 'create' calistir.")
        sys.exit(1)
    result = subprocess.run(
        [
            "curl", "-s",
            f"{N8N_HOST}/api/v1/workflows/{wf_id}",
            "-H", f"X-N8N-API-KEY: {api_key}",
        ],
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def update_workflow(api_key):
    """Workflow'u scriptteki tanimla guncelle."""
    wf_id = load_workflow_id()
    if not wf_id:
        print("HATA - workflow_id.txt bulunamadi. Once 'create' calistir.")
        sys.exit(1)
    workflow = build_workflow()
    clean = {
        "name": workflow["name"],
        "nodes": workflow["nodes"],
        "connections": workflow["connections"],
        "settings": workflow["settings"],
    }
    result = subprocess.run(
        [
            "curl", "-s", "-X", "PUT",
            f"{N8N_HOST}/api/v1/workflows/{wf_id}",
            "-H", f"X-N8N-API-KEY: {api_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(clean, ensure_ascii=False),
        ],
        capture_output=True,
        text=True,
    )
    resp = json.loads(result.stdout)
    if "message" in resp:
        print(f"HATA - {resp['message']}")
        return False
    print(f"Guncellendi -> {resp.get('name')} (active: {resp.get('active')})")
    return True


def activate_workflow(api_key):
    """Workflow'u aktif et."""
    wf_id = load_workflow_id()
    if not wf_id:
        print("HATA - workflow_id.txt bulunamadi")
        sys.exit(1)
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            f"{N8N_HOST}/api/v1/workflows/{wf_id}/activate",
            "-H", f"X-N8N-API-KEY: {api_key}",
        ],
        capture_output=True,
        text=True,
    )
    resp = json.loads(result.stdout)
    print(f"Activate -> {resp.get('active', resp)}")


def trigger_webhook():
    """Workflow'u webhook ile tetikle."""
    result = subprocess.run(
        ["curl", "-s", f"{N8N_HOST}/webhook/{WEBHOOK_PATH}"],
        capture_output=True,
        text=True,
    )
    print(f"Trigger response -> {result.stdout[:500]}")


def show_status(api_key):
    """Workflow durumunu goster."""
    w = get_workflow(api_key)
    print(f"Workflow -> {w['name']}")
    print(f"ID       -> {w['id']}")
    print(f"Active   -> {w.get('active')}")
    print(f"Nodes    -> {len(w['nodes'])}")
    for n in w["nodes"]:
        print(f"  - {n['name']} ({n['type']})")


def send_test_data():
    """sample-bookmarks.json'u Mac Air'e kopyala."""
    sample = os.path.join(SCRIPT_DIR, "sample-bookmarks.json")
    if not os.path.exists(sample):
        print(f"HATA - {sample} bulunamadi")
        sys.exit(1)
    dest = f"elifberraksayilar@100.108.136.36:{DATA_DIR}/bookmarks.json"
    result = subprocess.run(
        SCP_CMD.split() + [sample, dest],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"Kopyalandi -> {dest}")
    else:
        print(f"HATA - {result.stderr}")


def find_node(workflow, name):
    """Workflow icinde node bul."""
    for n in workflow["nodes"]:
        if n["name"] == name:
            return n
    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

COMMANDS = {
    "create": "Yeni workflow olustur",
    "update": "Workflow'u guncelle",
    "trigger": "Webhook ile tetikle",
    "status": "Workflow durumunu gor",
    "activate": "Workflow'u aktif et",
    "test": "Ornek bookmarks.json'u Mac Air'e kopyala",
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Kullanim: python fix-workflow.py <komut>\n")
        for cmd, desc in COMMANDS.items():
            print(f"  {cmd:10s}  {desc}")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "trigger":
        trigger_webhook()
    elif cmd == "test":
        send_test_data()
    else:
        api_key = get_api_key()
        if cmd == "create":
            create_workflow(api_key)
        elif cmd == "update":
            update_workflow(api_key)
        elif cmd == "status":
            show_status(api_key)
        elif cmd == "activate":
            activate_workflow(api_key)

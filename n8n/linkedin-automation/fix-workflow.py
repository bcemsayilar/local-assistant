"""
LinkedIn Workflow guncelleme scripti.

Kullanim:
1. Mevcut workflow'u API'den cek
2. Degisiklikleri uygula
3. API ile geri yukle

Ornek:
    python fix-workflow.py

Not: Bu script Mac Pro'dan calistirilir, n8n Mac Air'de calisir.
"""

import json
import subprocess
import sys

N8N_HOST = "http://100.108.136.36:5678"
WORKFLOW_ID = "S0RDiop6EVTj33AX"
SSH_CMD = "ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 elifberraksayilar@100.108.136.36"


def get_api_key():
    """n8n API key'ini Mac Air SQLite'dan al."""
    result = subprocess.run(
        SSH_CMD.split() + [
            'sqlite3 /Users/elifberraksayilar/.n8n/database.sqlite '
            '"SELECT apiKey FROM user_api_keys LIMIT 1"'
        ],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def get_workflow(api_key):
    """Mevcut workflow'u API'den cek."""
    result = subprocess.run(
        ["curl", "-s", f"{N8N_HOST}/api/v1/workflows/{WORKFLOW_ID}",
         "-H", f"X-N8N-API-KEY: {api_key}"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


def update_workflow(api_key, payload):
    """Workflow'u API ile guncelle."""
    clean = {
        "name": payload["name"],
        "nodes": payload["nodes"],
        "connections": payload["connections"],
        "settings": payload.get("settings", {
            "executionOrder": "v1",
            "timezone": "Europe/Istanbul"
        })
    }
    result = subprocess.run(
        ["curl", "-s", "-X", "PUT",
         f"{N8N_HOST}/api/v1/workflows/{WORKFLOW_ID}",
         "-H", f"X-N8N-API-KEY: {api_key}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(clean, ensure_ascii=False)],
        capture_output=True, text=True
    )
    resp = json.loads(result.stdout)
    if "message" in resp:
        print(f"HATA: {resp['message']}")
        return False
    print(f"Guncellendi: {resp.get('name')} (active: {resp.get('active')})")
    return True


def trigger_webhook():
    """Workflow'u webhook ile tetikle."""
    result = subprocess.run(
        ["curl", "-s", f"{N8N_HOST}/webhook/linkedin-trigger"],
        capture_output=True, text=True
    )
    print(f"Trigger: {result.stdout}")


def find_node(workflow, name):
    """Workflow icinde node bul."""
    for n in workflow["nodes"]:
        if n["name"] == name:
            return n
    return None


if __name__ == "__main__":
    api_key = get_api_key()
    if not api_key:
        print("API key alinamadi")
        sys.exit(1)

    w = get_workflow(api_key)
    print(f"Workflow: {w['name']}")
    print(f"Nodes: {len(w['nodes'])}")

    # Buraya degisiklikleri ekle:
    # node = find_node(w, "LLM - Write LinkedIn Post")
    # node["parameters"]["jsCode"] = "..."

    # update_workflow(api_key, w)
    # trigger_webhook()

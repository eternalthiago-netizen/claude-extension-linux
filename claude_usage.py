#!/usr/bin/env python3
"""Uso do plano Claude (limite de 5 h e semanal) em JSON, para a barra do GNOME.

Usa o login que o app Claude (aba Code) mantém em ~/.claude/.credentials.json
e o mesmo endpoint do comando /usage. O endpoint não é documentado e pode mudar.
O token nunca é renovado aqui (quem renova é o app) nem impresso. Se o login
estiver vencido, devolve o último valor conhecido com "stale": true.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

CREDENTIALS = os.path.expanduser("~/.claude/.credentials.json")
URL = "https://api.anthropic.com/api/oauth/usage"
CACHE = os.path.expanduser("~/.cache/claude-usage.json")


def from_cache(error):
    try:
        with open(CACHE) as f:
            out = json.load(f)
    except (OSError, ValueError):
        return {"error": error}
    out.update(stale=True, error=error)
    return out


def fetch():
    try:
        with open(CREDENTIALS) as f:
            oauth = json.load(f)["claudeAiOauth"]
    except (OSError, ValueError, KeyError):
        return from_cache("Faça login no app Claude")
    if oauth.get("expiresAt", 0) / 1000 < time.time():
        return from_cache("Login vencido: abra uma sessão na aba Code do app")

    req = urllib.request.Request(URL, headers={
        "Authorization": f"Bearer {oauth['accessToken']}",
        "anthropic-beta": "oauth-2025-04-20",
        "User-Agent": "claude-code",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        return from_cache(f"Erro HTTP {e.code}")
    except (urllib.error.URLError, TimeoutError, ValueError):
        return from_cache("Sem conexão")

    out = {}
    for key, src in (("session", "five_hour"), ("weekly", "seven_day")):
        block = data.get(src) or {}
        util = block.get("utilization")
        out[key] = None if util is None else round(util)
        out[key + "_resets_at"] = block.get("resets_at")
    out["fetched_at"] = int(time.time())
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "w") as f:
            json.dump(out, f)
    except OSError:
        pass
    return out


if __name__ == "__main__":
    json.dump(fetch(), sys.stdout)
    print()

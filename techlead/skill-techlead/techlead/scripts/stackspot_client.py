"""Cliente da StackSpot AI — autenticação + chamada de Agent.

Só biblioteca padrão (urllib). Respeita proxy corporativo via variáveis de
ambiente HTTPS_PROXY/HTTP_PROXY (comportamento nativo do urllib).
"""
import json
import urllib.request
import urllib.parse
import urllib.error


def authenticate(cfg: dict, timeout: int = 30) -> str:
    """Client Credentials -> access_token (JWT)."""
    payload = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": cfg["STACKSPOT_CLIENT_ID"],
        "client_secret": cfg["STACKSPOT_CLIENT_SECRET"],
    }).encode("utf-8")
    req = urllib.request.Request(
        cfg["STACKSPOT_IDM_TOKEN_URL"],
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Falha na autenticação StackSpot ({e.code}): {e.read().decode('utf-8', 'ignore')}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Erro de rede na autenticação (verifique proxy HTTPS_PROXY): {e}")
    token = body.get("access_token")
    if not token:
        raise SystemExit("Resposta de auth sem access_token: " + json.dumps(body)[:300])
    return token


def call_agent(cfg: dict, token: str, user_prompt: str, extra_ks=None, timeout: int = 120) -> str:
    """Chama o Agent (síncrono, sem streaming) e retorna o texto da mensagem."""
    url = cfg["STACKSPOT_AGENT_BASE_URL"].rstrip("/") + "/v1/agent/" + cfg["STACKSPOT_AGENT_ID"] + "/chat"
    body = {
        "streaming": False,
        "user_prompt": user_prompt,
        "stackspot_knowledge": True,
        "return_ks_in_response": False,
    }
    if extra_ks:
        # Seleção de Knowledge Sources extras por chamada (enriquecimento por fase)
        body["knowledge_sources"] = extra_ks
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise PermissionError("token_expirado")
        raise SystemExit(f"Erro na chamada do Agent ({e.code}): {e.read().decode('utf-8', 'ignore')}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Erro de rede na chamada do Agent: {e}")
    return payload.get("message", "")

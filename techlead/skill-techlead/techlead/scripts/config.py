"""Configuração do harness TechLead.

Lê credenciais e hosts de um arquivo .env (ou de variáveis de ambiente).
Zero dependências externas — só biblioteca padrão (Python 3.8+).
"""
import os
from pathlib import Path

# Raiz do repositório: .../techlead/scripts/config.py -> parents[2] = raiz
REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_ENV = REPO_ROOT / "techlead" / "setup" / ".env"

# Chaves esperadas no .env
KEYS = [
    "STACKSPOT_IDM_TOKEN_URL",   # URL completa de token (vem do curl do portal)
    "STACKSPOT_AGENT_BASE_URL",  # ex.: https://genai-inference-app.stackspot.com
    "STACKSPOT_CLIENT_ID",
    "STACKSPOT_CLIENT_SECRET",
    "STACKSPOT_AGENT_ID",
]


def _parse_env_file(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        val = val.strip().strip('"').strip("'")
        data[key.strip()] = val
    return data


def load_config(env_path: Path = None, require: bool = True) -> dict:
    """Carrega config do .env e do ambiente. Ambiente tem prioridade."""
    env_path = env_path or DEFAULT_ENV
    cfg = _parse_env_file(env_path)
    for k in KEYS:
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    if require:
        faltando = [k for k in KEYS if not cfg.get(k)]
        if faltando:
            raise SystemExit(
                "Credenciais faltando no .env: " + ", ".join(faltando) +
                "\nRode: python techlead/setup/configure.py  (ou use --mock)"
            )
    return cfg

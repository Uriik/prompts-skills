#!/usr/bin/env python3
"""Wizard de configuração do TechLead.

Cria o arquivo .env local (credenciais individuais da StackSpot) e testa a
autenticação. Cada pessoa do time roda isto uma vez. Só biblioteca padrão.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV_PATH = HERE / ".env"
EXAMPLE = HERE / ".env.example"

CAMPOS = [
    ("STACKSPOT_IDM_TOKEN_URL", "URL de token (copie do curl do portal StackSpot)"),
    ("STACKSPOT_AGENT_BASE_URL", "Base URL do Agent (ex.: https://genai-inference-app.stackspot.com)"),
    ("STACKSPOT_CLIENT_ID", "Seu Client ID (Service Credential)"),
    ("STACKSPOT_CLIENT_SECRET", "Seu Client Secret"),
    ("STACKSPOT_AGENT_ID", "ID do Agent techlead-core"),
]


def main():
    print("== Configuração do TechLead ==")
    if ENV_PATH.exists():
        resp = input(f".env já existe em {ENV_PATH}. Sobrescrever? (s/N) ").strip().lower()
        if resp != "s":
            print("Mantido o .env atual.")
            return
    valores = {}
    for chave, desc in CAMPOS:
        valores[chave] = input(f"{desc}\n  {chave}= ").strip()

    linhas = [f'{k}="{v}"' for k, v in valores.items()]
    ENV_PATH.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\n.env gravado em {ENV_PATH}")

    # Teste de autenticação
    try:
        sys.path.insert(0, str(HERE.parent / "scripts"))
        from config import load_config
        import stackspot_client as ss
        cfg = load_config(ENV_PATH)
        ss.authenticate(cfg)
        print("Autenticação OK — credenciais válidas.")
    except SystemExit as e:
        print(f"Falha no teste de autenticação: {e}")
    except Exception as e:
        print(f"Não foi possível testar agora: {e}")


if __name__ == "__main__":
    main()

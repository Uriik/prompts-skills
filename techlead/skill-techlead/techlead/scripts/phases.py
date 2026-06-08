"""Fases determinísticas do TechLead.

Cada fase: monta um prompt rígido, chama a StackSpot (ou lê mock), extrai JSON,
valida as chaves obrigatórias e devolve um dict Python.
"""
import json
from pathlib import Path

from config import REPO_ROOT

PROMPTS_DIR = REPO_ROOT / "techlead" / "scripts" / "prompts"
MOCK_DIR = REPO_ROOT / "stackspot-simulado" / "mock-responses"


def load_prompt(nome: str, **subs) -> str:
    texto = (PROMPTS_DIR / nome).read_text(encoding="utf-8")
    for chave, valor in subs.items():
        texto = texto.replace("{{" + chave + "}}", valor)
    return texto


def extract_json(texto: str) -> dict:
    """Extrai o primeiro objeto JSON de uma resposta de LLM (tolera ```)."""
    t = texto.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1] if t.count("```") >= 2 else t.strip("`")
        if t.lstrip().startswith("json"):
            t = t.lstrip()[4:]
    ini = t.find("{")
    fim = t.rfind("}")
    if ini == -1 or fim == -1:
        raise ValueError("Sem JSON na resposta")
    return json.loads(t[ini:fim + 1])


def validate(obj: dict, required: list) -> list:
    """Retorna lista de chaves obrigatórias ausentes (vazia = ok)."""
    return [k for k in required if k not in obj]


def load_mock(nome: str) -> dict:
    return json.loads((MOCK_DIR / nome).read_text(encoding="utf-8"))

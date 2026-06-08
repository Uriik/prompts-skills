"""Escreve as tasks em markdown e o log de execução. Garante o limite de linhas.

Esta é a parte determinística que NÃO confia na LLM: conta linhas em Python.
"""
import json
import re
import time
import unicodedata
from pathlib import Path

LIMITE_LINHAS = 120


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t[:40] or "task"


def render_task(task: dict) -> str:
    dep = ", ".join(task.get("depende_de") or []) or "nenhuma"
    linhas = []
    linhas.append(f"# Task {task['id']} — {task['titulo']}")
    linhas.append("")
    linhas.append(f"> Objetivo: {task['objetivo']}")
    linhas.append(f"> Depende de: {dep}")
    linhas.append("")
    linhas.append("## Decisões já tomadas (NÃO reabrir)")
    for d in task.get("decisoes_tomadas") or []:
        linhas.append(f"- {d}")
    if task.get("regras"):
        linhas.append(f"- Arquitetura/código: {', '.join(task['regras'])}")
    if task.get("snippets"):
        linhas.append(f"- Snippets de partida: {', '.join(task['snippets'])}")
    linhas.append("")
    linhas.append("## Passos")
    for i, p in enumerate(task.get("passos") or [], 1):
        linhas.append(f"{i}. {p}")
    linhas.append("")
    linhas.append("## Critérios de aceite")
    for c in task.get("criterios_aceite") or []:
        linhas.append(f"- [ ] {c}")
    linhas.append("")
    linhas.append("## Arquivos esperados")
    for a in task.get("arquivos_esperados") or []:
        linhas.append(f"- `{a}`")
    linhas.append("")
    return "\n".join(linhas)


def escrever_tasks(tasks: list, out_dir: Path, dry_run: bool = False) -> list:
    resultados = []
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
    for task in tasks:
        md = render_task(task)
        n_linhas = len(md.splitlines())
        alerta = None
        if n_linhas > LIMITE_LINHAS:
            alerta = f"ACIMA DE {LIMITE_LINHAS} linhas ({n_linhas}) — candidata a re-split"
        nome = f"{task['id']}-{slug(task['titulo'])}.md"
        destino = out_dir / nome
        if not dry_run:
            destino.write_text(md, encoding="utf-8")
        resultados.append({"arquivo": str(destino), "linhas": n_linhas, "alerta": alerta})
    return resultados


def escrever_log(run: dict, log_dir: Path):
    log_dir.mkdir(parents=True, exist_ok=True)
    nome = f"run-{time.strftime('%Y%m%d-%H%M%S')}.json"
    (log_dir / nome).write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(log_dir / nome)

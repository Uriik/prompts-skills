#!/usr/bin/env python3
"""TechLead — orquestrador determinístico.

Pipeline: Fase 1 (análise) -> Fase 2 (decisão) -> Fase 3 (tasks) -> escrita.
A inteligência de coordenação é deste script; a StackSpot é só motor de
linguagem. Zero dependências externas (Python 3.8+).

Uso:
  python techlead/scripts/techlead.py --demanda "..." --contexto ctx.md
  python techlead/scripts/techlead.py --demanda "..." --mock        # sem StackSpot
  python techlead/scripts/techlead.py --demanda "..." --mock --dry-run
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # permite import direto

from config import REPO_ROOT, load_config
import phases
import writer

MAX_RETRIES = 2

SCHEMAS = {
    "fase1": ["resumo", "impactos", "modulos_afetados", "apis_envolvidas", "riscos", "regras_arquitetura"],
    "fase2": ["decisoes", "padroes", "skills", "gates"],
    "fase3": ["tasks"],
}


def rodar_fase(nome, prompt, required, cfg, token, mock_file, mock):
    """Executa uma fase: mock (lê arquivo) ou real (chama StackSpot + valida + retry)."""
    if mock:
        obj = phases.load_mock(mock_file)
        faltando = phases.validate(obj, required)
        if faltando:
            raise SystemExit(f"[{nome}] mock inválido, faltam chaves: {faltando}")
        return obj, {"modo": "mock"}

    # modo real
    import stackspot_client as ss
    tentativa, ultimo_erro = 0, None
    user_prompt = prompt
    while tentativa <= MAX_RETRIES:
        tentativa += 1
        try:
            msg = ss.call_agent(cfg, token, user_prompt)
        except PermissionError:
            token = ss.authenticate(cfg)  # 401 -> reautentica
            msg = ss.call_agent(cfg, token, user_prompt)
        try:
            obj = phases.extract_json(msg)
            faltando = phases.validate(obj, required)
            if faltando:
                raise ValueError(f"faltam chaves: {faltando}")
            return obj, {"modo": "real", "tentativas": tentativa}
        except (ValueError, json.JSONDecodeError) as e:
            ultimo_erro = str(e)
            user_prompt = prompt + (
                "\n\nATENÇÃO: sua resposta anterior foi inválida (" + ultimo_erro +
                "). Responda APENAS com JSON válido no schema pedido."
            )
    raise SystemExit(f"[{nome}] falhou após {MAX_RETRIES} tentativas: {ultimo_erro}")


def main():
    ap = argparse.ArgumentParser(description="TechLead — planejador de tasks")
    ap.add_argument("--demanda", required=True, help="Texto da demanda")
    ap.add_argument("--contexto", help="Caminho do context.md (Fase 0 do agente local)")
    ap.add_argument("--out", default=str(REPO_ROOT / ".github" / "tasks"), help="Pasta de saída das tasks")
    ap.add_argument("--mock", action="store_true", help="Usa respostas simuladas (sem StackSpot)")
    ap.add_argument("--dry-run", action="store_true", help="Não grava arquivos, só mostra")
    args = ap.parse_args()

    contexto = ""
    if args.contexto and Path(args.contexto).exists():
        contexto = Path(args.contexto).read_text(encoding="utf-8")

    cfg, token = None, None
    if not args.mock:
        import stackspot_client as ss
        cfg = load_config()
        token = ss.authenticate(cfg)

    print(f"== TechLead == demanda: {args.demanda!r}  modo: {'mock' if args.mock else 'real'}")

    # Fase 1 — Análise
    p1 = phases.load_prompt("fase1_analista.txt", DEMANDA=args.demanda, CONTEXTO=contexto or "(sem contexto)")
    analise, m1 = rodar_fase("fase1", p1, SCHEMAS["fase1"], cfg, token, "fase1.json", args.mock)
    print(f"  Fase 1 OK — {len(analise.get('impactos', []))} impactos, {len(analise.get('riscos', []))} riscos")

    # Fase 2 — Decisão (Tech Advisor)
    p2 = phases.load_prompt("fase2_advisor.txt", DEMANDA=args.demanda,
                            ANALISE=json.dumps(analise, ensure_ascii=False))
    decisao, m2 = rodar_fase("fase2", p2, SCHEMAS["fase2"], cfg, token, "fase2.json", args.mock)
    print(f"  Fase 2 OK — {len(decisao.get('decisoes', []))} decisões, padrões: {decisao.get('padroes')}")

    # Fase 3 — Quebra em tasks
    p3 = phases.load_prompt("fase3_split.txt", DEMANDA=args.demanda,
                            ANALISE=json.dumps(analise, ensure_ascii=False),
                            DECISAO=json.dumps(decisao, ensure_ascii=False))
    plano, m3 = rodar_fase("fase3", p3, SCHEMAS["fase3"], cfg, token, "fase3.json", args.mock)
    tasks = plano.get("tasks", [])
    print(f"  Fase 3 OK — {len(tasks)} tasks")

    # Fase 4 — Escrita + garantia de tamanho (Python puro)
    out_dir = Path(args.out)
    resultados = writer.escrever_tasks(tasks, out_dir, dry_run=args.dry_run)

    print("\n== Tasks ==")
    for r in resultados:
        flag = f"  ⚠ {r['alerta']}" if r["alerta"] else ""
        print(f"  - {Path(r['arquivo']).name}  ({r['linhas']} linhas){flag}")

    if not args.dry_run:
        log = writer.escrever_log({
            "demanda": args.demanda,
            "analise": analise, "decisao": decisao, "tasks": tasks,
            "resultados": resultados,
        }, REPO_ROOT / ".github" / ".techlead" / "runs")
        print(f"\nLog: {log}")
        print(f"Tasks em: {out_dir}")
    else:
        print("\n(dry-run: nada gravado)")


if __name__ == "__main__":
    main()

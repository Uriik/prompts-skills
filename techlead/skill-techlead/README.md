# TechLead — POC

Substituto do agente multiagente do Copilot Studio. Transforma uma **demanda**
em um **plano de tasks pequenas** (≤120 linhas), com as **decisões de
arquitetura/tecnologia já tomadas** e os **gates de qualidade** (Veracode/Sonar/
lint) embutidos — para que o executor (LLM ou dev) implemente sem deliberar.

A inteligência de coordenação vive no **harness Python** (determinístico, zero
dependências). A **StackSpot** é só o motor de linguagem (Agent + Knowledge
Sources). O **agente local** (Windsurf / Claude Code) aciona a skill e executa as
tasks.

```
[Demanda]
   │  (Fase 0: agente local lê o repo → context.md)
   ▼
techlead.py  ──Fase 1 Analista──▶ StackSpot ─▶ JSON impacto
             ──Fase 2 Advisor ──▶ StackSpot ─▶ JSON decisões (só do Tech Radar)
             ──Fase 3 Prompt  ──▶ StackSpot ─▶ JSON tasks (mini-specs)
             ──Fase 4 (Python puro)─────────▶ .github/tasks/NN.md (≤120 linhas)
   │
   ▼
Windsurf / Claude Code executam uma task por vez.
```

## Começar em 30 segundos (sem credenciais)
Na raiz do projeto:
```bash
python techlead/scripts/techlead.py \
  --demanda "Criar consumo da API de Extrato e exibir os 10 ultimos lancamentos (Angular), ocultando estornados" \
  --contexto .github/.techlead/context.md \
  --mock
```
Resultado: 4 tasks de exemplo em `.github/tasks/`. O modo `--mock` usa respostas
simuladas (`stackspot-simulado/mock-responses/`) — mesmo pipeline, sem StackSpot.

## Estrutura
```
skill-techlead/
├── techlead/                       # A SKILL
│   ├── SKILL.md                    # entrypoint (Claude Code)
│   ├── reference/                  # o "cérebro" curado (você mantém)
│   │   ├── persona.md
│   │   ├── arquitetura-itau.md     # regras ARQ-xx
│   │   ├── padroes-codigo.md       # regras COD-xx
│   │   ├── tech-radar.md           # adotar/evitar (decisões prontas)
│   │   ├── catalogo-skills.md      # golden-paths + skills
│   │   ├── formato-task.md         # contrato da task
│   │   ├── agents/                 # knowledge de cada agente (5 camadas)
│   │   └── schemas/                # contratos JSON das fases
│   ├── scripts/                    # O HARNESS (stdlib puro)
│   │   ├── techlead.py             # orquestrador (CLI)
│   │   ├── stackspot_client.py     # auth + chamada do Agent
│   │   ├── phases.py               # prompts + extração/validação JSON
│   │   ├── writer.py               # escreve tasks + garante ≤120 linhas
│   │   ├── config.py               # lê .env / proxy
│   │   └── prompts/                # templates de prompt por fase
│   └── setup/
│       ├── configure.py            # wizard de credenciais + teste de auth
│       └── .env.example
├── .windsurf/rules/techlead.md     # entrypoint (Windsurf)
├── stackspot-simulado/             # o que vai para a StackSpot
│   ├── agente/                     # System Prompt do Agent
│   ├── knowledge-sources/          # exemplos de KS (Custom/Snippet/API)
│   └── mock-responses/             # respostas simuladas (modo --mock)
├── .github/tasks/                  # SAÍDA: tasks geradas
├── .github/.techlead/              # context.md (Fase 0) + logs
├── PLANO-IMPLEMENTACAO-TECHLEAD.md # plano conceitual completo
└── PLANO-POC.md                    # passo a passo desta POC
```

## Como funciona (as 4 fases)
1. **Analista** — análise de impacto (o que muda, riscos, regras aplicáveis).
2. **Tech Advisor** — escolhe stack/padrão **só** do Tech Radar e do Catálogo
   (decisão mastigada). Nada fora do Radar.
3. **Prompt Engineer** — quebra em tasks (mini-specs) com "Decisões já tomadas",
   passos, critérios de aceite (com gates) e arquivos esperados.
4. **Writer (Python)** — escreve as tasks e **garante o limite de linhas** em
   código (não confia na LLM para contar).

Cada chamada à StackSpot é *stateless* (sem histórico) → previsível e barata.
Validação de JSON + retry tornam modelos "mini" confiáveis.

## Usar com a StackSpot de verdade
Ver `PLANO-POC.md` §4 (criar Agent, cadastrar Knowledge Sources, gerar Service
Credential, rodar `configure.py`). Resumo:
```bash
python techlead/setup/configure.py        # cria techlead/setup/.env e testa auth
python techlead/scripts/techlead.py --demanda "<...>" --contexto .github/.techlead/context.md
```

## Evoluir o cérebro (sem tocar no código)
- Decisão nova de tecnologia → `reference/tech-radar.md` (+ KS equivalente).
- Receita nova → `reference/catalogo-skills.md` (Golden Path).
- Regra nova → `reference/arquitetura-itau.md` / `padroes-codigo.md`.
- Snippet novo → `stackspot-simulado/knowledge-sources/ks-snippets-*`.
O harness não muda — muda só o conhecimento.

## Decisões de projeto
- **Zero dependências** (só stdlib): nada de `pip install`/`npx` — amigável a
  ambiente corporativo restrito.
- **Credenciais individuais** em `.env` local (no `.gitignore`); ninguém usa a
  chave de outro.
- **Proxy corporativo** respeitado via `HTTPS_PROXY`/`HTTP_PROXY`.
- **Portável** entre Windsurf e Claude Code (mesmo `reference/` + mesmo harness).
- **EV2 fora de escopo:** Devin playbook e Workflow StackSpot ficam para depois.

## Segurança
Nunca versione `techlead/setup/.env`. Não há segredo no repositório. Dados
sensíveis (conta/CPF) são mascarados por regra (ARQ-09 / skill-mascaramento).

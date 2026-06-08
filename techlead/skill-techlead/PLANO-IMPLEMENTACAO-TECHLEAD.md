# Plano de Implementação — Skill TechLead + Harness Orquestrador (StackSpot)

> Documento de **planejamento** (sem código). Objetivo: substituir o agente multiagente do Copilot Studio por uma **skill portável** (Windsurf + Claude Code) cujo cérebro vive numa pasta `reference/`, acionando um **harness Python determinístico** que usa a StackSpot apenas como motor de linguagem.

---

## 1. Princípio central (a decisão que sustenta tudo)

O antigo TechLead do Copilot falhava em custo porque deixava **as LLMs se coordenarem em loop** (orchestrator → subagentes → orchestrator). Cada volta consumia créditos.

A inversão aqui é deliberada: **a inteligência de coordenação sai da LLM e vai para o código Python**. A StackSpot (GPT-4.1 / GPT-5.1-mini) vira um *executor de etapa única* — recebe um prompt rígido, devolve JSON, e acabou. Quem decide a ordem, valida, divide e escreve arquivos é o harness.

Mapeamento dos antigos subagentes → fases determinísticas do harness:

| Antigo subagente (Copilot) | Vira no harness | Papel |
|---|---|---|
| `techlead` (orquestrador) | O próprio `techlead.py` (Python) | Decide ordem, valida, escreve arquivos. **Não é LLM.** |
| `analist` | Fase 1 — Análise de impacto | 1 chamada StackSpot → JSON |
| `analist-skills` | Fase 2 — Seleção de skills/padrões | 1 chamada StackSpot → JSON |
| `engenheiro de prompt` | Fase 3 — Quebra em tasks (≤100–120 linhas) | 1 chamada StackSpot → JSON |
| Persona + boas práticas de arquitetura | `reference/` + System Prompt do Agent StackSpot | Fonte única de regras |

Resultado: **3 chamadas de LLM por demanda** (previsível e barato), em vez de N voltas imprevisíveis.

---

## 2. Como a StackSpot é chamada (confirmado na doc oficial)

Você tem acesso às **duas** superfícies. O plano usa a **Agents API** como caminho principal e mantém **Remote Quick Commands (RQC)** como alternativa.

### 2.1 Autenticação (igual nas duas)
- **Endpoint:** `POST https://idm.stackspot.com/{REALM}/oidc/oauth/token`
- **Body (form-urlencoded):** `grant_type=client_credentials&client_id=...&client_secret=...`
- Retorna `access_token` (JWT). Reutilizável até expirar — o harness cacheia em memória durante a execução.

### 2.2 Caminho principal — Agents API (síncrono, recomendado)
- **Chamada:** `POST https://genai-inference-app.stackspot.com/v1/agent/{AGENT_ID}/chat`
- **Body:** `{ "streaming": false, "user_prompt": "<prompt da fase>", "stackspot_knowledge": true, "return_ks_in_response": false }`
- Resposta vem direta em `message` (sem polling). As Knowledge Sources do Agent entram automaticamente no enriquecimento.
- **Importante p/ custo/determinismo:** **não** usar `use_conversation`. Cada fase é uma chamada *stateless* — o harness encadeia as saídas, não a LLM. Isso evita reinjeção de histórico (= menos tokens) e elimina alucinação de fluxo.

### 2.3 Alternativa — Remote Quick Commands (assíncrono)
- **Cria execução:** `POST https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution/{QC_SLUG}` com `{ "input_data": "..." }` → retorna `execution_id`.
- **Polling:** `GET https://genai-code-buddy-api.stackspot.com/v1/quick-commands/callback/{execution_id}` a cada ~5s até `progress.status == COMPLETED` (ou `FAILED`).
- Use só se precisar de execuções longas/em pipeline CI. Para o uso interativo do dia a dia, a Agents API é mais simples.

> **Decisão de arquitetura:** 1 Agent único `techlead-core` com a persona + regras no System Prompt e as KS anexadas. O harness manda *prompts de fase diferentes* como `user_prompt`. É mais barato e tem só uma config para manter. (Alternativa: um Agent por fase — mais isolamento, mais manutenção. Começar com Agent único.)

---

## 3. Decisões de ambiente corporativo (Itaú)

Estas decisões evitam retrabalho e bloqueios de TI:

1. **Zero dependência externa no harness.** Escrever o script usando **apenas a biblioteca padrão do Python** (`urllib.request`, `json`, `os`, `argparse`). Sem `requests`, sem `python-dotenv`, sem `npx`, sem `pip install`. Nada para baixar, nada para a TI bloquear. (O parsing do `.env` é ~10 linhas de código próprio.)
2. **Proxy corporativo.** O `urllib` respeita as variáveis `HTTPS_PROXY`/`HTTP_PROXY`/`NO_PROXY` do ambiente. O harness deve documentar isso e logar qual proxy está em uso.
3. **Endpoints podem passar por gateway interno.** Os domínios `*.stackspot.com` acima são os públicos. Se o Itaú expõe a StackSpot atrás de um gateway/allowlist interno, os hosts devem ser **configuráveis via `.env`** (`STACKSPOT_IDM_URL`, `STACKSPOT_AGENT_URL`), nunca hardcoded. *(Ver pergunta aberta #1.)*
4. **Credenciais individuais.** Cada pessoa gera o próprio Client ID/Secret (Service Credential) no portal StackSpot. Você **nunca** distribui as suas. O harness lê de `.env` local (no `.gitignore`).
5. **Auditabilidade.** Cada execução grava um log JSON (`.github/.techlead/runs/run-<timestamp>.json`) com demanda, fases, tokens consumidos e tasks geradas. Útil para governança bancária.

---

## 4. Estrutura de pastas do projeto

Fonte única de verdade em `reference/` e `scripts/`. Os dois entrypoints (Claude Code e Windsurf) são **ponteiros finos** para os mesmos arquivos — sem duplicar regra.

```
skill-techlead/
├── techlead/                         # A SKILL (entrypoint Claude Code)
│   ├── SKILL.md                      # Quando/como acionar; manda rodar o harness
│   ├── reference/                    # O "cérebro" — boas práticas centralizadas
│   │   ├── persona.md                # Persona do TechLead
│   │   ├── arquitetura-itau.md       # Regras de arquitetura do banco
│   │   ├── padroes-codigo.md         # Padrões de código / convenções
│   │   ├── formato-task.md           # Spec do formato de task (≤120 linhas, prompt-ready)
│   │   ├── catalogo-skills.md        # Skills/padrões disponíveis p/ a fase 2 escolher
│   │   └── schemas/                  # Schemas JSON de cada fase (contrato com a LLM)
│   │       ├── fase1-analise.json
│   │       ├── fase2-skills.json
│   │       └── fase3-tasks.json
│   ├── scripts/                      # O HARNESS
│   │   ├── techlead.py               # Orquestrador determinístico (entrypoint CLI)
│   │   ├── stackspot_client.py       # Auth + chamada Agent/RQC (só stdlib)
│   │   ├── phases.py                 # Monta prompts de cada fase + valida JSON
│   │   ├── writer.py                 # Escreve .github/tasks/*.md + log de run
│   │   ├── config.py                 # Lê .env, hosts, proxy
│   │   └── prompts/                  # Templates de prompt por fase (texto)
│   │       ├── fase1_analista.txt
│   │       ├── fase2_skills.txt
│   │       └── fase3_split.txt
│   └── setup/
│       ├── configure.py              # Wizard: cria .env e testa auth
│       └── .env.example              # Modelo de credenciais
├── .windsurf/
│   └── rules/
│       └── techlead.md               # Entrypoint Windsurf → aponta p/ reference + manda rodar harness
├── .github/
│   └── tasks/                        # SAÍDA: tasks geradas (uma por arquivo)
├── .gitignore                        # ignora .env e .github/.techlead/runs
└── README.md                         # Onboarding do time
```

---

## 5. O harness por dentro (fluxo determinístico)

Entrada: `python techlead/scripts/techlead.py --demanda "criar tela de extrato" --contexto .github/.techlead/context.md`

```
[Demanda]  +  [context.md gerado pelo AGENTE LOCAL antes de chamar o harness]
        │
        ▼
 (Agente local — Windsurf/Claude Code, plan mode, modelo barato):
   lê o repo, resume estrutura/arquivos-chave em .github/.techlead/context.md.
   O Python NÃO varre o repo — recebe o resumo pronto. (Decisão da pergunta #3.)
        │
        ▼
 FASE 1 — Análise de impacto      → StackSpot Agent → JSON (valida contra schema; retry se inválido)
        │
        ▼
 FASE 2 — Seleção de skills/padrões → StackSpot Agent → JSON (recebe saída da fase 1)
        │
        ▼
 FASE 3 — Quebra em tasks          → StackSpot Agent → JSON (array de tasks ≤120 linhas)
        │
        ▼
 (Python) Validação dura: conta linhas de cada task. Se >120 → re-split programático
          ou devolve a task ofensora à fase 3. Garante o limite SEM confiar na LLM.
        │
        ▼
 (Python) writer.py → escreve .github/tasks/01-*.md, 02-*.md ... + run log JSON
        │
        ▼
 Retorna ao agente (Windsurf/Claude Code) um resumo: N tasks criadas, caminhos, tokens.
```

Regras de robustez do harness (o "bom harness" que você pediu):

- **JSON obrigatório por fase.** Prompt exige *só* JSON. Se a resposta não parsear, retry até `MAX_RETRIES` (ex.: 2) com a mensagem "sua saída anterior não era JSON válido; responda apenas com JSON". Modelos mini seguem isso bem.
- **Schema validation** contra os arquivos em `reference/schemas/`. Campo faltando = retry.
- **Contexto enxuto por fase.** Cada chamada recebe só o que precisa (saída da fase anterior + trecho do reference), nunca o histórico todo. Isso é o que segura o custo.
- **Limite de linhas garantido em Python**, não pela LLM (a LLM erra contagem). Esse é o ponto onde o Copilot original te traía.
- **Idempotência/dry-run.** Flag `--dry-run` imprime as tasks sem escrever, p/ você revisar antes.
- **Tratamento de erro da API:** timeout, 401 (token expirado → reautentica), 429 (backoff), 5xx (retry com limite).

---

## 6. Portabilidade Windsurf + Claude Code

Os dois consomem **o mesmo** `reference/` e **o mesmo** harness. Só muda a "capa":

**Claude Code** — `techlead/SKILL.md`:
- Descrição que dispara a skill quando você pede "quebrar demanda em tasks", "agir como techlead", etc.
- Instrui o agente a: (1) confirmar que `.env` existe (senão rodar `setup/configure.py`); (2) **ler o repo e gerar `.github/.techlead/context.md`** (resumo de estrutura + arquivos relevantes à demanda — use plan mode / modelo barato); (3) executar `python techlead/scripts/techlead.py --demanda "<...>" --contexto .github/.techlead/context.md`; (4) ler o resumo e abrir as tasks geradas; (5) executar uma task por vez.

**Windsurf** — `.windsurf/rules/techlead.md`:
- Regra (always-on ou manual) que dá ao Cascade a mesma instrução: "Para planejar uma demanda, NÃO escreva código direto. Rode o harness `techlead.py`, depois execute as tasks de `.github/tasks/` uma a uma. As regras de arquitetura estão em `techlead/reference/`."
- Opcional: um **Windsurf Workflow** (`/techlead`) que encapsula o comando.

> O agente **não** reimplementa a lógica — ele só *invoca o script e lê a saída*. Toda a inteligência fica versionada em `reference/` + harness. É isso que torna portável e barato.

---

## 7. Setup da StackSpot (uma vez, no portal)

1. Criar um **Agent** `techlead-core`:
   - System Prompt = `persona.md` + resumo das regras de `arquitetura-itau.md` + `padroes-codigo.md`.
   - Anexar **Knowledge Sources** com as documentações internas de arquitetura/padrões do Itaú.
   - Escolher o melhor modelo disponível (GPT-5.1-mini).
   - Anotar o `AGENT_ID` → vai no `.env`.
2. Gerar **Service Credential** (Client ID/Secret) — cada membro do time gera a sua.
3. (Opcional) Criar os **RQC** equivalentes se quiser usar o caminho assíncrono em CI.

---

## 8. Distribuição para o time (sem expor seus dados)

1. Time clona o repositório compartilhado (GitHub interno).
2. Cada pessoa roda `python techlead/setup/configure.py` → wizard cria o `.env` dela (Client ID/Secret/Realm/Agent ID próprios) e faz um *teste de auth* (bate no IDM e confirma token).
3. `.env` está no `.gitignore` → credenciais nunca sobem.
4. Pronto: a pessoa usa via Windsurf ou Claude Code, com a inteligência que **você** centralizou no `reference/`.

---

## 9. Roadmap de implementação (ordem sugerida)

| # | Etapa | Entregável | Depende de |
|---|---|---|---|
| 0 | Responder perguntas abertas (§10) | Decisões travadas | — |
| 1 | Setup StackSpot (Agent + KS + credencial) | `AGENT_ID`, realm, hosts | #0 |
| 2 | Scaffold da estrutura de pastas | Árvore do §4 vazia | — |
| 3 | Escrever o `reference/` (o cérebro) | persona, arquitetura, padrões, formato-task, schemas | #0 |
| 4 | `stackspot_client.py` (auth + chat, só stdlib) + teste de auth | Cliente funcional | #1 |
| 5 | `phases.py` + `prompts/` + validação JSON/schema | Pipeline das 3 fases | #3, #4 |
| 6 | `writer.py` (tasks + run log) + garantia de ≤120 linhas | Saída em `.github/tasks/` | #5 |
| 7 | `techlead.py` (orquestrador + CLI + dry-run) | Harness completo | #4–#6 |
| 8 | `SKILL.md` + `.windsurf/rules/techlead.md` | Entrypoints portáveis | #7 |
| 9 | `configure.py` (wizard) + `.env.example` + `.gitignore` | Onboarding | #4 |
| 10 | Validação com 1 demanda "golden" + revisão das tasks | Teste ponta a ponta | #7 |
| 11 | `README.md` + rollout no time | Distribuição | #8–#10 |

---

## 10. Decisões travadas (respondidas)

1. **Hosts:** o StackSpot entrega o **curl pronto** ao criar o Agent/QC. O host real (público ou gateway interno) sai desse curl → vai para o `.env` como variável (`STACKSPOT_AGENT_URL`, `STACKSPOT_IDM_URL`). O harness nunca fixa host.
2. **Python:** alvo **3.8+**, **100% stdlib**, sem `pip install`.
3. **Contexto:** lido pelo **agente local** (Windsurf/Claude Code em plan mode, modelo barato), salvo em `.github/.techlead/context.md`, passado ao harness via `--contexto`. Devin entra só como **playbook opcional** (ver Parte 2 §D).
4. **Idioma:** tudo em **PT-BR** (persona, prompts, tasks).
5. **Repo:** GitHub Enterprise interno, **padrão de mercado** de estrutura.

---

# Parte 2 — Detalhamento (`reference/` + pseudo-fluxo das fases)

## A. O que entra em cada arquivo do `reference/`

O `reference/` é o cérebro versionado. Regra de ouro: **conteúdo curto e citável** — cada fase injeta só o trecho relevante no prompt, nunca o arquivo inteiro, para segurar token.

### `persona.md`
Define quem é o TechLead: tom, princípios de decisão, o que ele **sempre** faz (quebrar em tasks pequenas, citar a regra de arquitetura que justifica cada escolha) e o que **nunca** faz (escrever código na fase de planejamento, criar task >120 linhas, inventar padrão fora do catálogo). ~30–50 linhas.

### `arquitetura-itau.md`
As regras de arquitetura do banco que toda task precisa respeitar: camadas permitidas, padrões de integração, segurança/compliance, o que exige aprovação. Estruturado em **regras numeradas e curtas** (`ARQ-01`, `ARQ-02`...) para a LLM conseguir referenciar o ID na saída. Este conteúdo também vai no System Prompt do Agent + nas Knowledge Sources.

### `padroes-codigo.md`
Convenções de código: nomenclatura, estrutura de pastas esperada, tratamento de erro, testes mínimos, lint. Também em itens com ID (`COD-01`...).

### `formato-task.md`
**O contrato da saída** — o mais importante. Define a anatomia de uma task gerada:
- Cabeçalho (id, título, objetivo, ≤120 linhas).
- Pré-requisitos / tasks que bloqueiam.
- Passos como **prompt pronto** para o executor (o "engenheiro de prompt" virou este template).
- Critérios de aceite + arquivos esperados.
- Regras de arquitetura aplicáveis (IDs de `arquitetura-itau.md`).
Inclui um **exemplo completo** de uma task modelo (gold standard) que a Fase 3 deve imitar.

### `catalogo-skills.md`
Lista fechada de skills/padrões reutilizáveis que a Fase 2 pode escolher (ex.: "skill-rest-client", "padrão-paginacao", "template-tela-crud"). Cada item: nome, quando usar, o que entrega. A Fase 2 **só pode escolher desta lista** — evita alucinação.

### `schemas/fase1-analise.json`, `fase2-skills.json`, `fase3-tasks.json`
JSON Schemas (draft-07) que definem o contrato de saída de cada fase. O harness valida a resposta da LLM contra eles. Campo faltando ou tipo errado → retry. São a "trava" que faz modelo mini se comportar.

> **Fora de escopo (EV2):** o playbook do Devin é uma evolução futura, de outro fluxo. **Não** entra neste plano. A Fase 0 aqui é sempre o agente local (Windsurf/Claude Code).

---

## B. Pseudo-fluxo de cada fase

Notação: cada fase = `[input Python] → monta prompt (persona + trecho do reference + input) → 1 chamada StackSpot → parse JSON → valida schema → (retry se falhar) → output Python`.

### Fase 0 — Contexto (agente local, **não** é chamada StackSpot)
- **Quem:** Windsurf/Claude Code em plan mode.
- **Faz:** lê o repo, identifica arquivos relevantes à demanda, escreve `.github/.techlead/context.md` (estrutura resumida, stack, arquivos-chave, pontos de integração). Curto, ~1–2 páginas.
- **Por quê fora do Python:** o modelo local já tem o repo indexado e é barato/grátis para ler. Tira varredura de arquivo do script.

### Fase 1 — Análise de impacto (StackSpot)
- **Input:** `demanda` + `context.md` + trecho de `arquitetura-itau.md`.
- **Prompt (esqueleto):** "Você é o TechLead. Analise a demanda e o contexto. Responda **apenas** com JSON no schema X: o que muda, módulos/arquivos afetados, riscos, regras de arquitetura aplicáveis (IDs), dependências, esforço relativo."
- **Output JSON:** `{ resumo, impactos[], modulos_afetados[], riscos[], regras_arquitetura[], dependencias[] }`.
- **Validação:** schema `fase1-analise.json`.

### Fase 2 — Seleção de skills/padrões (StackSpot)
- **Input:** saída da Fase 1 + `catalogo-skills.md`.
- **Prompt:** "Dado o impacto abaixo e o catálogo de skills disponíveis, escolha **apenas itens do catálogo** que se aplicam. Justifique cada escolha em 1 linha. Responda só JSON."
- **Output JSON:** `{ skills_escolhidas[ {id, motivo} ], padroes[ {id, motivo} ] }`.
- **Validação:** schema + checagem Python de que todo `id` existe no catálogo (descarta inventados).

### Fase 3 — Quebra em tasks (StackSpot)
- **Input:** Fases 1+2 + `formato-task.md` (incl. exemplo gold).
- **Prompt:** "Quebre a demanda em tasks sequenciais. Cada task ≤120 linhas, no formato do exemplo, como prompt pronto para um executor. Inclua dependências entre tasks e IDs de regra de arquitetura. Responda só JSON: array de tasks."
- **Output JSON:** `{ tasks: [ { id, titulo, objetivo, depende_de[], passos, criterios_aceite[], arquivos_esperados[], regras[] } ] }`.
- **Validação:** schema `fase3-tasks.json`.

### Fase 4 — Escrita + garantia de tamanho (Python puro, **sem LLM**)
- Para cada task: renderiza o markdown final em `.github/tasks/NN-<slug>.md`.
- **Conta as linhas.** Se > 120: tenta re-split programático (quebra em `NN-a`, `NN-b` preservando dependências) ou devolve **só aquela task** à Fase 3 com instrução de dividir. Loop até todas ≤120.
- Escreve `.github/.techlead/runs/run-<timestamp>.json`: demanda, saídas de cada fase, tokens (a Agents API retorna `tokens` por chamada), tasks geradas.
- Retorna ao agente: lista de tasks + caminhos + total de tokens.

---

## C. Tratamento de erro / retry (resumo operacional do harness)

| Situação | Ação |
|---|---|
| Resposta não é JSON | Retry (máx 2) com "responda apenas com JSON válido" |
| JSON não bate no schema | Retry citando o campo que faltou |
| `id` fora do catálogo (Fase 2) | Python descarta o item inválido |
| Task > 120 linhas (Fase 4) | Re-split programático ou re-chamada da Fase 3 só p/ a task |
| 401 token expirado | Reautentica no IDM e repete a chamada |
| 429 / 5xx | Backoff exponencial, máx N tentativas |
| Timeout | Erro claro + sugere checar proxy (`HTTPS_PROXY`) |

---

## D. Caminho Devin — **EV2, fora deste escopo**

O Devin Ask como gerador de contexto é uma **evolução futura (EV2)**, parte de outro fluxo. Fica registrado aqui só para não se perder, mas **não** é implementado neste plano. Neste plano, a Fase 0 é sempre o agente local em plan mode (modelo barato).

---

## E. Próximo nível de detalhe (quando você quiser)

Posso descer mais em qualquer destes — me diz qual prioriza:
- **Conteúdo real dos schemas JSON** (campos exatos das 3 fases).
- **Texto modelo do `formato-task.md`** com a task gold de exemplo.
- **Pseudocódigo do `techlead.py`** (funções, ordem de chamadas, sem implementar).
- **Texto do `SKILL.md` e da regra do Windsurf** (os entrypoints).

---

# Parte 3 — TechLead como Consultor de Tecnologia (decisão já mastigada)

> O TechLead antigo não só quebrava tasks: ele **trazia a decisão de tecnologia/código pronta**, para o executor não gastar raciocínio "escolhendo". Esta parte traz ideias de como recriar isso. O conceito-chave, repetido nos repos/práticas mais respeitados, é **separar "decidir" de "fazer"**: a decisão é curada uma vez por você e injetada na task; o executor só implementa.

## A. O mecanismo central — "Decisões já tomadas" dentro de cada task

Toda task gerada em `.github/tasks/NN.md` ganha um bloco fixo no topo:

```
## Decisões já tomadas (não reabrir)
- Stack/libs: usar X (Tech Radar: ADOTAR) — não avaliar alternativas.
- Padrão: seguir golden-path GP-03 (nova tela CRUD).
- Arquitetura: ADR-012, ADR-007 se aplicam.
- Snippets de partida: snippets/cliente-rest.md, snippets/paginacao.md
```

O executor (Windsurf/Claude/Devin) lê isso e **não delibera** stack nem padrão — já vem decidido. É exatamente o "não fazer a LLM pensar" que você descreveu. Esse padrão é o mesmo que ferramentas tipo Mneme aplicam: transformar ADRs em **checagem determinística antes da geração** para Claude Code/Cursor/Copilot.

## B. O que entra no `reference/` para alimentar isso (curado por você)

Aqui mora a sua expertise de TechLead. Quatro artefatos, todos curtos e citáveis por ID:

1. **Tech Radar** (`reference/tech-radar.md`) — modelo ThoughtWorks: `ADOTAR / EXPERIMENTAR / AVALIAR / EVITAR`. Diz qual lib/ferramenta é o default e qual é proibida. Resolve 80% das microdecisões ("qual cliente HTTP?", "qual lib de data?") antes de existirem.
2. **ADRs** (`reference/decisoes/ADR-XXX.md`) — formato Nygard: contexto, decisão, alternativas rejeitadas, consequência. Imutáveis. São o "porquê" que justifica o radar.
3. **Golden Paths / Receitas** (`reference/golden-paths/GP-XX.md`) — o caminho pavimentado para tipos recorrentes de demanda (nova tela CRUD, novo endpoint REST, consumir fila, etc.): passo a passo + esqueleto. Reduz carga cognitiva guiando para o default testado.
4. **Snippets** (`reference/snippets/*.md`) — blocos de código prontos dos padrões do banco, para o executor adaptar em vez de inventar.

## C. Como a decisão entra no fluxo das fases (duas opções)

**Opção 1 — Determinística (recomendada, custo zero de LLM):**
A Fase 2 (já existente, "seleção de skills/padrões") é estendida para também **selecionar do catálogo curado** quais entradas de Radar/ADR/Golden-Path/Snippet se aplicam — escolhendo **só de listas fechadas** (sem inventar). A Fase 3 injeta essas escolhas no bloco "Decisões já tomadas" de cada task. Nenhuma chamada extra.

**Opção 2 — Fase "Tech Advisor" dedicada (uma chamada a mais):**
Uma Fase 2.5 que recebe a análise de impacto e devolve um "decision pack" (JSON) com as recomendações de tecnologia. Útil se você quiser que a LLM *combine* decisões de forma mais rica — mas continua **presa ao catálogo**. Custa um pouco mais; só vale se a Opção 1 ficar limitada.

> Minha recomendação: comece pela **Opção 1**. O ganho do "consultor" vem 90% da curadoria do `reference/` (Radar/ADR/Golden-Path), não de mais inteligência em runtime.

## D. Padrões emprestados dos repos/práticas mais respeitados

- **AGENTS.md / CLAUDE.md / `.cursorrules`** — convenção de um arquivo de regras vivo na raiz que todo agente lê. Aqui ele é o entrypoint fino que aponta para `reference/`. (Padrão emergente AGENTS.md.)
- **Spec-Driven Development (GitHub Spec Kit / `specify`)** — escrever a spec antes; o agente gera a partir dela. As suas tasks **são** mini-specs — alinhe o `formato-task.md` a isso: cada task = spec com a decisão embutida.
- **ADR como pré-checagem determinística** (Mneme) — ADR não é doc parado; vira regra que o harness injeta antes da geração.
- **Golden Paths (Spotify Backstage / Platform Engineering)** — caminhos opinativos e suportados que reduzem deliberação.
- **Knowledge activation / "skills como conhecimento institucional"** — tratar cada golden-path como uma skill instalável e versionada.

## E. Perguntas para você (antes de eu detalhar o `reference/` de decisão)

1. **Quem mantém o Radar/ADRs?** Só você, ou o time abre PR para propor mudança de decisão? (Isso define o fluxo de governança no GitHub Enterprise.)
2. **Você já tem decisões catalogáveis hoje** (libs padrão, padrões de tela/endpoint do banco) que eu posso usar como exemplo de Radar/ADR no modelo, ou começamos com a estrutura vazia para você preencher?
3. **Opção 1 (determinística) ou Opção 2 (fase Tech Advisor)** para a primeira versão? (Recomendo a 1.)
4. **Tipos de demanda recorrentes** que mais se repetem no seu dia a dia (ex.: nova tela, novo endpoint, integração) — para eu já desenhar os primeiros Golden Paths.

---

# Parte 4 — Catálogo de Knowledge Sources por agente (enriquecimento robusto)

> Decisão registrada: **sem Workflow StackSpot** no inner loop. Contexto real do time: **Java + Angular**, libs/SDKs internos do banco, foco em **integração com APIs, novos endpoints, novos consumos e regras de negócio**, com **Veracode + Sonar + lint** como gates obrigatórios.

## A. Os 3 tipos de KS da StackSpot (use o tipo certo p/ cada conteúdo)

| Tipo | Formatos | Split recomendado | Para quê |
|---|---|---|---|
| **API** | json, yaml (OpenAPI/Swagger) | `ENDPOINT` (1 objeto por endpoint) | Contratos das APIs internas que você consome/expõe |
| **Snippet** | java, ts, js, sql… | `SYNTACTIC` (por função/bloco) | Código-padrão do banco pronto p/ adaptar |
| **Custom** | txt, md, json, yaml, pdf | `SYNTACTIC` ou `TOKENS_QUANTITY` | Regras, decisões, padrões, glossário, gates |

Regra de ouro do enriquecimento: **um KS = um assunto**. KS focado recupera melhor na busca por similaridade do que um KS "saco de gato". Vale criar muitos KS pequenos em vez de poucos gigantes.

## B. Catálogo de KS (o que criar)

### Fundação / governança (Custom)
| ID | Conteúdo | Split | Origem |
|---|---|---|---|
| `ks-arquitetura` | Camadas permitidas, padrões de integração, o que exige aprovação (regras `ARQ-xx`) | SYNTACTIC (por header) | Doc interna de arquitetura |
| `ks-padroes-codigo` | Convenções Java + Angular, estrutura de pastas, tratamento de erro, testes mínimos (`COD-xx`) | SYNTACTIC | Guia de código do time |
| `ks-tech-radar` | Adotar / Experimentar / Avaliar / Evitar (libs, frameworks, versões) | NONE ou SYNTACTIC | Curadoria sua |
| `ks-adr` | Catálogo de ADRs (decisão, alternativas rejeitadas, consequência) | SYNTACTIC (1 ADR por objeto) | Curadoria sua |
| `ks-glossario-negocio` | Termos de domínio do banco, siglas, entidades de negócio | TOKENS_QUANTITY | Time de negócio |

### Segurança e qualidade (Custom) — os gates
| ID | Conteúdo | Split | Origem |
|---|---|---|---|
| `ks-veracode` | Categorias de vulnerabilidade que mais reprovam + padrões de remediação seguros (ex.: input validation, SQLi, XSS) | SYNTACTIC | Relatórios Veracode + políticas |
| `ks-sonar` | Quality gates, regras ativadas, thresholds de cobertura, code smells recorrentes | SYNTACTIC | Config Sonar do projeto |
| `ks-lint` | Regras de lint Java (Checkstyle/SpotBugs) e Angular (ESLint/TSLint) ativas | NONE | Arquivos de config |

### Contratos de API (tipo API)
| ID | Conteúdo | Split | Origem |
|---|---|---|---|
| `ks-apis-internas` | OpenAPI/Swagger das APIs internas que você **consome** (endpoints, schemas, auth) | `ENDPOINT` | Specs dos serviços internos |
| `ks-api-guidelines` | Padrão de design de API do banco: versionamento, formato de erro, paginação, headers | SYNTACTIC (Custom md) | Guia de APIs |

### Código-padrão (tipo Snippet)
| ID | Conteúdo | Split | Origem |
|---|---|---|---|
| `ks-snip-java` | Controller, Service, DTO, client REST, tratamento de erro, paginação, teste unitário — no padrão do banco | SYNTACTIC | Repos de referência |
| `ks-snip-angular` | Component, service HTTP, interceptor, form reativo, guard — no padrão do banco | SYNTACTIC | Repos de referência |
| `ks-snip-integracao` | Consumo de API: resiliência (retry/circuit breaker), auth interna, SDK do banco | SYNTACTIC | Repos de referência |
| `ks-golden-paths` | Receitas passo a passo: "novo endpoint REST", "novo consumo de API", "nova regra de negócio", "nova tela Angular" | SYNTACTIC | Curadoria sua |

## C. Qual KS alimenta cada agente/fase

Modelo recomendado: **1 Agent base `techlead-core`** (persona + KS de fundação como default) e o harness **seleciona os KS extras por chamada** via o parâmetro *Extra Knowledge Source Selection* da Agents API. Assim cada fase é enriquecida só com o que importa — sem criar 4 Agents para manter. (Alternativa: 1 Agent por fase, se quiser isolamento total.)

| Fase / papel | KS default (persona) | KS extras selecionados na chamada | Por quê |
|---|---|---|---|
| **TechLead (persona base)** | `ks-arquitetura`, `ks-tech-radar`, `ks-adr`, `ks-glossario-negocio` | — | Identidade + regras macro sempre presentes |
| **Fase 1 — Analista (impacto)** | herda persona | `ks-apis-internas`, `ks-api-guidelines` | Saber o que existe/é afetado, contratos em jogo |
| **Fase 2 — Tech Advisor (decisões)** | herda persona | `ks-tech-radar`, `ks-adr`, `ks-golden-paths`, `ks-veracode`, `ks-sonar` | Escolher stack/padrão **já decidido** e compatível com os gates |
| **Fase 3 — Prompt Engineer (split)** | herda persona | `ks-padroes-codigo`, `ks-snip-java`, `ks-snip-angular`, `ks-snip-integracao`, `ks-golden-paths`, `ks-api-guidelines`, `ks-veracode`, `ks-sonar`, `ks-lint` | Cada task sai com snippet de partida + gates nos critérios de aceite |

> **Veracode/Sonar/lint viram critério de aceite em toda task.** A Fase 2 escolhe o padrão seguro (`ks-veracode`/`ks-sonar`) e a Fase 3 escreve isso no bloco "Critérios de aceite" de cada task (ex.: "0 findings High/Medium no Veracode; passa no quality gate do Sonar; sem violação de lint"). O executor já recebe a barra de qualidade explícita.

## D. Boas práticas de enriquecimento (para ficar robusto de verdade)

- **KS focado e versionado em md** quando possível — fica diffável no GitHub Enterprise e fácil de revisar por PR.
- **APIs como tipo API com split `ENDPOINT`** — cada endpoint vira um objeto recuperável; muito melhor que colar Swagger num Custom.
- **Snippets como tipo Snippet, não Custom** — o split sintático respeita a estrutura do código.
- **`return_ks_in_response: true` na fase de tuning** — mostra quais KS foram realmente usados; ajuste o que não está sendo recuperado.
- **`Deep Knowledge Sources` quando precisar de precisão** — busca mais detalhada dentro dos objetos.
- **Cadência de atualização:** APIs internas e Veracode/Sonar mudam — defina dono e revisão (ex.: trimestral, ou via PR quando a regra muda).
- **Não duplicar** o mesmo conteúdo no System Prompt **e** no KS: regras macro curtas no prompt; detalhe pesquisável no KS.

## E. Perguntas para fechar o catálogo

1. As **APIs internas que você consome têm OpenAPI/Swagger** disponível (pra virar `ks-apis-internas` tipo API)? Ou só doc em texto?
2. Os **rule sets de Veracode e Sonar são exportáveis** (relatório/JSON/config) pra eu estruturar `ks-veracode`/`ks-sonar`, ou começo com um modelo genérico pra você preencher?
3. Quer **1 Agent base com seleção de KS por chamada** (recomendado) ou **1 Agent por fase**?

---

# Parte 5 — Os "knowledges" de cada agente (o que ensinar para extrair 100%)

> **Esclarecimento (corrige a confusão das Partes 4 e 5):** skill, regra e instrução **são** conhecimento — e "Fonte de Conhecimento" (Knowledge Source) é só o **recipiente** da StackSpot onde esse conteúdo mora. Não são coisas diferentes: o conteúdo desta Parte 5 **é** o que você coloca dentro de uma Fonte de Conhecimento (ou no System Prompt). A Parte 4 só descreve a mecânica do recipiente (tipos/split) — não um "outro tipo de knowledge".
>
> A única distinção real é o **canal de entrega** do mesmo conhecimento:
> - **System Prompt do agente** → identidade, persona, regras duras, contrato de saída. Curto, sempre lido.
> - **Fonte de Conhecimento** → material volumoso e pesquisável (catálogo de skills, ADRs, snippets, specs). Buscado por similaridade.
> O que decide o canal é só o tamanho e se precisa ser sempre lido ou sob demanda.
>
> Padrão para todo agente: cada "knowledge" tem 5 camadas — **(1) o que ele sabe** (domínio), **(2) como pensa** (método/heurística), **(3) checklist** (o que nunca esquecer), **(4) anti-padrões** (o que nunca fazer), **(5) exemplo gold** (1 caso modelo). É isso que tira o agente de "genérico" e o deixa cirúrgico.

## Conhecimento compartilhado (base de todos os agentes)
Antes dos específicos, todo agente herda esta fundação:
- **Mapa do sistema do banco:** camadas, serviços, como as coisas se integram.
- **Glossário de negócio:** termos, siglas, entidades de domínio.
- **Régua de qualidade inegociável:** Veracode (0 High/Medium), Sonar quality gate, lint limpo, testes.
- **Contrato de saída:** todo agente responde **só JSON** no schema da sua fase.
- **Idioma e tom:** PT-BR, objetivo, sem floreio.

---

## 1. Agente TechLead (persona / dono da régua)
**Papel:** guardar boas práticas, decidir granularidade, garantir que nada vira código sem plano.

| Camada | Knowledge a embutir |
|---|---|
| Sabe | Princípios de arquitetura do banco; o que exige aprovação/compliance; definição de "task pronta" |
| Pensa | Heurística de escopo: 1 responsabilidade por task, ≤120 linhas, testável isolada; quando recusar/escalar |
| Checklist | Toda demanda tem objetivo claro? Há ambiguidade a resolver antes? Dependências mapeadas? Régua de qualidade anexada? |
| Anti-padrões | Task gigante; decisão ambígua repassada ao executor; codar na fase de planejamento; dependência circular |
| Exemplo gold | 1 demanda → plano de tasks modelo (referência de qualidade) |

**Sinal de 100%:** o plano que ele entrega não gera nenhuma pergunta do executor.

## 2. Agente Analista (análise de impacto) — Fase 1
**Papel:** dizer o que muda, o que quebra e o que arrisca **antes** de escrever qualquer task.

| Camada | Knowledge a embutir |
|---|---|
| Sabe | Mapa de dependências entre serviços; contratos das APIs em jogo; pontos de integração; dados afetados |
| Pensa | *Blast radius* (raio de impacto): entradas→efeitos colaterais→consumidores a jusante; retrocompatibilidade; idempotência |
| Checklist | Endpoints afetados? Breaking change em contrato? Impacto em performance? Observabilidade/log? Migração de dado? Segurança (dado sensível)? |
| Anti-padrões | Subestimar impacto; ignorar retrocompat; esquecer monitoração; tratar integração como "só uma chamada" |
| Exemplo gold | 1 demanda de "novo consumo de API" → análise de impacto modelo (JSON) |

**Sinal de 100%:** nada surpreende na execução; todo risco já estava no relatório.

## 3. Agente Tech Advisor (seleção de tecnologia/padrão) — Fase 2
**Papel:** entregar a decisão **mastigada** — qual lib, qual padrão, qual receita — para o executor não deliberar.

| Camada | Knowledge a embutir |
|---|---|
| Sabe | Tech Radar do banco (adotar/evitar); catálogo de padrões e skills; trade-offs de libs Java/Angular comuns |
| Pensa | Mapeamento problema→padrão (ex.: consumo de API → cliente resiliente com retry/circuit breaker; regra de negócio → Strategy/Specification; validação → Bean Validation) |
| Checklist | A escolha está no Radar? Passa nos gates Veracode/Sonar? Já existe skill/golden-path? Menor complexidade que resolve? |
| Anti-padrões | Escolher tech fora do Radar; over-engineering; reinventar algo que já é skill; padrão que falha no Veracode |
| Exemplo gold | 1 análise de impacto → "decision pack" modelo (libs + padrões + receita + justificativa em 1 linha cada) |

**Sinal de 100%:** o executor nunca precisa escolher stack — só seguir.

## 4. Agente Prompt Engineer (quebra em tasks/prompts) — Fase 3
**Papel:** transformar decisão + impacto em tasks que uma LLM executa sozinha, sem perguntar nada.

| Camada | Knowledge a embutir |
|---|---|
| Sabe | Anatomia da task-prompt (objetivo, contexto, passos, critérios de aceite, arquivos); padrões de código Java/Angular para dar esqueleto |
| Pensa | Granularidade (≤120 linhas, 1 responsabilidade); ordenação por dependência; cada task testável e incremental; embutir "decisões já tomadas" + snippet + gates |
| Checklist | A task é executável sem contexto externo? Critério de aceite é mensurável (Veracode/Sonar/lint/teste)? Tem arquivos esperados? Dependências explícitas? Snippet de partida? |
| Anti-padrões | Passo "implemente tudo"; critério vago ("funcionar bem"); dependência implícita; task que precisa de decisão não tomada |
| Exemplo gold | 1 decision pack → 1 task modelo (a "task gold" do `formato-task.md`) |

**Sinal de 100%:** qualquer task, dada a uma LLM isolada, produz código que passa nos gates de primeira.

---

## Como isso vira arquivo / Fonte de Conhecimento
Cada bloco acima é conhecimento — e vai para um dos dois canais:
- As **camadas 1–4 (sabe / pensa / checklist / anti-padrões)**, curtas e sempre necessárias, entram no **System Prompt** do agente (ou num `reference/agents/<papel>.md` que o harness injeta na fase).
- O **exemplo gold** e materiais volumosos (catálogo de snippets, ADRs, specs) entram como **Fonte de Conhecimento** (Custom/Snippet/API, conforme a Parte 4) — buscados por similaridade só quando relevantes.

Arquivos sugeridos: `reference/agents/techlead.md`, `analista.md`, `tech-advisor.md`, `prompt-engineer.md`. **Curto e citável** continua valendo — não duplicar o mesmo texto no System Prompt e na Fonte de Conhecimento.

## Para eu transformar isso em conteúdo real, me diz:
1. **Tipos de demanda mais frequentes** (novo endpoint, novo consumo, nova regra de negócio, nova tela) — pra eu escrever o *exemplo gold* de cada agente em cima de um caso real seu.
2. **2–3 "decisões que você sempre toma na mão hoje"** (ex.: "sempre uso X para cliente HTTP", "sempre valido assim") — viram o Radar + decision pack do Tech Advisor.
3. **As reprovações mais comuns de Veracode/Sonar** no seu time — viram o checklist anti-padrão do Analista e do Prompt Engineer.

---

> Fontes consultadas:
> - StackSpot (doc oficial): [Agents API](https://ai.stackspot.com/docs/agents/agent-api/agents-api), [Remote Quick Commands](https://ai.stackspot.com/docs/quick-commands/create-remote-qc), [Workflow / AI Prompt Execution](https://docs.stackspot.com/en/create-use/create-content/workflow/create-workflow/actions-workflow/ai-prompt-execution), [Knowledge Sources](https://ai.stackspot.com/docs/knowledge-source/ks), [Criar/atualizar KS via API](https://ai.stackspot.com/docs/knowledge-source/create-update-via-api).
> - Padrões: [Agent Decision Records (AgDR)](https://github.com/me2resh/agent-decision-record), [ADRs com AI coding assistants](https://blog.thestateofme.com/2025/07/10/using-architecture-decision-records-adrs-with-ai-coding-assistants/), [AGENTS.md vs ADR](https://ai.gopubby.com/agents-md-is-the-ew-architecture-decision-record-adr-3cfb6bdd6f2c), [Golden Paths (Platform Engineering)](https://platformengineering.com/features/golden-paths-should-let-the-spice-flow/), [GitHub Spec Kit (Spec-Driven Development)](https://github.com/github/spec-kit).

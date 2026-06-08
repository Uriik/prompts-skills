# Plano da POC — TechLead (skill + harness + StackSpot)

> Plano minucioso para colocar a POC de pé, derivado do
> `PLANO-IMPLEMENTACAO-TECHLEAD.md`. A EV2 (Devin/Workflow StackSpot) **não** faz
> parte desta POC.

## 0. Objetivo da POC
Provar, ponta a ponta, que dá para substituir o agente multiagente do Copilot
por: **skill local** (Windsurf/Claude Code) → **harness Python determinístico**
→ **StackSpot (Agent + Knowledge Sources)** como motor de linguagem, gerando um
plano de tasks pequenas com decisões já tomadas e gates de qualidade embutidos.

**Critério de sucesso:** rodar um comando e obter tasks em `.github/tasks/`,
cada uma ≤120 linhas, executável por uma LLM isolada sem deliberar stack.

## 1. Pré-requisitos
- Python 3.8+ no terminal (validado nesta POC com 3.10). **Zero** dependências
  externas (só biblioteca padrão).
- Acesso ao portal StackSpot AI com permissão para criar Agent + Knowledge
  Sources e gerar Service Credential (Client ID/Secret).
- (Corporativo) Se houver proxy, exportar `HTTPS_PROXY`/`HTTP_PROXY`.

## 2. Estrutura entregue (já criada nesta POC)
```
skill-techlead/
├── techlead/                  # a SKILL (entrypoint + cérebro + harness)
│   ├── SKILL.md               # entrypoint Claude Code
│   ├── reference/             # persona, arquitetura, padrões, radar, agentes, schemas
│   ├── scripts/               # harness Python (stdlib) + prompts
│   └── setup/                 # configure.py + .env.example
├── .windsurf/rules/techlead.md  # entrypoint Windsurf
├── stackspot-simulado/        # o que vai para a StackSpot (KS + system prompt) + mock
├── .github/tasks/             # SAÍDA: tasks geradas
└── .github/.techlead/         # context.md (Fase 0) + logs de execução
```

## 3. Passo a passo — rodar SEM StackSpot (modo mock)
Serve para validar o fluxo e demonstrar para o time, sem credenciais.

1. Abra um terminal na raiz `skill-techlead/`.
2. Rode:
   ```bash
   python techlead/scripts/techlead.py \
     --demanda "Criar consumo da API de Extrato e exibir os 10 ultimos lancamentos (Angular), ocultando estornados" \
     --contexto .github/.techlead/context.md \
     --mock
   ```
3. Confira a saída em `.github/tasks/` (4 tasks de exemplo) e o log em
   `.github/.techlead/runs/`.
4. (Opcional) `--dry-run` mostra as tasks sem gravar.

> No mock, o harness lê `stackspot-simulado/mock-responses/fase{1,2,3}.json` em
> vez de chamar a StackSpot. É o mesmo pipeline; só troca a fonte da resposta.

## 4. Passo a passo — colocar a StackSpot de verdade
### 4.1 Criar o Agent
1. Portal StackSpot AI → **Agents** → criar `techlead-core`.
2. **System Prompt:** cole o conteúdo de
   `stackspot-simulado/agente/techlead-core.system-prompt.md`.
3. Modelo: escolha o melhor disponível (ex.: GPT-5.1-mini).
4. Na aba **API Usage**, copie o `curl` — dele saem a **URL de token** e a **base
   URL do Agent** e o **Agent ID**.

### 4.2 Criar as Knowledge Sources
Para cada item de `stackspot-simulado/knowledge-sources/`, crie uma KS no tipo
indicado (ver `stackspot-simulado/README.md`):
- Custom (split SYNTACTIC): `ks-arquitetura`, `ks-tech-radar`, `ks-adr/*`,
  `ks-veracode`, `ks-sonar`.
- Snippet (split SYNTACTIC): `ks-snippets-java/*`, `ks-snippets-angular/*`.
- API (split ENDPOINT): `ks-apis-internas/extrato-api.openapi.yaml`.
Anexe as KS de persona (`ks-arquitetura`, `ks-tech-radar`, `ks-adr`) como padrão
do Agent.

### 4.3 Configurar credenciais locais
1. Gere sua **Service Credential** (Client ID/Secret) no portal.
2. Rode o wizard:
   ```bash
   python techlead/setup/configure.py
   ```
   Cole a URL de token, a base URL do Agent, Client ID/Secret e o Agent ID. O
   wizard grava `techlead/setup/.env` e testa a autenticação.

### 4.4 Rodar de verdade
```bash
python techlead/scripts/techlead.py \
  --demanda "<sua demanda>" \
  --contexto .github/.techlead/context.md
```
(O agente local — Windsurf/Claude Code — gera o `context.md` na Fase 0 lendo o
repo. Para a POC há um exemplo estático.)

## 5. O pipeline por dentro (o que o harness faz)
1. **Fase 0 (agente local):** lê o repo → `.github/.techlead/context.md`.
2. **Fase 1 (Analista):** demanda + contexto → JSON de impacto (valida schema).
3. **Fase 2 (Tech Advisor):** impacto → JSON de decisões (só do Radar/Catálogo).
4. **Fase 3 (Prompt Engineer):** decisões → JSON de tasks (mini-specs).
5. **Fase 4 (Python puro):** escreve `.github/tasks/NN.md`, **conta linhas**
   (≤120, com alerta se exceder) e grava o log da execução.

Cada fase: prompt rígido → 1 chamada → extrai JSON → valida → retry (até 2x) se
inválido. A coordenação é do Python; a StackSpot só gera linguagem.

## 6. Como evoluir o cérebro (sem mexer no código)
- Nova decisão de stack → edite `reference/tech-radar.md` (e KS equivalente).
- Nova receita → adicione um Golden Path em `reference/catalogo-skills.md`.
- Nova regra → `reference/arquitetura-itau.md` / `padroes-codigo.md`.
- Novo snippet → `stackspot-simulado/knowledge-sources/ks-snippets-*`.
O harness não muda; muda só o conhecimento.

## 7. Limitações conscientes da POC
- Validação de JSON é por chaves obrigatórias (não jsonschema completo) — sem
  dependências. Suficiente para a POC; dá para endurecer depois.
- Re-split automático de task >120 linhas está como **alerta** (não divide
  sozinho ainda). O ponto de extensão está no `writer.py`.
- O `context.md` da POC é estático; em uso real é gerado pelo agente local.

## 8. Checklist de aceite da POC
- [ ] `--mock` gera 4 tasks em `.github/tasks/`, todas ≤120 linhas.
- [ ] Cada task tem o bloco "Decisões já tomadas" e gates nos critérios.
- [ ] `configure.py` cria `.env` e autentica na StackSpot.
- [ ] Execução real gera tasks coerentes a partir do Agent + KS.

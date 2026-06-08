---
name: techlead
description: >-
  Aciona o TechLead para transformar uma demanda em um plano de tasks pequenas
  (≤120 linhas), com decisões de arquitetura/tecnologia já tomadas e gates de
  qualidade (Veracode/Sonar/lint) embutidos. Use quando o usuário pedir para
  "quebrar uma demanda em tasks", "agir como techlead", "planejar a
  implementação", "criar as tasks na pasta .github". NÃO escreve código nesta
  fase — só planeja.
---

# Skill: TechLead

Você é o agente local (Windsurf / Claude Code). Esta skill te ensina a acionar o
**TechLead**: um orquestrador determinístico em Python que usa a StackSpot como
motor de linguagem para planejar uma demanda em tasks executáveis.

## Quando usar
- O usuário tem uma demanda (nova feature, novo endpoint, novo consumo de API,
  nova regra de negócio, nova tela) e quer um plano de tasks.
- O usuário pede explicitamente "techlead", "quebrar em tasks", "planejar".

## Como acionar (passo a passo)

1. **Verifique as credenciais.** Se não existir `techlead/setup/.env`, peça ao
   usuário para rodar `python techlead/setup/configure.py` (cria o `.env` dele).
   Para testar o fluxo sem credenciais, use o modo `--mock`.

2. **Gere o contexto do repositório (Fase 0).** Em plan mode / modelo barato,
   leia o repositório e escreva um resumo curto em
   `.github/.techlead/context.md` (estrutura, stack, arquivos relevantes à
   demanda, pontos de integração). O harness NÃO varre o repo — recebe este
   resumo pronto.

3. **Rode o harness:**
   ```bash
   python techlead/scripts/techlead.py \
     --demanda "<texto da demanda do usuário>" \
     --contexto .github/.techlead/context.md
   ```
   Para demonstração sem StackSpot, acrescente `--mock`.
   Para revisar antes de gravar, acrescente `--dry-run`.

4. **Leia o resumo** que o harness imprime (quantidade de tasks, caminhos,
   tokens) e **abra as tasks** geradas em `.github/tasks/`.

5. **Execute uma task por vez.** Cada task em `.github/tasks/NN-*.md` é
   autossuficiente: traz "Decisões já tomadas" (não reabrir), passos, critérios
   de aceite (incluindo gates) e arquivos esperados. Implemente exatamente o que
   a task pede; não redecida stack nem padrão.

## Regras importantes
- Nesta fase de planejamento, **não escreva código de produção**.
- As regras de arquitetura, padrões e decisões ficam em `techlead/reference/`.
- Se uma task gerada parecer ambígua, isso é um defeito do plano: rode de novo
  ou ajuste o `reference/`, não improvise na execução.

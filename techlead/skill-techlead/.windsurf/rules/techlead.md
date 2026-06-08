---
trigger: manual
description: TechLead — planejar demanda em tasks via harness StackSpot
---

# Regra: TechLead (Windsurf / Cascade)

Quando o usuário pedir para **planejar uma demanda** ("agir como techlead",
"quebrar em tasks", "planejar a implementação"):

1. **NÃO escreva código de produção** nesta fase. Você é o planejador.
2. **Fase 0 (contexto):** leia o repositório e escreva um resumo curto em
   `.github/.techlead/context.md` (estrutura, stack, arquivos relevantes à
   demanda, pontos de integração). Use um modelo barato / plan mode.
3. **Rode o harness** (ele orquestra a StackSpot de forma determinística):
   ```bash
   python techlead/scripts/techlead.py \
     --demanda "<demanda do usuário>" \
     --contexto .github/.techlead/context.md
   ```
   Sem credenciais? Acrescente `--mock` para demonstrar o fluxo.
4. **Abra as tasks** geradas em `.github/tasks/` e execute **uma por vez**.
   Cada task traz "Decisões já tomadas" — siga sem redecidir stack/padrão.

As regras de arquitetura, Tech Radar, padrões e snippets ficam em
`techlead/reference/`. Se uma task parecer ambígua, é defeito do plano: rode de
novo ou ajuste o `reference/` — não improvise na execução.

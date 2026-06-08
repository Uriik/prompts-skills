# Task 04 — Criar componente Angular de lançamentos na Conta Corrente

> Objetivo: Exibir os 10 últimos lançamentos válidos na tela de Conta Corrente.
> Depende de: 03

## Decisões já tomadas (NÃO reabrir)
- Componente standalone consumindo ExtratoService (GP-04)
- Sem lógica de negócio no template (COD-07)
- Arquitetura/código: ARQ-07, COD-05, COD-07

## Passos
1. Criar LancamentosComponent standalone
2. Injetar ExtratoService e carregar lançamentos no init
3. Renderizar lista com data, valor e tipo; estado de loading e erro

## Critérios de aceite
- [ ] Tela exibe os lançamentos retornados pelo service
- [ ] Estado de loading e de erro visíveis ao usuário
- [ ] Sem lógica de negócio no template
- [ ] Lint ESLint sem erros

## Arquivos esperados
- `app-conta-corrente/.../lancamentos.component.ts`
- `app-conta-corrente/.../lancamentos.component.html`

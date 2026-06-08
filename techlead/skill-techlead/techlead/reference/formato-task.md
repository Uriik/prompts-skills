# Formato de Task (contrato de saída do plano)

Toda task gerada pelo TechLead segue este formato. É um **mini-spec**: uma LLM
isolada deve conseguir executá-lo sem perguntar nada. Limite: **≤120 linhas**.

## Anatomia

```markdown
# Task NN — <título curto e imperativo>

> Objetivo: <1 frase: o resultado esperado>
> Depende de: <IDs de tasks ou "nenhuma">

## Decisões já tomadas (NÃO reabrir)
- Stack/libs: <decisão> (fonte: RADAR-ADOTAR / ADR-xx)
- Padrão: <golden-path ou padrão> 
- Arquitetura: <IDs ARQ-xx aplicáveis>
- Snippets de partida: <caminhos em ks-snippets-*>

## Passos
1. <passo objetivo e verificável>
2. ...

## Critérios de aceite
- [ ] <critério mensurável>
- [ ] Veracode: 0 findings High/Medium
- [ ] Sonar: passa no quality gate
- [ ] Lint: sem erros

## Arquivos esperados
- `<caminho/Arquivo.java>`
- ...
```

## Regras do formato
- O bloco **"Decisões já tomadas"** é obrigatório — é o que impede o executor de
  deliberar.
- Critérios de aceite são **mensuráveis** (nada de "funcionar bem").
- Sempre listar os **arquivos esperados**.
- Se a task passar de 120 linhas, ela deve ser dividida (`NN-a`, `NN-b`).

## Exemplo gold
Ver `.github/tasks/` após rodar a POC em modo `--mock`, ou
`stackspot-simulado/mock-responses/fase3.json` para a estrutura de dados.

# Catálogo de Skills / Golden Paths (exemplo)

Lista **fechada** de padrões reutilizáveis. O Tech Advisor só pode escolher
itens daqui (evita alucinação). Cada item: ID, quando usar, o que entrega.

## Golden Paths (receitas de demanda recorrente)
- **GP-01 — Novo endpoint REST:** controller + service + DTO + teste + contrato
  OpenAPI. Use quando a squad vai EXPOR um recurso novo.
- **GP-02 — Novo consumo de API interna:** client resiliente (itau-rest-starter)
  + DTO de resposta + service + teste. Use quando a squad vai CONSUMIR uma API.
- **GP-03 — Nova regra de negócio:** service com a regra isolada + testes de
  cenário. Use para lógica de domínio.
- **GP-04 — Nova tela Angular:** component standalone + service HTTP +
  interceptor + tratamento de erro.

## Skills (padrões de implementação)
- **skill-rest-client-resiliente:** configura timeout/retry/circuit breaker no
  client (base ARQ-03/ARQ-04).
- **skill-observabilidade:** log estruturado com correlationId + métrica de
  latência (ARQ-05).
- **skill-mascaramento-dados:** mascarar conta/CPF em logs e respostas (ARQ-09).
- **skill-validacao-borda:** Bean Validation no controller / validação de form
  no Angular (ARQ-10).

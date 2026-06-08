# Task 01 — Criar client resiliente de consumo da API de Extrato

> Objetivo: Consumir GET /extrato/{conta}/lancamentos com resiliência e observabilidade.
> Depende de: nenhuma

## Decisões já tomadas (NÃO reabrir)
- Usar itau-rest-starter (NÃO criar cliente HTTP do zero) — RADAR-ADOTAR
- Configurar timeout, retry e circuit breaker (skill-rest-client-resiliente)
- Log estruturado com correlationId e máscara de conta (skill-observabilidade, skill-mascaramento-dados)
- Arquitetura/código: ARQ-03, ARQ-04, ARQ-05, ARQ-09
- Snippets de partida: ks-snippets-java/rest-client.java

## Passos
1. Criar ExtratoClient usando itau-rest-starter apontando para a API de Extrato
2. Mapear a resposta para LancamentoDto (campos: id, data, valor, tipo, estornado)
3. Configurar timeout=2s, retry=2, circuit breaker conforme padrão do starter
4. Adicionar log estruturado com correlationId; mascarar o número da conta

## Critérios de aceite
- [ ] ExtratoClient retorna lista de LancamentoDto a partir da API
- [ ] Falha da API não propaga stacktrace cru; circuit breaker ativo
- [ ] Número da conta aparece mascarado no log
- [ ] Veracode: 0 findings High/Medium
- [ ] Sonar: passa no quality gate
- [ ] Lint Checkstyle sem erros

## Arquivos esperados
- `modulo-conta-corrente/.../client/ExtratoClient.java`
- `modulo-conta-corrente/.../dto/LancamentoDto.java`

# Task 02 — Criar service com regra de ocultar lançamentos estornados

> Objetivo: Aplicar a regra de negócio e expor os 10 últimos lançamentos válidos.
> Depende de: 01

## Decisões já tomadas (NÃO reabrir)
- Regra de negócio isolada no service (ARQ-02, GP-03)
- Validação de entrada com Bean Validation (skill-validacao-borda)
- Arquitetura/código: ARQ-02, ARQ-10, COD-02, COD-03

## Passos
1. Criar ExtratoService que chama ExtratoClient
2. Filtrar lançamentos com estornado=true
3. Ordenar por data desc e limitar a 10
4. Validar a conta de entrada com Bean Validation
5. Cobrir com testes JUnit 5 + Mockito (cenários: com estornado, sem estornado, lista vazia)

## Critérios de aceite
- [ ] Lançamentos estornados nunca retornam
- [ ] Retorna no máximo 10, mais recentes primeiro
- [ ] Conta inválida retorna erro de validação tratado
- [ ] Cobertura de testes atende o quality gate do Sonar
- [ ] Veracode: 0 findings High/Medium
- [ ] Lint Checkstyle sem erros

## Arquivos esperados
- `modulo-conta-corrente/.../service/ExtratoService.java`
- `modulo-conta-corrente/.../service/ExtratoServiceTest.java`

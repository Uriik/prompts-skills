# Task 03 — Criar service Angular de consumo do extrato

> Objetivo: Acessar o backend de extrato via service dedicado e tipado.
> Depende de: 02

## Decisões já tomadas (NÃO reabrir)
- Acesso a API só via service Angular (ARQ-07)
- Headers internos via HttpInterceptor (ARQ-08) — RADAR-ADOTAR
- Observable tipado com catchError (COD-06)
- Arquitetura/código: ARQ-07, ARQ-08, COD-05, COD-06
- Snippets de partida: ks-snippets-angular/extrato.service.ts

## Passos
1. Criar ExtratoService Angular com HttpClient
2. Definir interface Lancamento (id, data, valor, tipo)
3. Tratar erro com catchError retornando estado de erro amigável

## Critérios de aceite
- [ ] Service retorna Observable<Lancamento[]> tipado
- [ ] Erro de rede tratado sem quebrar a tela
- [ ] Sem uso de any
- [ ] Lint ESLint sem erros

## Arquivos esperados
- `app-conta-corrente/.../extrato.service.ts`

# KS Sonar (Custom) — quality gate e regras

> Tipo StackSpot: **Custom** · Split: **SYNTACTIC**.

## Quality gate (exemplo)
- Cobertura mínima em código novo: 80%.
- 0 bugs e 0 vulnerabilidades em código novo.
- Code smells: rating de manutenibilidade ≥ A em código novo.
- Duplicação em código novo < 3%.

## Code smells recorrentes a evitar
- Método longo / alta complexidade ciclomática: extrair métodos.
- `catch` vazio ou engolir exceção (ver COD-02).
- Uso de `any` em TypeScript (ver COD-05).
- Variáveis/métodos sem uso.

## Regra de aceite
Toda task que gera código inclui: "Sonar: passa no quality gate".

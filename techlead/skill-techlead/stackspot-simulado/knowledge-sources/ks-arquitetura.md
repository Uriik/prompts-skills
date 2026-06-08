# KS Arquitetura (Custom) — regras citáveis

> Tipo StackSpot: **Custom** · Split: **SYNTACTIC** (por header).
> Versão de exemplo. Substitua pelas regras reais do banco.

## Camadas (Java)
- **ARQ-01** Camadas: controller → service → client/repository. Controller não
  chama client/repository direto.
- **ARQ-02** Regra de negócio no service. Controller só orquestra.
- **ARQ-03** Integração com API passa por client dedicado com timeout, retry e
  circuit breaker.

## Integração
- **ARQ-04** Consumo de API interna usa `itau-rest-starter`; não criar cliente
  HTTP do zero.
- **ARQ-05** Toda chamada externa é observável (log com correlationId + métrica).
- **ARQ-06** Mudança de contrato exposto exige versionamento.

## Frontend (Angular)
- **ARQ-07** Acesso a API só via service Angular dedicado.
- **ARQ-08** Headers internos via HttpInterceptor.

## Segurança
- **ARQ-09** Dado sensível nunca em log (mascarar conta/CPF).
- **ARQ-10** Validação de entrada em toda borda.

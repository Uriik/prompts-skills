# Regras de Arquitetura (exemplo — substitua pelas regras reais do banco)

> Conteúdo de exemplo para a POC. Cada regra tem um ID curto e citável para que
> os agentes referenciem nas saídas. Mantenha cada regra em 1–3 linhas.

## Camadas (backend Java)
- **ARQ-01** — Arquitetura em camadas: `controller` → `service` → `client`/
  `repository`. Controller nunca chama client/repository direto.
- **ARQ-02** — Regra de negócio mora no `service`. Controller só orquestra
  request/response; não contém lógica de domínio.
- **ARQ-03** — Toda integração com API externa/interna passa por um `client`
  dedicado, com tratamento de timeout, retry e circuit breaker.

## Contratos e integração
- **ARQ-04** — Consumo de API interna usa o SDK/starter interno do banco
  (`itau-rest-starter`); não criar cliente HTTP do zero.
- **ARQ-05** — Toda chamada externa é observável: log estruturado com
  `correlationId` e métrica de latência.
- **ARQ-06** — Mudança em contrato exposto exige versionamento; nunca quebrar
  retrocompatibilidade sem nova versão.

## Frontend (Angular)
- **ARQ-07** — Acesso a API só via `service` Angular dedicado; componente nunca
  chama `HttpClient` direto.
- **ARQ-08** — Autenticação/headers internos aplicados via `HttpInterceptor`.

## Segurança e dados
- **ARQ-09** — Dado sensível nunca em log. Mascarar conta/CPF.
- **ARQ-10** — Validação de entrada em toda borda (controller e formulário).

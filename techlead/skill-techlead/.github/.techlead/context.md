# Contexto do repositório (exemplo — gerado pela Fase 0 do agente local)

> Este arquivo seria gerado pelo Windsurf/Claude Code em plan mode ao ler o repo.
> Aqui é um exemplo estático para a POC rodar em modo --mock.

## Stack
- Backend: Java (Spring), módulo `modulo-conta-corrente`.
- Frontend: Angular, app `app-conta-corrente`.
- Integrações via API interna com `itau-rest-starter`.

## Arquivos/áreas relevantes à demanda
- `modulo-conta-corrente/.../client/` — onde ficam os clients de API.
- `modulo-conta-corrente/.../service/` — regras de negócio.
- `app-conta-corrente/.../` — componentes e services Angular.

## Pontos de integração
- API interna de Extrato (ver contrato em ks-apis-internas/extrato-api.openapi.yaml).

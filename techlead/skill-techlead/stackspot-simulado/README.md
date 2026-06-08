# stackspot-simulado/ — o que vai para a StackSpot

Esta pasta **simula** os artefatos que você vai cadastrar no portal da StackSpot.
Nada aqui é executado pelo harness em produção (exceto `mock-responses/`, usado
só no modo `--mock` para demonstrar o fluxo sem credenciais).

## Conteúdo

| Pasta/arquivo | O que é | Onde cadastrar na StackSpot |
|---|---|---|
| `agente/techlead-core.system-prompt.md` | System Prompt do Agent | Agents → criar `techlead-core` → System Prompt |
| `knowledge-sources/ks-arquitetura.md` | Regras de arquitetura | KS tipo **Custom**, split SYNTACTIC |
| `knowledge-sources/ks-tech-radar.md` | Tech Radar | KS tipo **Custom**, split NONE/SYNTACTIC |
| `knowledge-sources/ks-adr/` | Catálogo de ADRs | KS tipo **Custom**, split SYNTACTIC |
| `knowledge-sources/ks-veracode.md` | Padrões de remediação Veracode | KS tipo **Custom**, split SYNTACTIC |
| `knowledge-sources/ks-sonar.md` | Quality gate / regras Sonar | KS tipo **Custom**, split SYNTACTIC |
| `knowledge-sources/ks-snippets-java/` | Código-padrão Java | KS tipo **Snippet**, split SYNTACTIC |
| `knowledge-sources/ks-snippets-angular/` | Código-padrão Angular | KS tipo **Snippet**, split SYNTACTIC |
| `knowledge-sources/ks-apis-internas/` | Contratos OpenAPI | KS tipo **API**, split ENDPOINT |
| `mock-responses/` | Saídas simuladas das 3 fases | NÃO vai para a StackSpot (uso local `--mock`) |

## Mapa: qual KS alimenta cada fase

- **Persona (sempre):** `ks-arquitetura`, `ks-tech-radar`, `ks-adr`
- **Fase 1 (Analista):** + `ks-apis-internas`
- **Fase 2 (Tech Advisor):** + `ks-tech-radar`, `ks-adr`, `ks-veracode`, `ks-sonar`
- **Fase 3 (Prompt Engineer):** + `ks-snippets-java`, `ks-snippets-angular`, `ks-veracode`, `ks-sonar`

> Recomendado: 1 Agent base `techlead-core` com os KS de persona como padrão; o
> harness seleciona os KS extras por chamada (parâmetro `knowledge_sources`).

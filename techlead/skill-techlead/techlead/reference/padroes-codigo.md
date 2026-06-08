# Padrões de Código (exemplo — substitua pelos padrões reais do banco)

> IDs `COD-xx` citáveis. Mantém curto. Estes alimentam principalmente a fase de
> quebra em tasks (Prompt Engineer).

## Java
- **COD-01** — Nomenclatura: classes em `PascalCase`, métodos/variáveis em
  `camelCase`, pacotes em minúsculo. Sufixos: `Controller`, `Service`,
  `Client`, `Dto`.
- **COD-02** — Tratamento de erro: exceções de negócio estendem
  `NegocioException`; nunca engolir exceção (sem `catch` vazio).
- **COD-03** — Todo método público de `service` tem teste unitário (JUnit +
  Mockito). Cobertura mínima do quality gate do Sonar.
- **COD-04** — DTOs imutáveis sempre que possível; validação com Bean
  Validation (`@NotNull`, `@Valid`).

## Angular / TypeScript
- **COD-05** — Componentes `standalone` quando aplicável; `service` para acesso
  a dados; tipos explícitos (sem `any`).
- **COD-06** — Chamadas HTTP retornam `Observable` tipado; tratar erro com
  `catchError`.
- **COD-07** — Sem lógica de negócio no template; usar `pipe`/`service`.

## Geral
- **COD-08** — Mensagens, logs e identificadores em padrão do banco; sem dado
  sensível.
- **COD-09** — Lint obrigatório: Checkstyle/SpotBugs (Java), ESLint (Angular).

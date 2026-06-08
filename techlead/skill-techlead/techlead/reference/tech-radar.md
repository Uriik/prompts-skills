# Tech Radar (exemplo — substitua pelas decisões reais do banco)

Resolve as microdecisões antes que existam. O Tech Advisor escolhe **só** daqui.

## ADOTAR (default — use sem discutir)
- **Cliente HTTP (Java):** `itau-rest-starter` (wrapper interno sobre Spring
  WebClient). Resiliência (retry + circuit breaker) já incluída.
- **Validação (Java):** Bean Validation (`jakarta.validation`).
- **Testes (Java):** JUnit 5 + Mockito.
- **HTTP (Angular):** `HttpClient` + `HttpInterceptor` interno do banco.
- **Estado (Angular):** Signals para estado local simples.

## EXPERIMENTAR (ok em piloto, com aval do TechLead)
- Resilience4j custom (quando o starter interno não cobre o caso).

## AVALIAR (estudar, ainda não usar em produção)
- Novas libs de mapeamento DTO além do padrão atual.

## EVITAR (não usar)
- Criar cliente HTTP do zero (`RestTemplate` manual, `fetch` cru no componente).
- Lógica de negócio no controller ou no template Angular.
- Libs externas não homologadas pela segurança do banco.

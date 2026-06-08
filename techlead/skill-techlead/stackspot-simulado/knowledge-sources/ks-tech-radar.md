# KS Tech Radar (Custom)

> Tipo StackSpot: **Custom** · Split: **NONE** ou **SYNTACTIC**.
> O Tech Advisor escolhe SÓ daqui.

## ADOTAR
- Cliente HTTP (Java): `itau-rest-starter` (WebClient interno, resiliência inclusa).
- Validação (Java): Bean Validation.
- Testes (Java): JUnit 5 + Mockito.
- HTTP (Angular): HttpClient + HttpInterceptor interno.
- Estado (Angular): Signals para estado local simples.

## EXPERIMENTAR
- Resilience4j custom (quando o starter não cobre o caso, com aval do TechLead).

## AVALIAR
- Novas libs de mapeamento DTO além do padrão atual.

## EVITAR
- Cliente HTTP do zero (RestTemplate manual, fetch cru no componente).
- Lógica de negócio no controller ou no template Angular.
- Libs externas não homologadas pela segurança.

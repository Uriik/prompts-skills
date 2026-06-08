# ADR-012 — Cliente HTTP padrão para consumo de APIs internas

- **Status:** Aceito
- **Data:** 2025-01-15

## Contexto
Squads criavam clientes HTTP de formas diferentes (RestTemplate manual, WebClient
cru), gerando inconsistência em timeout, retry e observabilidade, e findings
recorrentes de Veracode/Sonar.

## Decisão
Todo consumo de API interna usa o **`itau-rest-starter`** (wrapper interno sobre
Spring WebClient), que já entrega timeout, retry, circuit breaker e log
estruturado padronizados.

## Alternativas rejeitadas
- **RestTemplate manual:** sem resiliência nativa; depreciado.
- **WebClient cru:** exige reconfigurar resiliência em cada squad; propenso a erro.

## Consequência
Menos código por squad, menos findings de segurança, observabilidade uniforme.
Quem precisa de comportamento fora do starter abre exceção via TechLead.

// KS Snippet (Java) — client resiliente padrão (itau-rest-starter)
// Tipo StackSpot: Snippet · Split: SYNTACTIC
// Esqueleto de partida para a Task 01 (consumo de API interna).

@Component
public class ExtratoClient {

    private final RestClientInterno restClient; // itau-rest-starter

    public ExtratoClient(RestClientInterno restClient) {
        this.restClient = restClient;
    }

    // Resiliência (timeout/retry/circuit breaker) configurada no starter.
    public List<LancamentoDto> buscarLancamentos(String conta) {
        // correlationId e máscara de conta tratados pelo log estruturado do starter
        return restClient
                .get("/extrato/{conta}/lancamentos", conta)
                .retrieveList(LancamentoDto.class);
    }
}

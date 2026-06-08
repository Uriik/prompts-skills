// KS Snippet (Java) — controller padrão (GP-01)
// Tipo StackSpot: Snippet · Split: SYNTACTIC
// Controller só orquestra (ARQ-02); validação de borda (ARQ-10).

@RestController
@RequestMapping("/contas/{conta}/extrato")
public class ExtratoController {

    private final ExtratoService extratoService;

    public ExtratoController(ExtratoService extratoService) {
        this.extratoService = extratoService;
    }

    @GetMapping("/lancamentos")
    public List<LancamentoDto> listar(@PathVariable @NotBlank String conta) {
        return extratoService.ultimosLancamentos(conta);
    }
}

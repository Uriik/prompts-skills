# KS Veracode (Custom) — padrões de remediação

> Tipo StackSpot: **Custom** · Split: **SYNTACTIC**.
> Exemplos das reprovações mais comuns + como evitar já na escrita.

## Categorias frequentes e remediação
- **Injection (SQL/Command):** usar queries parametrizadas; nunca concatenar
  entrada do usuário. Validar e normalizar entradas.
- **CRLF / Log Injection:** sanitizar dados antes de logar; usar log estruturado
  (não interpolar entrada crua no log).
- **Sensitive Data Exposure:** nunca logar conta, CPF, token. Mascarar
  (skill-mascaramento-dados).
- **Improper Input Validation:** Bean Validation em toda borda (ARQ-10).
- **Insecure Deserialization:** desserializar só tipos esperados; evitar
  desserialização genérica de payload externo.

## Regra de aceite
Toda task que gera código backend inclui: "Veracode: 0 findings High/Medium".

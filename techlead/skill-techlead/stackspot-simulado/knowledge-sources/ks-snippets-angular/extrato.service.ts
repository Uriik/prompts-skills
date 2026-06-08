// KS Snippet (Angular) — service de consumo padrão (GP-04)
// Tipo StackSpot: Snippet · Split: SYNTACTIC
// Acesso a API só via service (ARQ-07); Observable tipado + catchError (COD-06).

@Injectable({ providedIn: 'root' })
export class ExtratoService {
  private readonly http = inject(HttpClient);
  private readonly base = '/contas';

  // Headers internos aplicados pelo HttpInterceptor (ARQ-08).
  listarLancamentos(conta: string): Observable<Lancamento[]> {
    return this.http
      .get<Lancamento[]>(`${this.base}/${conta}/extrato/lancamentos`)
      .pipe(catchError(() => of([])));
  }
}

export interface Lancamento {
  id: string;
  data: string;
  valor: number;
  tipo: string;
}

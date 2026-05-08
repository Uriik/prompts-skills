# Hooks Agent - Guide

## O que faz?

Cria **HOOKS** para policy enforcement automático (validação, formatação)

Hooks rodam em background em eventos específicos (sessionStart, postCodeGeneration, etc).

## Arquivos nesta pasta

- `agente-hooks.md` - O agente completo com fluxo passo-a-passo
- `TEMPLATE-hook.json` - Template vazio para você preencher
- `exemplos/` - Exemplos prontos
  - `exemplo-enforce-naming.json` - Valida naming conventions
  - `exemplo-enforce-testing.json` - Valida coverage 80%

## Como usar?

1. Abra `agente-hooks.md`
2. Descreva a policy (que validações fazer?)
3. Ele gera JSON com ações e regras
4. Ele valida JSON syntax
5. Copie para `.github/hooks/seu-hook.json`
6. Hook ativa automaticamente no próximo evento

## Estrutura JSON

```json
{
  "name": "policy-name",
  "description": "O que valida",
  "version": "1.0.0",
  "enabled": true,
  "events": ["sessionStart", "postCodeGeneration"],
  "actions": [
    {
      "type": "validate|format|alert|block",
      "rules": [...]
    }
  ]
}
```

## Eventos Suportados (7 tipos)

- `sessionStart` - Quando inicia uma sessão
- `sessionEnd` - Quando termina uma sessão
- `preToolUse` - Antes de usar uma tool
- `postToolUse` - Depois de usar uma tool
- `preCodeGeneration` - Antes de gerar código
- `postCodeGeneration` - Depois de gerar código
- `messageReceived` - Quando recebe mensagem

## Tipos de Action

- `validate` - Valida código contra regras
- `format` - Formata código (prettier, eslint)
- `alert` - Mostra alerta (info, warning, error)
- `block` - Bloqueia ação e mostra mensagem

## Exemplos

- `exemplo-enforce-naming.json` - Valida camelCase, PascalCase, UPPER_SNAKE_CASE
- `exemplo-enforce-testing.json` - Valida teste file + coverage 80%

Copie e adapte conforme necessário!

## ⚠️ IMPORTANTE

**Hooks APENAS funcionam em `.github/hooks/`**

NÃO funcionam em `~/.copilot/hooks/` ou outro local!

## Tempo estimado

10-15 minutos por hook

## Token cost

0 tokens (executa em background, não conta)

---

Para voltar ao overview, veja `../README.md`

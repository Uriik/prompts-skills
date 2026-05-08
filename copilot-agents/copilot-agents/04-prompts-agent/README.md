# Prompts Agent - Guide

## O que faz?

Cria **PROMPTS** (slash commands) para tarefas repetitivas (/create, /test, /optimize)

Prompts são atalhos que economizam tokens ao executar tarefas padronizadas.

## Arquivos nesta pasta

- `agente-prompts.md` - O agente completo com fluxo passo-a-passo
- `TEMPLATE-prompt.md` - Template vazio para você preencher
- `exemplos/` - Exemplos prontos
  - `exemplo-create-component.prompt.md` - Criar componentes React
  - `exemplo-create-hook.prompt.md` - Criar custom hooks

## Como usar?

1. Abra `agente-prompts.md`
2. Descreva a tarefa automática (nome, inputs, outputs)
3. Ele gera template com YAML + exemplos
4. Ele valida parâmetros e formato de saída
5. Copie para `.github/prompts/seu-prompt.prompt.md`
6. Use via `/seu-prompt arg1 arg2` no Copilot

## Seções que serão criadas

1. Purpose
2. What This Prompt Does
3. How to Use
4. Input Parameters
5. Output Format
6. Examples (2-3 exemplos concretos)
7. Tips & Tricks
8. Related Prompts

## Exemplos

- `exemplo-create-component.prompt.md` - `/create-component Modal dialog`
- Mostra como estruturar exemplos com Input/Output

## Tempo estimado

10-15 minutos por prompt

## Token cost

0 se não invocar, ~150-200 tokens se usar

---

Para voltar ao overview, veja `../README.md`

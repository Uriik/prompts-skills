# 🚀 GitHub Copilot - Agentes Especializados

**Versão:** 1.0  
**Data:** Maio 2026  
**Objetivo:** 5 Agentes modulares para criar Instructions, Agents, Skills, Prompts e Hooks com economia de tokens

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura de Pastas](#estrutura-de-pastas)
3. [Como Usar Cada Agente](#como-usar-cada-agente)
4. [Economia de Tokens](#economia-de-tokens)
5. [Checklist Rápido](#checklist-rápido)

---

## 🎯 Visão Geral

Este pacote contém **5 agentes especializados** para criar e validar componentes do GitHub Copilot:

| Agente | Foco | Tipo | Linhas | Token Cost |
|--------|------|------|--------|-----------|
| **Instructions Agent** | Padrões globais | `.md` puro | ≤55 | 40-80/req |
| **Agents Agent** | Personas especializadas | `.agent.md` | ≤110 | ~50/session |
| **Skills Agent** | Tarefas reutilizáveis | `SKILL.md` | ≤330 | 5-10 + 250 |
| **Prompts Agent** | Atalhos slash commands | `.prompt.md` | ≤165 | 0 ou ~150 |
| **Hooks Agent** | Policy enforcement | `.json` | - | 0 (background) |

---

## 📁 Estrutura de Pastas

```
copilot-agents/
│
├── 01-instructions-agent/
│   ├── agente-instructions.md        (documentação do agente)
│   ├── TEMPLATE-instructions.md      (template vazio)
│   └── README.md                     (instruções)
│
├── 02-agents-agent/
│   ├── agente-agents.md             
│   ├── TEMPLATE-agent.md            
│   ├── exemplos/
│   │   └── exemplo-developer.agent.md
│   └── README.md
│
├── 03-skills-agent/
│   ├── agente-skills.md             
│   ├── TEMPLATE-skill.md            
│   ├── skill-testing/
│   │   └── SKILL.md
│   ├── skill-debugging/
│   │   └── SKILL.md
│   ├── skill-code-review/
│   │   └── [template]
│   ├── skill-documentation/
│   │   └── [template]
│   └── README.md
│
├── 04-prompts-agent/
│   ├── agente-prompts.md            
│   ├── TEMPLATE-prompt.md           
│   ├── exemplos/
│   │   ├── exemplo-create-component.prompt.md
│   │   └── exemplo-create-hook.prompt.md
│   └── README.md
│
├── 05-hooks-agent/
│   ├── agente-hooks.md              
│   ├── TEMPLATE-hook.json           
│   ├── exemplos/
│   │   ├── exemplo-enforce-naming.json
│   │   └── exemplo-enforce-testing.json
│   └── README.md
│
└── README.md (este arquivo)
```

---

## 🤖 Como Usar Cada Agente

### 1️⃣ Instructions Agent

**Quando usar**: Criar padrões globais para seu projeto

**Arquivo gerado**: `.github/copilot-instructions.md`

**Processo**:
1. Abra o agente em `01-instructions-agent/agente-instructions.md`
2. Ele fará perguntas sobre seu tech stack
3. Ele gerará um template de ~55 linhas
4. Ele validará estrutura automaticamente
5. Você copia o resultado para `.github/copilot-instructions.md`

**Custo**: 40-80 tokens por requisição (sempre carregado)

### 2️⃣ Agents Agent

**Quando usar**: Criar personas especializadas (@developer, @pm, @tech-lead)

**Arquivo gerado**: `.github/agents/nome.agent.md`

**Processo**:
1. Abra o agente em `02-agents-agent/agente-agents.md`
2. Descreva a persona e suas responsabilidades
3. Ele gerará template estruturado com YAML
4. Valida seções obrigatórias
5. Você copia para `.github/agents/seu-agente.agent.md`

**Exemplo**: Veja `exemplos/exemplo-developer.agent.md`

**Custo**: ~50 tokens quando selecionado

### 3️⃣ Skills Agent

**Quando usar**: Criar tarefas reutilizáveis (/testing, /debug, /review)

**Arquivo gerado**: `.github/skills/nome/SKILL.md`

**Processo**:
1. Abra o agente em `03-skills-agent/agente-skills.md`
2. Descreva a tarefa que a skill automatizará
3. Ele gerará template com 8 seções essenciais
4. Gera estrutura de pastas (scripts/, templates/)
5. Você copia SKILL.md + estrutura para `.github/skills/`

**Exemplos**: 
- `skill-testing/SKILL.md` - Criar testes com Jest
- `skill-debugging/SKILL.md` - Debugar issues

**Custo**: 5-10 discovery + 250 se ativada

### 4️⃣ Prompts Agent

**Quando usar**: Criar atalhos para tarefas repetitivas (/create, /optimize)

**Arquivo gerado**: `.github/prompts/nome.prompt.md`

**Processo**:
1. Abra o agente em `04-prompts-agent/agente-prompts.md`
2. Descreva a tarefa automática
3. Ele gerará prompt com exemplo de uso
4. Valida parameters e output format
5. Você copia para `.github/prompts/seu-prompt.prompt.md`

**Exemplo**: Veja `exemplos/exemplo-create-component.prompt.md`

**Custo**: ~150-200 tokens quando invocado

### 5️⃣ Hooks Agent

**Quando usar**: Aplicar policies obrigatórias (validação, formatação)

**Arquivo gerado**: `.github/hooks/seu-hook.json`

**Processo**:
1. Abra o agente em `05-hooks-agent/agente-hooks.md`
2. Descreva a policy (que validações fazer?)
3. Ele gerará JSON com validações/formatações
4. Valida JSON syntax e eventos
5. Você copia para `.github/hooks/seu-hook.json`

**Exemplos**:
- `exemplos/exemplo-enforce-naming.json` - Validar naming conventions
- `exemplos/exemplo-enforce-testing.json` - Validar coverage 80%

**Custo**: 0 tokens (executa em background)

⚠️ **IMPORTANTE**: Hooks APENAS funcionam em `.github/hooks/` - não suportam `~/.copilot/hooks/`

---

## 💰 Economia de Tokens

### Antes (sem estrutura modular)
```
1 Agente monolítico com TUDO = ~200-300 linhas
Carregado: SEMPRE
Token cost: 100-200 por requisição
Total por sessão: 500-1000+ tokens
```

### Depois (com 5 agentes)
```
Instructions + Agents + Skills + Prompts + Hooks
Carregados: Cada um sob demanda
Token cost: ~40-50 base + ativação conforme necessidade
Total por sessão: 200-300 tokens (70-80% redução!)
```

---

## ✅ Checklist Rápido

### Ao criar uma nova INSTRUCTION
- [ ] Tem 6 seções? (Tech Stack, Naming, Structure, Error Handling, TypeScript, Testing)
- [ ] Tem exemplos ✅ e ❌?
- [ ] Tamanho ≤ 55 linhas?
- [ ] Sem YAML frontmatter?

### Ao criar um novo AGENT
- [ ] Tem YAML válido? (name, description, model, tools)
- [ ] Tem 7 seções? (Core Responsibilities, Communication Style, Decision-Making, Tools, Handoffs)
- [ ] Model é válido? (Opus ou Sonnet)
- [ ] Tamanho ≤ 110 linhas?

### Ao criar uma nova SKILL
- [ ] Tem YAML válido? (name, description, allowed-tools)
- [ ] Tem 8 seções? (Overview, When to Use, Steps, Templates, Best Practices, Troubleshooting, References)
- [ ] Description tem keywords para discovery?
- [ ] Tamanho ≤ 330 linhas?
- [ ] Tem pasta skill-nome/ com SKILL.md?

### Ao criar um novo PROMPT
- [ ] Tem YAML válido? (description, agent, model, tools, argument-hint)
- [ ] Tem 8 seções? (Purpose, What It Does, How to Use, Input Parameters, Output Format, Examples, Tips)
- [ ] Tem exemplos de uso concretos?
- [ ] Tamanho ≤ 165 linhas?

### Ao criar um novo HOOK
- [ ] É JSON válido?
- [ ] Tem: name, description, version, events, enabled, actions?
- [ ] Events são válidos? (sessionStart, preCodeGeneration, etc)
- [ ] Actions têm type válido? (validate, format, alert, block)
- [ ] Está em `.github/hooks/` (NÃO em ~/.copilot/hooks/)?

---

## 🚀 Próximos Passos

1. **Escolha um agente** para começar (recomendo: Instructions)
2. **Use o agente** para gerar seu primeiro template
3. **Copie o resultado** para a estrutura de seu projeto
4. **Commit e push**
5. **Use o resultado** no GitHub Copilot

---

## 📞 Suporte & Dúvidas

Se tiver dúvidas durante o processo:
- Consulte o arquivo `agente-[tipo].md` do componente
- Veja exemplos em `exemplos/`
- Revise o template em `TEMPLATE-[tipo].[md|json]`

---

**Documento v1.0 - 5 Agentes Modulares para Máxima Eficiência de Tokens**

**Última atualização**: Maio 2026

# 📁 Estrutura Completa da Pasta `.claude/` - Guia Detalhado

**Fonte:** Documentação oficial Anthropic + Best Practices da comunidade (2026)

-----

## 🎯 Visão Geral

A pasta `.claude/` (ou `~/.claude/` para configuração global) controla o comportamento do Claude Code. Ela controla 5 subsistemas distintos: instruções (CLAUDE.md e rules), workflows (skills e commands), especialistas (agents), permissões (settings.json), e memória (diretório global ~/.claude/).

### 📊 Dois Níveis de Configuração

|Nível      |Localização |Escopo                |Compartilhamento        |
|-----------|------------|----------------------|------------------------|
|**Projeto**|`./.claude/`|Seu projeto específico|✅ Commit no Git         |
|**Global** |`~/.claude/`|Todos os seus projetos|❌ Pessoal (não commitar)|

-----

## 🏗️ Estrutura Recomendada Completa

```
seu-projeto/
│
├── CLAUDE.md                    # ⭐ Arquivo principal (OBRIGATÓRIO)
├── TASKS.md                     # ⭐ Tarefas para Claude implementar (RECOMENDADO)
│
└── .claude/
    ├── CLAUDE.md               # (Opcional) Sobrescreve raiz em subpastas
    ├── settings.json           # 🔐 Configurações e permissões
    ├── .claudeignore          # Arquivos ignorados
    │
    ├── rules/                  # 📋 Regras modularizadas
    │   ├── code-style.md
    │   ├── testing.md
    │   ├── security.md
    │   ├── api-conventions.md
    │   └── database/
    │       └── queries.md
    │
    ├── skills/                 # 🎯 Habilidades (workflows especializados)
    │   ├── pdf-processor/
    │   │   ├── SKILL.md
    │   │   ├── extract_text.py
    │   │   └── templates/
    │   │       └── summary.html
    │   │
    │   ├── security-audit/
    │   │   ├── SKILL.md
    │   │   ├── checklist.md
    │   │   └── templates/
    │   │       └── report.md
    │   │
    │   └── deploy/
    │       ├── SKILL.md
    │       └── scripts/
    │           └── release-notes.js
    │
    ├── commands/               # 🔥 Comandos slash customizados
    │   ├── next-task.md        # ⭐ Implementar próxima tarefa
    │   ├── batch-implement.md  # ⭐ Implementar todas as tarefas
    │   ├── test.md
    │   ├── review.md
    │   └── deploy.md
    │
    ├── agents/                 # 🤖 Agentes especializados
    │   ├── code-reviewer/
    │   │   └── AGENT.md
    │   └── infrastructure/
    │       └── AGENT.md
    │
    ├── hooks/                  # 🪝 Event handlers
    │   ├── pre-commit.sh
    │   └── post-test.sh
    │
    └── memory/                 # 🧠 Memória automática (gerada)
        └── session-history.json
```

-----

## 📌 ARQUIVO RAIZ: CLAUDE.md

### ✅ O Que É Obrigatório

Claude Code lê CLAUDE.md, settings.json, hooks, skills, commands, subagents e auto memory da pasta do projeto e de ~/.claude do diretório home.

### 📐 Formato e Estrutura

**Tamanho recomendado:** <60 linhas (máximo 300)

```markdown
# [Nome do Projeto]

## Visão Geral
[1-2 linhas descrevendo o projeto]

## Stack de Tecnologia
- **Frontend:** React + TypeScript
- **Backend:** Node.js + Express
- **Database:** PostgreSQL
- **Testes:** Jest + Testing Library

## Comandos Bash Essenciais
- npm run dev: Inicia servidor de desenvolvimento
- npm run build: Build para produção
- npm test: Roda suite de testes
- npm run typecheck: Verifica tipos TypeScript

## Estilo de Código
- **IMPORTANTE:** Use ES modules (import/export), não CommonJS (require)
- Destructure imports quando possível: `import { foo } from 'bar'`
- Use TypeScript strict mode em todos os arquivos
- Nunca commite arquivos .env

## Workflow & Testes
- **YOU MUST** rodar npm test antes de marcar como pronto
- **YOU MUST** rodar npm run typecheck para verificar tipos
- Prefira testes unitários, use integração com moderação
- Escreva testes ANTES da implementação (TDD preferido)

## Decisões Arquiteturais
- Componentes React: src/components/ com co-located tests
- Services: src/services/ para lógica de negócio
- Utils: src/utils/ apenas para funções puras

## Regras de Segurança
- **NUNCA:** Commite secrets, API keys, tokens
- **NUNCA:** Submeta .env ou arquivos locais
- Sempre valide inputs do usuário
- Use prepared statements para SQL

## Branch e Commits
- Nomenclatura: feature/*, bugfix/*, hotfix/*
- Commits atômicos e descritivos
- Rebase preferido (não squash em PRs)

## Regras Específicas Deste Projeto
- Se vê um padrão não documentado → pergunte primeiro
- Leia .claude/rules/* para regras específicas por domínio
```

### 🔍 Exemplo Minimalista (Ideal)

```markdown
# MyApp

## Tech Stack
- Next.js 15, TypeScript, Tailwind CSS
- PostgreSQL + Prisma ORM
- Jest + React Testing Library

## Commands
- npm run dev: dev server
- npm run build: production build
- npm test: run tests
- npm run lint: ESLint

## Essentials
- **IMPORTANT:** TypeScript strict mode required
- Never commit .env or secrets
- Write tests with TDD pattern
- Run npm test before marking done

## Conventions
- src/components/: React components with co-located .test.tsx
- src/lib/: Utility functions and helpers
- Prefer functional components and hooks
```

-----

## 📋 ARQUIVO: .claude/rules/

### ✅ Objetivo

Quando seu time cresce, você acaba com um CLAUDE.md de 300 linhas que ninguém mantém. A pasta rules/ resolve isso. Cada arquivo markdown dentro .claude/rules/ é carregado automaticamente. Em vez de um arquivo gigante, você divide instruções por preocupação.

### 📂 Estrutura Recomendada

```
.claude/rules/
├── code-style.md           # Padrões de código
├── testing.md              # Estratégia de testes
├── security.md             # Regras de segurança
├── api-conventions.md      # Convenções de API
├── database/
│   └── queries.md          # Padrões de query
└── performance.md          # Otimizações
```

### 📝 Exemplo: `rules/code-style.md`

```markdown
---
paths: ["src/**/*.ts", "src/**/*.tsx"]
priority: medium
---

# Code Style Rules

## TypeScript
- Always use `interface` for object shapes, `type` for unions
- Avoid `any` - use `unknown` with type guards
- Strict mode: no implicit `any`

## React Components
- Functional components only (no class components)
- Use hooks: `useState`, `useEffect`, `useCallback`
- Props destructuring at function signature
- One component per file

## File Naming
- Components: PascalCase (Button.tsx)
- Utilities: camelCase (formatDate.ts)
- Tests: [name].test.ts or [name].spec.ts

## Imports Organization
```typescript
// 1. External libraries
import React from 'react';
import { useState } from 'react';

// 2. Internal modules (absolute imports)
import { Button } from '@/components/Button';

// 3. Relative imports
import { helper } from '../utils/helper';

// 4. Side effects
import './styles.css';
```

## Formatting

- Use Prettier (already configured)
- Line length: 100 characters
- Semicolons: required
- Quotes: single quotes

```
### 📝 Exemplo: `rules/testing.md`

```markdown
---
paths: ["src/**/*.test.ts", "src/**/*.test.tsx"]
priority: high
---

# Testing Standards

## TDD Pattern
- Write test first
- Make it fail (RED)
- Write minimal code to pass (GREEN)
- Refactor (REFACTOR)

## Test Structure
```javascript
describe('Button component', () => {
  it('should render with text prop', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick handler', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

## Coverage Requirements

- Minimum 80% coverage
- 100% coverage for utilities
- Happy path + error cases

## What To Test

- ✅ User interactions
- ✅ State changes
- ✅ Edge cases and errors
- ❌ Implementation details
- ❌ Third-party library behavior

## Avoid

- Testing internal state
- Testing private methods
- Mock unnecessarily

```
### 📝 Exemplo: `rules/security.md`

```markdown
---
priority: critical
---

# Security Rules

## Data Protection
- **NEVER** hardcode passwords, keys, tokens
- Use environment variables for secrets
- Validate and sanitize ALL user inputs
- Use parameterized queries (no string concat for SQL)

## Authentication
- Implement rate limiting on login endpoints
- Hash passwords with bcrypt (min 10 rounds)
- Store JWT in httpOnly cookies
- CSRF protection on state-changing endpoints

## Authorization
- Check user permissions on every protected route
- Principle of least privilege
- Audit log sensitive operations

## Dependencies
- Run `npm audit` regularly
- Update packages monthly
- Review dependency license compatibility

## Environment Variables
```bash
# GOOD: Use .env.example (no secrets)
DATABASE_URL=postgresql://localhost/mydb
API_TIMEOUT=5000

# BAD: NEVER commit this
ADMIN_PASSWORD=supersecret123
JWT_SECRET=my-secret-key
```

## Sensitive Files

- .env* files
- private keys
- credentials
- API keys

Must be in .gitignore

```
---

## 🎯 ARQUIVO: .claude/skills/

### ✅ O Que É

Skills são pastas contendo um arquivo SKILL.md e scripts/recursos opcionais. Subpastas são permitidas (e encorajadas) para organizar helper scripts, templates e arquivos de dados.

### 📂 Estrutura de uma Skill
```

skill-name/
├── SKILL.md              # Descrição + instruções (OBRIGATÓRIO)
├── scripts/              # Scripts executáveis
│   ├── helper.py
│   └── processor.js
├── references/           # Documentação de referência
│   └── api-docs.md
├── templates/            # Modelos/templates
│   └── report.html
└── assets/              # Arquivos usados em output
├── icons/
└── styles/

```
### 📝 Exemplo Completo: `skills/pdf-processor/SKILL.md`

```yaml
---
name: pdf-processor
description: Extract, analyze, and transform text from PDF documents. Use when processing PDFs, extracting tables, generating summaries, or converting to other formats.
allowed-tools: [read, write, bash]
---

# PDF Processor Skill

## Purpose
This skill enables Claude to handle PDF documents end-to-end: extract text, identify structure, handle images, and generate summaries.

## When To Use
- User asks to "analyze this PDF"
- Extract data/tables from PDF
- Convert PDF to markdown/JSON
- Generate summary reports
- OCR scanned documents

## How To Use

### 1. Extract Text
```bash
python scripts/extract_text.py input.pdf output.txt
```

### 2. Extract Tables

```bash
python scripts/extract_tables.py input.pdf output.json
```

### 3. Generate Summary

```bash
python scripts/summarize.py input.pdf --length short
```

## Implementation Details

- Uses PyPDF2 for text extraction
- pdfplumber for table detection
- pytesseract for OCR on scanned PDFs

## Common Issues

- **No text extracted:** PDF might be scanned → use OCR
- **Tables split across pages:** Use table detection script
- **Encoding issues:** Ensure UTF-8 output

## Examples

- “Extract all tables from sales-report.pdf”
- “Summarize this contract and highlight key dates”
- “Convert this invoice PDF to JSON format”

```
### 📝 Exemplo: `skills/security-audit/SKILL.md`

```yaml
---
name: security-audit
description: Comprehensive security review of code. Use before deployments, when reviewing for vulnerabilities, checking authentication, or implementing security features.
allowed-tools: [read, grep, bash]
---

# Security Audit Skill

## Checklist
- [ ] SQL Injection & parameterized queries
- [ ] XSS prevention & input sanitization
- [ ] CSRF protection
- [ ] Authentication & authorization
- [ ] Sensitive data exposure
- [ ] Insecure dependencies
- [ ] API rate limiting
- [ ] Secrets in code
- [ ] CORS misconfiguration

## Instructions
1. Search for common vulnerabilities
2. Check for hardcoded secrets
3. Review authentication logic
4. Validate input handling
5. Generate report with findings and fixes

## Example Output
```markdown
# Security Audit Report
## Critical Issues
- SQL injection in login endpoint

## Medium Issues
- Missing CORS headers

## Recommendations
- Use parameterized queries
- Add helmet.js middleware
```

```
---

## ⚙️ ARQUIVO: .claude/settings.json

### ✅ Objetivo

settings.json é o arquivo de configuração que controla permissões do Claude Code, ferramentas permitidas, hooks, e comportamento do ambiente em nível de usuário ou projeto.

### 📝 Exemplo Básico

```json
{
  "env": {
    "NODE_ENV": "development",
    "DATABASE_URL": "postgresql://localhost/myapp"
  },
  
  "permissions": {
    "allow": [
      "read:src/**",
      "read:tests/**",
      "write:src/**",
      "write:tests/**",
      "bash:npm run test",
      "bash:npm run build"
    ],
    "ask": [
      "write:.env*",
      "bash:npm run deploy",
      "bash:git push"
    ],
    "deny": [
      "read:.env*",
      "read:private/**",
      "bash:rm -rf",
      "bash:sudo",
      "write:package-lock.json"
    ]
  },

  "hooks": {
    "pre-tool": {
      "bash": "scripts/pre-bash-hook.sh"
    },
    "post-test": {
      "command": "npm run coverage-check"
    }
  },

  "modelOverrides": {
    "claude-sonnet-4-6": "anthropic/claude-sonnet-4-6-20250514"
  }
}
```

### 📋 Seções Principais

|Seção           |Objetivo             |Exemplo                    |
|----------------|---------------------|---------------------------|
|`env`           |Variáveis de ambiente|`NODE_ENV`, `API_KEY`      |
|`permissions`   |Controle de acesso   |allow/ask/deny rules       |
|`hooks`         |Event handlers       |pre-commit, post-test      |
|`modelOverrides`|Mapear modelos custom|Fine-tuned models          |
|`fileSuggestion`|Custom file search   |Script para buscar arquivos|

### 🔒 Exemplo: Configuração de Segurança

```json
{
  "permissions": {
    "allow": [
      "read:src/**",
      "write:src/**"
    ],
    "ask": [
      "bash:npm run deploy",
      "write:database/**"
    ],
    "deny": [
      "read:secret/**",
      "read:.env*",
      "bash:sudo",
      "bash:rm -rf /",
      "write:package.json"
    ]
  },
  
  "hooks": {
    "before-bash": "validate-command.sh",
    "before-write": "check-sensitive-files.sh"
  }
}
```

-----

## 📋 ARQUIVO: .claude/.claudeignore

### ✅ Objetivo

Funciona como .gitignore mas para o contexto do Claude. Arquivos que correspondem aos padrões não serão puxados para a janela de contexto durante a descoberta automática de arquivos.

### 📝 Exemplo

```
# Node
node_modules/
dist/
build/
*.log

# Sensitive
.env*
secrets/
private/
.ssh/

# Large files
*.mp4
*.zip
*.tar.gz

# Temporary
.tmp/
cache/
.DS_Store

# Version control
.git/
.github/workflows/test.yml
```

-----

## 🔥 ARQUIVO: .claude/commands/

### ✅ Objetivo

Comandos slash (`/mycommand`) que o usuário pode invocar rapidamente.

### 📝 Exemplo: `commands/test.md`

```markdown
# /test

Run tests for the current file or directory.

## Usage
- `/test` - Run tests for current file
- `/test src/components` - Run tests for directory
- `/test --watch` - Run in watch mode

## What It Does
1. Detects test framework (Jest/Vitest)
2. Runs appropriate test command
3. Shows coverage report
4. Highlights failures

## Example
```

> /test src/Button.test.tsx

PASS  src/Button.test.tsx
Button component
✓ renders with text
✓ calls onClick handler

Test Suites: 1 passed
Tests: 2 passed

```

```

### 📝 Exemplo: `commands/review.md`

```markdown
# /review

Ask Claude to review your code for best practices.

## Usage
- `/review` - Review current file
- `/review src/` - Review entire directory
- `/review --strict` - Strict review (more detailed)

## Checks
- Code quality
- Security issues
- Performance problems
- Test coverage
- Style compliance

## Output
Detailed report with:
- Issues found
- Severity level
- Suggested fixes
- Code examples
```

-----

## 🤖 ARQUIVO: .claude/agents/

### ✅ Objetivo

Agentes especializados para tarefas específicas (não carregam por padrão, apenas quando invocados).

### 📝 Exemplo: `agents/code-reviewer/AGENT.md`

```markdown
# Code Reviewer Agent

## Role
Specialized agent for comprehensive code review.

## Expertise
- Security vulnerabilities
- Performance optimization
- Code style & patterns
- Test coverage
- Documentation

## Process
1. Analyze code structure
2. Check for known vulnerabilities
3. Suggest optimizations
4. Verify test coverage
5. Generate review report

## Standards Applied
- OWASP Top 10
- Node.js best practices
- TypeScript strict mode
- Code coverage > 80%

## Output Format
```markdown
## Security Review
- [ ] Issue 1
- [x] Passed check 2

## Performance
- Suggestion 1
- Suggestion 2

## Code Quality
...
```

```
---

## 📋 ARQUIVO: TASKS.md - Gerenciamento de Tarefas

### ✅ Objetivo

TASKS.md é o arquivo de coordenação central para Claude implementar múltiplas tarefas de forma sequencial. Diferente de TODO lists simples, TASKS.md:
- É lido automaticamente por Claude
- Suporta dependências e bloqueadores
- Persiste entre sessões
- Integra com o Native Task System (Jan 2025+)

### 🎯 Por Que Não `.github/tasks/`?

❌ **Errado:**
```

.github/
├── workflows/      ← CI/CD
└── tasks/          ← ❌ Claude não carrega automático
└── feature.md

```
✅ **Correto:**
```

seu-projeto/
├── TASKS.md        ← ✅ Claude lê automaticamente
└── .github/
└── workflows/  ← Apenas CI/CD aqui

```
### 📐 Formato Recomendado

```markdown
# Implementation Tasks - MyProject

**Status:** In Progress | **Total:** 8 tasks | **Done:** 2 | **Blocked:** 1

## Phase 1: Foundation (CRITICAL)

- [ ] Task 1: Database Schema Setup
  - Priority: 🔴 CRITICAL
  - Effort: 2 hours
  - Subtasks:
    - [ ] Create users table
    - [ ] Create migrations
    - [ ] Add indexes
  - Blocked by: None
  - Blocking: Task 2, Task 3
  - Dependencies: schema.sql (exists)

- [ ] Task 2: Authentication System
  - Priority: 🔴 CRITICAL
  - Effort: 3 hours
  - Subtasks:
    - [ ] Setup JWT
    - [ ] Create login endpoint
    - [ ] Hash password validation
  - Blocked by: Task 1
  - Blocking: Task 4
  - Tests: Must achieve 90%+ coverage

## Phase 2: Core Features (HIGH)

- [ ] Task 3: User Profile API
  - Priority: 🟡 HIGH
  - Effort: 1.5 hours
  - Subtasks:
    - [ ] GET /users/:id
    - [ ] PATCH /users/:id
    - [ ] DELETE /users/:id
  - Blocked by: Task 1
  - Blocking: Task 5
  - Tests: Unit + Integration tests

- [ ] Task 4: Dashboard Backend
  - Priority: 🟡 HIGH
  - Effort: 2.5 hours
  - Subtasks:
    - [ ] Create dashboard routes
    - [ ] Analytics aggregation
    - [ ] Caching strategy
  - Blocked by: Task 2
  - Blocking: None
  - Dependencies: Redis (configure)

## Phase 3: Polish (MEDIUM)

- [ ] Task 5: Error Handling
  - Priority: 🟢 MEDIUM
  - Effort: 1 hour
  - Subtasks:
    - [ ] Error middleware
    - [ ] Error logging
    - [ ] Error responses
  - Blocked by: Task 3
  - Blocking: None

- [ ] Task 6: Documentation
  - Priority: 🟢 MEDIUM
  - Effort: 1.5 hours
  - Subtasks:
    - [ ] API docs (Swagger)
    - [ ] Setup guide
    - [ ] Contributing guide
  - Blocked by: None
  - Blocking: None

## Completed ✅

- [x] Task 0: Project Setup (1h) - DONE
  - Completed: npm, eslint, prettier, tsconfig
  
- [x] Task 1.5: Environment Variables (30m) - DONE
  - Completed: .env.example, docs

## Blocked/At Risk ⚠️

None at moment

## Notes
- Use `/next-task` command to implement next available task
- Use `/batch-implement` to implement all tasks sequentially
- Check `/task-status` for current progress
- Run `npm test` after each task
```

### 📝 Variações de Formato

#### Minimalista (Pequenos Projetos)

```markdown
# Tasks

## Ready to Implement
- [ ] Auth system
- [ ] User profile
- [ ] Dashboard

## In Progress
- [ ] Database setup

## Done
- [x] Project setup
```

#### Com Prioridades

```markdown
# Priority Tasks

### 🔴 CRITICAL (Implement First)
- [ ] Database migrations

### 🟡 HIGH (This Week)
- [ ] Authentication

### 🟢 MEDIUM (Next Week)
- [ ] Documentation
```

#### Com Dependências Explícitas

```markdown
# Task Dependencies Map

Task 1: Database (no deps)
├── Task 2: Auth (needs Task 1)
│   ├── Task 3: Profile (needs Task 2)
│   └── Task 4: Dashboard (needs Task 2)
└── Task 5: API Docs (needs everything)
```

-----

## 🔥 COMANDO: next-task (Automático)

### Criar: `.claude/commands/next-task.md`

```markdown
# /next-task

Implement the next available task from TASKS.md automatically.

## Process
1. Read TASKS.md from project root
2. Find first [ ] (uncompleted) task
3. Check "Blocked by:" field
4. If blocked: Report which tasks must be done first
5. If ready:
   - Create feature branch: feature/task-[number]
   - Implement all subtasks
   - Run tests: npm test
   - Commit with message: "Task [number]: [name]"
   - Mark as [x] in TASKS.md
   - Commit TASKS.md
   - Show what's next

## Example Output
```bash
> /next-task

📋 Reading TASKS.md...
Found: [ ] Task 1: Database Schema Setup
✅ Not blocked, starting now!

🌿 Creating branch: feature/task-1-database
⚙️ Implementing subtasks...
  [✓] Create users table
  [✓] Create migrations
  [✓] Add indexes
  
✅ All subtasks complete!
🧪 Running tests... PASS (95% coverage)
📝 Committing: "Task 1: Database Schema Setup"

✅ COMPLETE! Marked [x] in TASKS.md

📊 Progress:
- Completed: 1/8
- Blocked tasks available: Task 2
- Next: Task 2 (Authentication)
```

## Notes

- Never skip blockers - report them instead
- Always run tests before committing
- Update TASKS.md immediately after completion

```
---

## 🔄 COMANDO: batch-implement (Múltiplas Tasks)

### Criar: `.claude/commands/batch-implement.md`

```markdown
# /batch-implement

Implement ALL pending tasks sequentially from TASKS.md.

## Workflow
1. Read TASKS.md
2. Group tasks by phase/priority
3. For each task in order:
   a. Check blockers
   b. If blocked: Skip and report
   c. If ready: Implement (see /next-task)
   d. Mark as done
   e. Move to next
4. Continue until all done or blocker found
5. Generate completion report

## Execution Rules
- Stop on first blocker (don't skip)
- Test after each task
- Commit after each task
- Update TASKS.md after each task
- Show progress every 2 tasks

## Example Report
```

# 🚀 Batch Implementation Report

Session: 2026-06-11 14:30

✅ COMPLETED (2)
Task 1: Database Schema Setup (2h)
Task 2: Authentication System (3h)

⏳ BLOCKED (1)
Task 3: User Profile API (needs Task 1)
→ Task 1 is already done, but re-check…
→ Actually NOT blocked, starting…

✅ COMPLETED (3)
Task 3: User Profile API (1.5h)
Task 4: Dashboard Backend (2.5h)

⏸️ BLOCKED (1)
Task 5: Error Handling (blocked by Task 3… done)
→ Actually NOT blocked, continuing…

✅ COMPLETED (4)
Task 5: Error Handling (1h)

⏸️ BLOCKED (1)
Task 6: Documentation (no blockers!)
→ Starting…

✅ COMPLETED (5)
Task 6: Documentation (1.5h)

📊 Summary
Total time: 11.5 hours
Tasks done: 6/6 (100%)
All tasks complete! 🎉

```

```

-----

## 🧠 Integração com CLAUDE.md

No seu CLAUDE.md principal, adicione seção sobre tasks:

```markdown
## Task Management

### Current Implementation Status
- Strategy: Sequential task implementation via TASKS.md
- Status: Use `/next-task` to implement one task
- Batch: Use `/batch-implement` to implement all
- Tracking: Always update TASKS.md after each task

### Rules
- **NEVER** skip blockers - report them instead
- **ALWAYS** run tests after task
- **ALWAYS** mark task as [x] when done
- **ALWAYS** commit with message: "Task [N]: [name]"
- **ALWAYS** update TASKS.md in same commit

### Available Commands
- `/next-task` - Implement next pending task
- `/batch-implement` - Implement all pending tasks
- `/task-status` - Show current progress
- `/task-report` - Generate completion report

### Example Workflow
```bash
claude
> /next-task      # Implement Task 1
> /next-task      # Implement Task 2
> /batch-implement  # Implement Tasks 3-6
> show tasks
✅ All done!
```

### Notes

- Read TASKS.md from project root
- Each task has subtasks and blockers
- Follow priority (CRITICAL → HIGH → MEDIUM)
- Test coverage must stay above 80%

```
---

## 📊 Fluxo Completo: Exemplo Real

### 1️⃣ Setup (Dia 1)

```bash
# Criar TASKS.md na raiz
cat > TASKS.md << 'EOF'
# Implementation Tasks

## Phase 1
- [ ] Task 1: Database
- [ ] Task 2: Auth

## Phase 2
- [ ] Task 3: Profile

## Done
- [x] Project setup
EOF

# Criar comando
mkdir -p .claude/commands
cat > .claude/commands/next-task.md << 'EOF'
# /next-task
[conteúdo do comando acima]
EOF

# Commit
git add TASKS.md .claude/commands/next-task.md
git commit -m "chore: setup task management"
```

### 2️⃣ Desenvolvimento (Dia 2+)

```bash
# Iniciar Claude
claude

# Implementar próxima task
> /next-task
[Claude implementa Task 1]
[Marca [x] em TASKS.md]
[Commit automático]

# Ver próxima
> what's next?
Task 2 is now available (Task 1 done)

# Continuar
> /next-task
[Claude implementa Task 2]

# Ou fazer várias seguidas
> /batch-implement
[Claude implementa Tasks 3, 4, 5...]
```

### 3️⃣ Monitoramento

```bash
# Ver status
> show tasks

# Gerar relatório
> /task-report

# Ver bloqueadores
> which tasks are blocked?
```

-----

## ✅ Checklist: Implementação de Tasks

### Fase 1: Setup (Hoje)

- [ ] Criar TASKS.md na raiz do projeto
- [ ] Listar todas as tarefas com prioridades
- [ ] Definir bloqueadores e dependências
- [ ] Adicionar seção “Task Management” no CLAUDE.md

### Fase 2: Comandos (Hoje)

- [ ] Criar `.claude/commands/next-task.md`
- [ ] Criar `.claude/commands/batch-implement.md` (opcional)
- [ ] Testar: `> /next-task`
- [ ] Verificar que Claude lê TASKS.md

### Fase 3: Processo (Contínuo)

- [ ] Executar `/next-task` para cada tarefa
- [ ] Manter TASKS.md atualizado
- [ ] Revisar bloqueadores
- [ ] Ajustar cronograma conforme necessário

-----

## 📋 Comparação: Estratégias de Task Management

|Estratégia        |Vantagem                  |Desvantagem     |Quando Usar       |
|------------------|--------------------------|----------------|------------------|
|**TASKS.md**      |✅ Simples ✅ Claude lê auto|Manual marking  |Padrão recomendado|
|**.github/issues**|✅ Integrado               |❌ Claude não vê |GitHub Projects   |
|**Native /tasks** |✅ Persistência            |Requer Jan 2025+|Grandes projetos  |
|**Linear/Asana**  |✅ Team collab             |❌ Desincroniza  |Equipes grandes   |
|**Em código TODO**|❌ Perde visão             |❌ Disperso      |NÃO RECOMENDADO   |

-----

## 📝 CARREGAMENTO: Ordem de Prioridade

A ordem de carregamento quando você inicia uma sessão Claude Code é:

- Sempre carregado: CLAUDE.md raiz, qualquer CLAUDE.md de diretório pai, ~/.claude/CLAUDE.md (global)
- Carregado ao acessar: CLAUDE.md aninhado em subdiretórios (quando Claude navega lá)
- Carregado sob demanda: Skills (apenas nome e descrição carregam inicialmente - conteúdo completo carrega quando Claude decide que a skill é relevante)

### 🔄 Hierarquia

```
1. ~/.claude/CLAUDE.md (global - mais geral)
2. ./.claude/CLAUDE.md (projeto)
3. ./.claude/rules/* (por domínio)
4. src/CLAUDE.md (subpasta específica - se existir)
5. Skills (sob demanda)
```

-----

## ✅ CHECKLIST: Implementação Passo a Passo

### Fase 1: Essencial (Dia 1)

- [ ] Criar CLAUDE.md na raiz (< 60 linhas)
- [ ] Criar .claude/settings.json com permissões básicas
- [ ] Criar .claude/.claudeignore
- [ ] Criar TASKS.md com tarefas do projeto
- [ ] Adicionar seção “Task Management” no CLAUDE.md

### Fase 2: Intermediário (Semana 1)

- [ ] Criar .claude/rules/code-style.md
- [ ] Criar .claude/rules/testing.md
- [ ] Criar .claude/rules/security.md
- [ ] Criar `.claude/commands/next-task.md`
- [ ] Testar: `> /next-task`

### Fase 3: Avançado (Semana 2+)

- [ ] Criar `.claude/commands/batch-implement.md`
- [ ] Criar skills para tarefas recorrentes
- [ ] Definir custom commands avançados
- [ ] Adicionar agents especializados
- [ ] Configurar hooks
- [ ] Criar `.claude/commands/task-report.md` (opcional)

-----

## 🎯 EXEMPLO PRÁTICO COMPLETO

### Seu Projeto

```
meu-app/
├── CLAUDE.md                   # Instruções principais
├── TASKS.md                    # ⭐ Gerenciamento de tarefas
├── src/
│   ├── components/
│   ├── services/
│   └── utils/
├── tests/
├── .claude/
│   ├── settings.json
│   ├── .claudeignore
│   ├── rules/
│   │   ├── code-style.md
│   │   ├── testing.md
│   │   └── security.md
│   ├── skills/
│   │   └── pdf-processor/
│   │       ├── SKILL.md
│   │       └── scripts/
│   └── commands/
│       ├── next-task.md        # ⭐ Implementa próxima task
│       ├── batch-implement.md  # ⭐ Implementa todas as tasks
│       └── test.md
└── .github/
    └── workflows/              # Apenas CI/CD aqui
```

### Fluxo Quando Claude Trabalha

1. ⚡ Claude Code inicia → **carrega CLAUDE.md raiz**
1. 📋 Claude lê TASKS.md → **identifica tarefas disponíveis**
1. 🎯 Verifica **bloqueadores e dependências**
1. 🚀 User executa `/next-task` → **Claude implementa uma tarefa**
1. ✅ Task concluída → **marca [x] em TASKS.md e faz commit**
1. 🔄 Repete até tudo completo

**Fluxo de Desenvolvimento:**

```
claude
> /next-task        (Implementa Task 1)
> /next-task        (Implementa Task 2)
> /batch-implement  (Implementa Tasks 3-6)
> show tasks
✅ Todas as tarefas completas!
```

-----

## 📚 Boas Práticas Finais

### Estrutura e Organização

|✅ Fazer                                |❌ Evitar                  |
|---------------------------------------|--------------------------|
|Manter CLAUDE.md < 60 linhas           |Colocar tudo em um arquivo|
|Usar .claude/rules/ para domínios      |Arquivo monolítico        |
|Incluir exemplos concretos             |Descrições abstratas      |
|Regras executáveis (bash commands)     |Apenas instruções em prosa|
|Atualizar periodicamente               |Deixar desatualizado      |
|Usar IMPORTANT para 1-2 regras críticas|Marcar tudo como IMPORTANT|

### Task Management

|✅ Fazer                          |❌ Evitar                 |
|---------------------------------|-------------------------|
|Usar TASKS.md (raiz do projeto)  |Colocar em .github/tasks/|
|Definir bloqueadores explícitos  |Tasks desorganizadas     |
|Atualizar TASKS.md após cada task|Deixar desincronizado    |
|Usar `/next-task` sequencialmente|Pedir tarefas ad-hoc     |
|Testes após cada tarefa          |Testar ao final          |
|Commits atômicos por tarefa      |Mega commits             |

### Padrões Recomendados

|Padrão             |Quando Usar          |Benefício             |
|-------------------|---------------------|----------------------|
|**Sequential**     |Tarefas lineares     |Simples, previsível   |
|**Operator**       |Tarefas complexas    |Flexível, adaptável   |
|**Split-and-merge**|Tarefas independentes|Paralelo, rápido      |
|**Agent Teams**    |Grandes projetos     |Especialização, escala|
|**Headless**       |Automação pura       |Sem intervenção       |

-----

## 🔗 Referências Oficiais

- [Claude Code Documentation](https://code.claude.com/docs)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Task Management Guide](https://claudefa.st/blog/guide/development/task-management)
- [Claude Code Workflow Patterns](https://www.mindstudio.ai/blog/claude-code-agentic-workflow-patterns)
- [Agent Teams Documentation](https://code.claude.com/docs/en/agents)

-----

## 🎓 Workflow Patterns Suportados

Claude Code suporta 5 padrões de workflow para diferentes necessidades:

### 1. Sequential (Recomendado para Tasks)

- Passos fixos em ordem
- Um completa antes do próximo
- **Uso:** Implementar tasks de TASKS.md
- **Exemplo:** /next-task, /batch-implement

### 2. Operator Pattern

- Agent orquestrador + subagents especializados
- Delegação dinâmica
- **Uso:** Tarefas complexas que precisam ser decompostas

### 3. Split-and-Merge

- Tarefas paralelas independentes
- Consolidação final
- **Uso:** Processar múltiplos arquivos simultaneamente

### 4. Agent Teams

- Multi-sessão coordenada
- Comunicação em tempo real
- **Uso:** Grandes projetos com equipes virtuais

### 5. Headless (Autônomo)

- Sem intervenção humana
- Automação pura
- **Uso:** Pipelines de CI/CD, webhooks

**Para começar:** Use Sequential com TASKS.md e /next-task

-----

**Última atualização:** Junho 2026  
**Baseado em:** Documentação Oficial Anthropic + Community Best Practices + Native Task System (Jan 2025+)
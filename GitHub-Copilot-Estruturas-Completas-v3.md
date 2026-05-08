# 📗 GitHub Copilot - Estruturas Completas dos 5 Componentes

**Versão:** 3.0  
**Data:** Maio 2026  
**Foco:** Estruturas exatas, Tags Markdown, Schemas YAML, Temperatura, Exemplos Completos

---

## 📑 Índice

1. [Overview: 5 Componentes](#overview-5-componentes)
2. [INSTRUCTIONS - Estrutura Completa](#instructions---estrutura-completa)
3. [AGENTS - Estrutura Completa](#agents---estrutura-completa)
4. [SKILLS - Estrutura Completa](#skills---estrutura-completa)
5. [PROMPTS - Estrutura Completa](#prompts---estrutura-completa)
6. [HOOKS - Estrutura Completa](#hooks---estrutura-completa)
7. [Tags Markdown Suportadas](#tags-markdown-suportadas)
8. [Temperatura em Agents (Pesquisa e Evidências)](#temperatura-em-agents-pesquisa-e-evidências)
9. [Matriz Comparativa Completa](#matriz-comparativa-completa)
10. [Exemplos Práticos Enriquecidos](#exemplos-práticos-enriquecidos)

---

## 🎯 Overview: 5 Componentes

```
┌──────────────────────────────────────────────────────────┐
│         GITHUB COPILOT - 5 CAMADAS DE CUSTOMIZAÇÃO      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1️⃣  INSTRUCTIONS (.github/copilot-instructions.md)      │
│      └─ Padrões globais (SEMPRE carregado)              │
│      └─ ~40-80 tokens per requisição                    │
│                                                          │
│  2️⃣  AGENTS (.github/agents/nome.agent.md)               │
│      └─ Personas especializadas (@developer, @pm)       │
│      └─ ~50 tokens quando selecionado                   │
│      └─ SUPORTA temperatura, model seleção              │
│                                                          │
│  3️⃣  SKILLS (.github/skills/nome/SKILL.md)               │
│      └─ Tarefas reutilizáveis (/testing, /debug)       │
│      └─ ~5-10 tokens discovery + ~250 se match          │
│      └─ Progressive loading (3 níveis)                  │
│                                                          │
│  4️⃣  PROMPTS (.github/prompts/nome.prompt.md)            │
│      └─ Atalhos para tarefas repetitivas (/create)      │
│      └─ 0 tokens se não invocar, ~150-200 se usar       │
│      └─ SUPORTA temperatura, model seleção              │
│                                                          │
│  5️⃣  HOOKS (.github/hooks/seu-hook.json)                 │
│      └─ Policy enforcement (eventos)                     │
│      └─ 0 tokens (executa em background)                │
│      └─ ⚠️ APENAS project-level (.github/)               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 📝 INSTRUCTIONS - Estrutura Completa

### Arquivo: `.github/copilot-instructions.md` ou `~/.copilot/copilot-instructions.md`

**Formato:** Markdown puro (SEM frontmatter YAML)

### Estrutura Completa Anotada

```markdown
# Project Name - Global Standards

**Descrição:** Este arquivo contém TODAS as convenções que SEMPRE devem ser seguidas.

## 📋 Seções Recomendadas (Ordem é importante)

### 1. Tech Stack Overview
Defina com precisão o que seu projeto usa.

- **Frontend:** React 18.2+, TypeScript 5.2+, Tailwind CSS 3.4+
- **Backend:** Node.js 20 LTS, Express 4.18+, PostgreSQL 15+
- **Testing:** Jest 29+, React Testing Library 14+
- **Package Manager:** npm 10+
- **Build Tool:** Webpack 5 / Vite 5
- **CI/CD:** GitHub Actions

### 2. Naming Conventions (MANDATORY)

#### Variables & Functions
```
✅ Correct:   const userEmail = "..."
❌ Incorrect: const user_email = "..."
❌ Incorrect: const UserEmail = "..."
```
- camelCase for variables, functions, methods
- Use descriptive names (no single letters except i, j, k in loops)

#### Classes, Types, Interfaces
```
✅ Correct:   class UserManager {}
✅ Correct:   interface UserProfile {}
❌ Incorrect: class user_manager {}
```
- PascalCase ALWAYS
- Prefixes: no redundancy (UserManager, not UserUserManager)

#### Constants & Environment
```
✅ Correct:   const API_TIMEOUT = 5000
✅ Correct:   const MAX_RETRIES = 3
❌ Incorrect: const apiTimeout = 5000
```
- UPPER_SNAKE_CASE for constants

#### Files & Folders
```
✅ Correct:   src/utils/date-formatter.ts
✅ Correct:   src/hooks/use-auth.ts
❌ Incorrect: src/utils/dateFormatter.ts
```
- kebab-case for files and folders

### 3. Project Structure (Canonical)

```
src/
├── components/         # React components (reusable UI)
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   └── Card/
│       └── ...
│
├── hooks/              # Custom React hooks
│   ├── useAuth.ts
│   ├── useFetch.ts
│   └── index.ts
│
├── services/           # API calls, external integrations
│   ├── api.ts          # Axios/Fetch client setup
│   ├── userService.ts
│   └── index.ts
│
├── utils/              # Pure functions, helpers
│   ├── formatDate.ts
│   ├── validators.ts
│   └── index.ts
│
├── types/              # TypeScript type definitions
│   ├── user.ts
│   ├── api.ts
│   └── index.ts
│
├── styles/             # Global styles
│   ├── tailwind.config.js
│   └── globals.css
│
├── tests/              # Integration, E2E tests
│   └── setup.ts
│
└── App.tsx             # Root component
```

### 4. Error Handling Pattern (MANDATORY)

```typescript
// ✅ CORRECT PATTERN
try {
  const data = await fetchUser(id);
  return data;
} catch (error) {
  // 1. Log with context
  logger.error('Failed to fetch user', {
    userId: id,
    error: error instanceof Error ? error.message : 'Unknown error',
    timestamp: new Date().toISOString()
  });
  
  // 2. Transform for user
  throw new AppError(
    'Unable to load user profile. Please try again.',
    'USER_FETCH_ERROR',
    { originalError: error, userId: id }
  );
}

// ❌ NEVER DO THIS
catch (e) {
  console.log('Error'); // Too vague
  throw e; // Don't transform
}
```

### 5. TypeScript Requirements (MANDATORY)

```typescript
// ✅ CORRECT: Full typing
interface UserProps {
  id: string;
  name: string;
  email: string;
  age?: number;
}

const UserCard: React.FC<UserProps> = ({ id, name, email }) => {
  return <div>{name}</div>;
};

// ❌ INCORRECT: Any typing
const UserCard = ({ id, name, email }: any) => {
  return <div>{name}</div>;
};

// ❌ INCORRECT: Missing types
const UserCard = ({ id, name, email }) => {
  return <div>{name}</div>;
};
```

### 6. Testing Standards (MANDATORY)

- **Coverage minimum:** 80% for all new code
- **Framework:** Jest + React Testing Library
- **Test location:** `src/components/Button/__tests__/Button.test.tsx`
- **Test naming:** `describe('Component', () => { it('should...') })`
- **Async testing:** Always use `async/await` with testing-library queries

```typescript
// ✅ CORRECT
test('should display loading state while fetching', async () => {
  render(<UserList />);
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});

// ❌ INCORRECT
test('should load users', () => {
  render(<UserList />);
  // No async, no waitFor
});
```

### 7. Git Commit Standards

```
Format: <type>(<scope>): <subject>

Types:
  feat:    New feature
  fix:     Bug fix
  refactor: Code refactor (no behavior change)
  test:    Test addition/fix
  docs:    Documentation
  chore:   Build, CI, dependencies

Examples:
  ✅ feat(auth): add two-factor authentication
  ✅ fix(api): handle null user response
  ❌ fixed stuff
  ❌ update
```

### 8. Build & Run Commands (MANDATORY)

```bash
# Development
npm start                 # Start dev server (http://localhost:3000)
npm run dev              # Same as npm start

# Testing
npm test                 # Run all tests in watch mode
npm run test:coverage    # Generate coverage report (must be >80%)

# Building
npm run build            # Production build (optimized)
npm run build:analyze    # Show bundle size analysis

# Linting & Formatting
npm run lint             # ESLint check
npm run lint:fix         # ESLint auto-fix
npm run format           # Prettier format
npm run format:check     # Check if formatted

# Type Checking
npm run type-check       # TypeScript type check
```

### 9. Security Checklist (MANDATORY)

- ❌ NEVER hardcode API keys, secrets, or tokens
- ❌ NEVER commit `.env` files (use `.env.template`)
- ❌ NEVER store passwords in localStorage (use HTTP-only cookies)
- ❌ NEVER trust user input (validate + sanitize always)
- ✅ ALWAYS use HTTPS in production
- ✅ ALWAYS validate environment variables at startup
- ✅ ALWAYS use Content Security Policy headers
- ✅ ALWAYS escape HTML output

### 10. Do NOT

```
❌ Use `var` keyword anywhere
❌ Commit without running: npm test && npm run lint
❌ Create .test.tsx files for non-component files (put in __tests__)
❌ Use `any` type in TypeScript
❌ Leave console.log() in production code
❌ Ignore linter warnings
❌ Modify package-lock.json manually
❌ Use index as React key in lists
```

### 11. References & Documentation

- [Architecture Decision Records](../../docs/ADR.md)
- [API Documentation](../../docs/API.md)
- [Setup Guide](../../docs/SETUP.md)
- [Contributing Guide](../../CONTRIBUTING.md)
```

**Token Cost:** ~50-80 tokens (SEMPRE carregado em CADA requisição)

**Palavras-chave para descoberta:** Não usa descoberta - é ALWAYS-ON.

---

## 🎭 AGENTS - Estrutura Completa

### Arquivo: `.github/agents/developer.agent.md` ou `~/.copilot/agents/developer.agent.md`

### Estrutura Completa com Todas as Tags YAML

```markdown
---
# ========== REQUIRED FIELDS ==========
name: 'developer'
description: >
  Especializado em implementação de features, correção de bugs,
  refatoração e manutenção de código.
  Use quando precisa escrever código, corrigir bugs, refatorar,
  ou melhorar qualidade do código existente.
  Keywords: code, implement, feature, bug fix, development.

# ========== OPTIONAL FIELDS ==========
# Model selection (se suportado na sua versão)
# model: 'claude-opus-4-6'
# model: ['claude-opus-4-6', 'gpt-5.2']  # Priority order

# Tools available to this agent
tools:
  - read          # Read files
  - search        # Search workspace
  - edit          # Edit files
  - shell         # Run terminal commands

# Handoffs (Workflow transitions)
# Quando este agent termina, oferecer botões para mudar para outro
handoffs:
  - label: 'Request Code Review'
    agent: 'code-reviewer'
    prompt: 'Please review the implementation above for quality and security.'
    send: false    # false = usuário aprova antes de enviar
  
  - label: 'Create Tests'
    agent: 'test-specialist'
    prompt: 'Create comprehensive tests for the implementation above.'
    send: false

# Target environment (VS Code, GitHub, etc.)
# target: 'vscode'

# Metadata custom (opcional)
# metadata:
#   author: 'platform-team'
#   version: '1.0'
#   category: 'development'
---

# Developer Agent

Você é um **desenvolvedor sênior** especializado em implementação e manutenção de código.

## Identity & Role

- **Expertise:** Full-stack TypeScript/JavaScript development
- **Focus:** Feature implementation, bug fixes, refactoring, code quality
- **Personality:** Pragmatic, detail-oriented, focused on best practices
- **Scope:** Local codebase manipulation, NO deployment decisions

## Core Responsibilities

1. **Feature Implementation**
   - Break down requirements into subtasks
   - Implement with TDD (test-first) approach
   - Follow project conventions exactly
   - Create self-documenting code with JSDoc

2. **Bug Fixes**
   - Root cause analysis first
   - Fix with minimal side effects
   - Add regression tests
   - Document why the bug occurred

3. **Refactoring**
   - Improve readability without changing behavior
   - Reduce complexity, extract functions
   - Improve performance where safe
   - Always add/update tests

4. **Code Review**
   - Use the #tool:search tool to find related code
   - Cross-reference with coding standards
   - Suggest improvements with reasoning

## Tools & Capabilities

You have access to these tools:
- **#tool:read** — Read any file in the workspace
- **#tool:search** — Search files by name, content, pattern
- **#tool:edit** — Modify files (not deletion)
- **#tool:shell** — Run npm, git, linting commands

## Standards to Follow

Reference the global standards in [copilot-instructions.md](../../.github/copilot-instructions.md) for:
- Naming conventions (camelCase, PascalCase)
- Project structure rules
- TypeScript requirements
- Error handling patterns
- Testing standards (80% minimum coverage)
- Git commit format

## Workflow Steps

### When implementing a feature:

1. **Understand Requirements**
   - Ask clarifying questions if unclear
   - Reference requirements in code comments
   - Identify affected files using #tool:search

2. **Plan Implementation**
   - Break into discrete, testable units
   - Identify dependencies and side effects
   - Propose file structure changes if needed

3. **Implement with Tests**
   - Write tests first (TDD approach)
   - Run `npm test` to verify locally
   - Implement feature code
   - Ensure coverage > 80%

4. **Follow Conventions**
   - Use kebab-case for file names
   - camelCase for variables, functions
   - PascalCase for components, classes
   - Use TypeScript interfaces (never `any`)

5. **Self-Review Checklist**
   - [ ] Code follows naming conventions
   - [ ] All tests pass (`npm test`)
   - [ ] Coverage > 80% (`npm run test:coverage`)
   - [ ] Linter passes (`npm run lint`)
   - [ ] Code is formatted (`npm run format`)
   - [ ] No hardcoded secrets or API keys
   - [ ] Error handling with proper logging
   - [ ] JSDoc comments for public functions

## Examples of Your Work Style

### Example 1: Implementing a feature

**User:** "Add a login form component"

**Your Response:**
```
1. First, I'll search for existing auth components
   using #tool:search

2. Create src/components/LoginForm/LoginForm.tsx
   with proper TypeScript interfaces

3. Create src/components/LoginForm/__tests__/LoginForm.test.tsx
   with 80%+ coverage

4. Update src/components/index.ts to export LoginForm

5. Verify: npm test passes, npm run lint passes
```

### Example 2: Fixing a bug

**User:** "Users report that forgotten passwords reset emails not sending"

**Your Response:**
```
1. Search #tool:search for "password" + "email" to understand flow
2. Check error logs and identify failure point
3. Fix root cause with minimal changes
4. Add test case to prevent regression
5. Commit with clear message explaining why bug occurred
```

## Constraints & Boundaries

### ✅ DO
- Implement changes with full test coverage
- Ask questions to clarify unclear requirements
- Suggest better approaches with reasoning
- Update documentation alongside code
- Run full test suite before finishing

### ❌ DO NOT
- Commit code without tests passing
- Modify migrations or database schemas
- Deploy or make deployment decisions
- Change project dependencies without justification
- Leave console.log() or debugging code
- Ignore ESLint or TypeScript errors

## Integration with Other Agents

When you need help:
- **Code Review?** Use the handoff to "code-reviewer" agent
- **Create Tests?** Use the handoff to "test-specialist" agent
- **Architecture Help?** Use the handoff to "architect" agent

## References

- [Architecture Decision Records](../../docs/ADR.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [API Documentation](../../docs/API.md)
- [Project README](../../README.md)
```

**YAML Fields (COMPLETE SCHEMA):**

| Campo | Type | Required | Descrição |
|-------|------|----------|-----------|
| `name` | string | ✅ | kebab-case identifier (lowercase, hyphens) |
| `description` | string | ✅ | 2-4 linhas, keywords para discovery |
| `model` | string\|array | ❌ | Modelo a usar (ex: claude-opus-4-6) |
| `tools` | array | ❌ | Lista de tools disponíveis |
| `handoffs` | array | ❌ | Transições para outros agents |
| `target` | string | ❌ | 'vscode' ou 'github-copilot' |
| `metadata` | object | ❌ | Custom fields (author, version, etc) |

**Token Cost:** ~50 tokens (carregado 1x quando selecionado)

---

## 🛠️ SKILLS - Estrutura Completa

### Estrutura de Pasta

```
.github/skills/testing/                    ← Nome em kebab-case
├── SKILL.md                                ← OBRIGATÓRIO
├── LICENSE.txt                             ← Opcional
├── scripts/                                ← Automação
│   ├── run-tests.sh
│   └── check-coverage.js
├── references/                             ← Documentação
│   ├── jest-setup.md
│   └── testing-patterns.md
├── examples/                               ← Exemplos reais
│   ├── simple-function.test.ts
│   └── component.test.tsx
└── templates/                              ← Scaffolds
    └── test-template.ts
```

### Arquivo: `SKILL.md` - Estrutura Completa

```markdown
---
# ========== REQUIRED FIELDS ==========
name: 'testing'
description: >
  Gera testes unitários com jest e react-testing-library.
  Use quando precisa criar testes, melhorar cobertura,
  ou gerar testes para funções e componentes existentes.
  Keywords: unit test, jest, test coverage, testing, test suite,
  test generation, write tests, spec.

# ========== OPTIONAL FIELDS ==========
license: 'MIT'

# Pre-approve tools (skip confirmation dialog)
allowed-tools:
  - shell
  - bash

# Run in isolated subagent context (prevents context pollution)
context: 'fork'

# Can be invoked with /testing slash command?
user-invocable: true

# Should model be invoked for this skill?
disable-model-invocation: false

# Metadata custom
# metadata:
#   author: 'qa-team'
#   version: '2.0'
#   compatibility: 'Jest 29+, React Testing Library 14+'
---

# Unit Testing Skill

Gera testes unitários bem estruturados com boa cobertura.

## Before Starting

Certifique-se de que você tem:
- [ ] Jest instalado e funciona (`npm test` roda sem erros)
- [ ] A função/componente que precisa testar está clara
- [ ] Você conhece os casos de teste esperados
- [ ] Você tem acesso ao arquivo de produção

## Output Structure

Esta skill produz:

1. **Test File** — arquivo `.test.ts` ou `.test.tsx`
   - Localização: `src/components/Button/__tests__/Button.test.tsx`
   - Formato: Jest + React Testing Library (para componentes)
   - Inclui: setup, happy path, edge cases, error cases

2. **Coverage Report** — resumo de cobertura
   - Statements, Branches, Functions, Lines
   - Meta mínima: 80%

3. **Summary** — quantos testes criados, cobertura final

## Step 1: Analyze Function/Component

Examine o que precisa de testes:

### Para Funções
```typescript
// Exemplo de análise
export function sum(a: number, b: number): number {
  return a + b;
}

// Análise:
// - Input: 2 números
// - Output: número (sum)
// - Edge cases: zero, negativas, decimais
// - Errors: nenhum (função pura)
```

### Para Componentes
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ label, onClick, disabled }) => {
  return <button onClick={onClick} disabled={disabled}>{label}</button>;
};

// Análise:
// - Props: label, onClick, disabled
// - Renders: button com label
// - Interactions: click, disabled state
// - Accessibility: alt text, ARIA roles
```

Identifique:
- **Inputs:** parâmetros, props, estado inicial
- **Outputs:** retorno, renderização, estado final
- **Side effects:** mutações, network calls, DOM changes
- **Errors:** exceções, edge cases

Use #tool:read para examinar o arquivo real.

## Step 2: Identify Test Cases (Matriz de Testes)

Crie uma matriz de testes cobrindo:

### Happy Path (Caso Normal)
```
Input: sum(2, 3)
Expected: 5
Assertion: expect(sum(2, 3)).toBe(5)
```

### Edge Cases (Limites)
```
Input: sum(0, 5)       →  5 (zero na primeira)
Input: sum(5, 0)       →  5 (zero na segunda)
Input: sum(-2, 3)      →  1 (número negativo)
Input: sum(-2, -3)     → -5 (ambos negativos)
Input: sum(0.5, 0.3)   →  0.8 (decimais)
```

### Error Cases (Exceções)
```
Input: sum(undefined, 5)
Expected: TypeError ou default behavior
Assertion: expect(() => sum(undefined, 5)).toThrow()
```

### Conditional Branches (Paths)
```
Se a função tem if/else:
  if (a > 10) { ... }
  else { ... }

Teste AMBOS os branches
```

## Step 3: Generate Test Code

Use como referência: [test-template.ts](./templates/test-template.ts)

### Para Funções Síncronas

```typescript
describe('sum', () => {
  // Happy path
  it('should add two positive numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });

  // Edge cases
  it('should handle zero', () => {
    expect(sum(0, 5)).toBe(5);
    expect(sum(5, 0)).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(sum(-2, 3)).toBe(1);
    expect(sum(-2, -3)).toBe(-5);
  });

  it('should handle decimals', () => {
    expect(sum(0.5, 0.3)).toBeCloseTo(0.8);
  });
});
```

### Para Funções Assincronas

```typescript
describe('fetchUser', () => {
  it('should return user when found', async () => {
    const user = await fetchUser('123');
    expect(user.id).toBe('123');
    expect(user.name).toBeDefined();
  });

  it('should throw error when not found', async () => {
    await expect(fetchUser('invalid')).rejects.toThrow('User not found');
  });

  it('should handle network errors', async () => {
    // Mock network failure
    jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('Network error'));
    
    await expect(fetchUser('123')).rejects.toThrow();
  });
});
```

### Para Componentes React

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('should render with label', () => {
    render(<Button label="Click me" onClick={jest.fn()} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const onClick = jest.fn();
    render(<Button label="Click" onClick={onClick} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button label="Click" onClick={jest.fn()} disabled={true} />);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('should not call onClick when disabled', () => {
    const onClick = jest.fn();
    render(<Button label="Click" onClick={onClick} disabled={true} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).not.toHaveBeenCalled();
  });
});
```

## Step 4: Run & Verify

Execute localmente:

```bash
# Run all tests
npm test

# Run with coverage report
npm test -- --coverage

# Run specific test file
npm test -- Button.test.tsx

# Watch mode (re-run on file change)
npm test -- --watch
```

Verifique:
- ✅ Todos os testes passam (saída verde)
- ✅ Cobertura > 80% (statements, branches, functions, lines)
- ✅ Nenhum arquivo de produção foi modificado
- ✅ Testes são independentes (podem rodar em qualquer ordem)

## Rules (Non-Negotiable)

- **NUNCA** modifique código de produção nesta skill
  - Skill = TESTES APENAS
  - Implementação = outra skill ou agent

- **SEMPRE** use nomes descritivos
  - ✅ it('should add two positive numbers')
  - ❌ it('should work')

- **SEMPRE** inclua comentários em casos complexos
  ```typescript
  // Testa behavior quando servidor retorna 500
  it('should handle server error gracefully', async () => { ... });
  ```

- **Cobertura mínima:** 80% OBRIGATÓRIA
  - Statements: 80%+
  - Branches: 80%+
  - Functions: 80%+
  - Lines: 80%+

- **Testes devem ser independentes**
  - Cada teste setup seu próprio estado
  - Não use estado global entre testes
  - Ordem de execução não importa

- **Sem testes falhando**
  - Skill NÃO finaliza se `npm test` falhar
  - Skill NÃO retorna summary se cobertura < 80%

## Examples (Completos)

### Example 1: Função Simples

**Input:** Arquivo src/utils/formatDate.ts
```typescript
export function formatDate(date: Date, format: string = 'MM/DD/YYYY'): string {
  if (!date || !(date instanceof Date)) {
    throw new Error('Invalid date');
  }
  // Implementation...
  return formatted;
}
```

**Expected Output:** src/utils/__tests__/formatDate.test.ts
```typescript
describe('formatDate', () => {
  it('should format date with default format', () => {
    const date = new Date('2024-01-15');
    expect(formatDate(date)).toBe('01/15/2024');
  });

  it('should format date with custom format', () => {
    const date = new Date('2024-01-15');
    expect(formatDate(date, 'YYYY-MM-DD')).toBe('2024-01-15');
  });

  it('should throw error for invalid date', () => {
    expect(() => formatDate(null as any)).toThrow('Invalid date');
    expect(() => formatDate({} as any)).toThrow('Invalid date');
  });

  it('should handle edge case: start of month', () => {
    const date = new Date('2024-01-01');
    expect(formatDate(date)).toBe('01/01/2024');
  });
});
```

**Summary:** 4 tests, 100% coverage

---

### Example 2: Componente com Async

**Input:** src/components/UserList/UserList.tsx
```typescript
export const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers().then(setUsers).finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
};
```

**Expected Output:** src/components/UserList/__tests__/UserList.test.tsx
```typescript
describe('UserList', () => {
  it('should show loading state initially', () => {
    // Mock fetch
    jest.spyOn(global, 'fetch').mockImplementation(() =>
      new Promise(resolve => setTimeout(resolve, 100))
    );
    
    render(<UserList />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should display users after loading', async () => {
    const mockUsers = [{ id: '1', name: 'John' }, { id: '2', name: 'Jane' }];
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers
    });

    render(<UserList />);
    
    await waitFor(() => {
      expect(screen.getByText('John')).toBeInTheDocument();
      expect(screen.getByText('Jane')).toBeInTheDocument();
    });
  });

  it('should handle fetch error', async () => {
    jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('Network error'));
    
    render(<UserList />);
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

**Summary:** 3 tests, 95% coverage (1 error path não testado)

## Validation Checklist

Antes de finalizar, verificar:

- [ ] `npm test` passa sem warnings/errors
- [ ] `npm test -- --coverage` mostra > 80% em TODAS as métricas
  - [ ] Statements: 80%+
  - [ ] Branches: 80%+
  - [ ] Functions: 80%+
  - [ ] Lines: 80%+
- [ ] Nenhum arquivo src/ foi modificado (apenas __tests__)
- [ ] Nomes de testes são descritivos
- [ ] Edge cases estão cobertos
- [ ] Testes são independentes (sem dependência de ordem)
- [ ] Testes não usam hardcoded delays (use waitFor())
- [ ] Sem console.log() ou debugger no teste

## References

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [React Testing Library Guide](https://testing-library.com/docs/react-testing-library/intro)
- [Testing Best Practices](./references/testing-patterns.md)
- [Project Testing Standards](../../docs/TESTING.md)
```

**YAML Fields (COMPLETE SCHEMA):**

| Campo | Type | Required | Descrição |
|-------|------|----------|-----------|
| `name` | string | ✅ | kebab-case, DEVE combinar com folder name |
| `description` | string | ✅ | 3-5 linhas, keywords para automatic discovery |
| `license` | string | ❌ | MIT, Apache-2.0, Proprietary, etc |
| `allowed-tools` | array | ❌ | Pre-approve: shell, bash, etc |
| `context` | string | ❌ | 'fork' = isolated subagent |
| `user-invocable` | boolean | ❌ | Pode ser invocado com `/nome`? |
| `disable-model-invocation` | boolean | ❌ | Desabilitar invocação automática? |
| `metadata` | object | ❌ | Custom fields |

**Token Cost:** 5-10 tokens discovery + ~250-400 se houver match

---

## 💬 PROMPTS - Estrutura Completa

### Arquivo: `.github/prompts/generate-component.prompt.md`

### Estrutura Completa com Todas as Tags

```markdown
---
# ========== REQUIRED FIELDS ==========
description: >
  Generate a new React TypeScript component with full test coverage.
  Use when you need to create a component, scaffold a component structure,
  or initialize a new component file from scratch.
  Keywords: component, react, create component, new component, scaffold,
  generate component, component template.

# ========== OPTIONAL FIELDS ==========
# Agent to run this prompt in
agent: 'developer'

# Model preference
model: 'claude-opus-4-6'

# Tools available
tools:
  - search/codebase
  - vscode/askQuestions
  - edit

# Variables with user input
argument-hint: 'Describe the component you want to create'

# Handoffs after execution
# handoffs:
#   - label: 'Create Tests'
#     agent: 'test-specialist'
#     prompt: 'Generate tests for the component above'
#     send: false
---

# Generate React Component

Your goal is to generate a new React TypeScript component with full typing and tests.

## Prerequisites

Before starting, verify:
- [ ] Component purpose is clear
- [ ] You know the props the component needs
- [ ] Design system is available at src/styles/design-system.ts

## Inputs Needed

If not provided, ask for:
1. **Component Name**
   - Example: UserCard, LoginForm, NavBar
   - Format: PascalCase
   - Storage: src/components/<ComponentName>/

2. **Component Type**
   - Functional component (default)
   - Form component
   - Container/Page component
   - Utility component

3. **List of Props**
   - For each prop: name, type, required?, default?
   - Example: label: string (required), disabled: boolean (optional, default=false)

4. **Behavior**
   - What should component do? Click handlers? Form submission? State management?
   - Any special interactions?

## Output Structure

Will generate:
1. **Component File**
   - Location: src/components/<ComponentName>/<ComponentName>.tsx
   - TypeScript interface for Props
   - JSDoc comments
   - Responsive design with Tailwind

2. **Test File**
   - Location: src/components/<ComponentName>/__tests__/<ComponentName>.test.tsx
   - 80%+ coverage with Jest + React Testing Library
   - Tests for render, props, interactions

3. **Index File**
   - Location: src/components/<ComponentName>/index.ts
   - Exports component for cleaner imports

4. **Type Definitions** (if needed)
   - Location: src/types/<ComponentName>.ts
   - Shared type definitions used by multiple components

## Implementation Plan

### Step 1: Ask for Component Details

Use #tool:vscode/askQuestions to gather:
```
? Component name: UserCard
? Component type: Functional component
? Props: id:string, name:string, email:string, onClick:function
```

### Step 2: Check Existing Components

Use #tool:search/codebase to find:
- Similar components for patterns
- Existing TypeScript interfaces
- Component examples

### Step 3: Create Component File

Generate src/components/<ComponentName>/<ComponentName>.tsx:

```typescript
import React from 'react';

interface ${ComponentName}Props {
  // Props from user input
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

/**
 * ${ComponentName} component
 * 
 * @param props - Component props
 * @returns React component
 */
export const ${ComponentName}: React.FC<${ComponentName}Props> = ({
  label,
  onClick,
  disabled = false
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
    >
      {label}
    </button>
  );
};
```

Standards to follow:
- Use functional components (not class)
- TypeScript interfaces for props
- JSDoc comments (/** ... */)
- Tailwind CSS classes for styling
- No inline styles
- Accessible (ARIA, semantic HTML)

### Step 4: Create Test File

Generate src/components/<ComponentName>/__tests__/<ComponentName>.test.tsx:

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ${ComponentName} } from '../${ComponentName}';

describe('${ComponentName}', () => {
  it('should render with label', () => {
    render(<${ComponentName} label="Click me" onClick={jest.fn()} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const onClick = jest.fn();
    render(<${ComponentName} label="Click" onClick={onClick} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<${ComponentName} label="Click" onClick={jest.fn()} disabled={true} />);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

Requirements:
- Minimum 80% coverage
- Test render, props, interactions
- Use React Testing Library (not Enzyme)
- Test accessibility

### Step 5: Update Exports

Edit src/components/index.ts:
```typescript
export { ${ComponentName} } from './${ComponentName}/${ComponentName}';
```

### Step 6: Validate

Run validation commands:
```bash
npm test -- ${ComponentName}.test.tsx      # Tests pass?
npm test -- --coverage ${ComponentName}     # Coverage > 80%?
npm run lint                                # ESLint passes?
npm run format --check                      # Prettier formatted?
```

## Rules (Non-Negotiable)

- **ALWAYS** use TypeScript interfaces for props
  - ✅ interface UserCardProps { ... }
  - ❌ (props: any)

- **NEVER** use `any` type
  - ✅ string, number, boolean, User[], etc
  - ❌ any

- **ALWAYS** create test file alongside component
  - Tests are not optional
  - Minimum 80% coverage required

- **ALWAYS** add JSDoc comments
  - Document the component's purpose
  - Document each prop
  - Document complex logic

- **Use PascalCase for component names**
  - ✅ UserCard, LoginForm
  - ❌ userCard, user-card

- **Use kebab-case for file/folder names**
  - ✅ src/components/user-card/UserCard.tsx
  - ❌ src/components/UserCard/UserCard.tsx

## Examples

### Example 1: Simple Button Component

**Input:**
```
Component name: ActionButton
Type: Functional
Props:
  - label: string (required)
  - onClick: () => void (required)
  - variant: "primary" | "secondary" (default="primary")
```

**Output:**
```typescript
// src/components/ActionButton/ActionButton.tsx
interface ActionButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export const ActionButton: React.FC<ActionButtonProps> = ({
  label,
  onClick,
  variant = 'primary'
}) => {
  const baseClass = 'px-4 py-2 rounded font-medium transition-colors';
  const variantClass = variant === 'primary' 
    ? 'bg-blue-600 text-white hover:bg-blue-700'
    : 'bg-gray-200 text-gray-800 hover:bg-gray-300';

  return (
    <button className={`${baseClass} ${variantClass}`} onClick={onClick}>
      {label}
    </button>
  );
};
```

### Example 2: Form Component with Validation

**Input:**
```
Component name: EmailInput
Type: Form component
Props:
  - value: string (required)
  - onChange: (value: string) => void (required)
  - error?: string (optional)
  - placeholder?: string (default="Enter email")
```

**Output:** Component with validation, error display, accessibility features

## Validation Checklist

- [ ] Component file created at correct path
- [ ] Test file created with 80%+ coverage
- [ ] index.ts updated with export
- [ ] npm test passes
- [ ] npm run lint passes
- [ ] All props are typed (no `any`)
- [ ] Component has JSDoc comments
- [ ] Uses Tailwind CSS (not inline styles)
- [ ] Handles accessibility (ARIA, semantic HTML)

## References

- [React Best Practices](../../docs/REACT.md)
- [Component Examples](../../docs/COMPONENTS.md)
- [Design System](../../src/styles/design-system.ts)
- [Testing Standards](../../docs/TESTING.md)
```

**YAML Fields (COMPLETE SCHEMA):**

| Campo | Type | Required | Descrição |
|-------|------|----------|-----------|
| `description` | string | ✅ | 3-4 linhas, keywords, quando usar |
| `agent` | string | ❌ | Agent específico (ex: developer) |
| `model` | string\|array | ❌ | Modelo preferido |
| `tools` | array | ❌ | Tools disponíveis |
| `argument-hint` | string | ❌ | Hint para input do usuário |
| `handoffs` | array | ❌ | Transições de workflow |

**Token Cost:** 0 se não invocar, ~150-200 quando invocar `/nome`

---

## 🔒 HOOKS - Estrutura Completa

### Arquivo: `.github/hooks/copilot-hooks.json` (PROJETO APENAS, NÃO user-level)

### Estrutura Completa com Todos os Eventos

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "bash": "echo '🚀 Session started. Running pre-flight checks...'",
        "timeout": 10,
        "description": "Welcome message and initial validation"
      },
      {
        "type": "command",
        "bash": "npm run type-check 2>/dev/null || true",
        "timeout": 30,
        "description": "Validate TypeScript types"
      }
    ],

    "userPromptSubmit": [
      {
        "type": "command",
        "bash": "./scripts/validate-prompt.sh",
        "timeout": 5,
        "description": "Audit user requests for safety"
      }
    ],

    "preToolUse": [
      {
        "type": "command",
        "bash": "./scripts/check-secrets.sh",
        "timeout": 15,
        "description": "Check for exposed secrets before running any tool"
      },
      {
        "type": "command",
        "bash": "test -f 'src/test-file-to-modify.ts' || (echo 'File not found'; exit 1)",
        "timeout": 5,
        "description": "Validate file exists before edit tool"
      }
    ],

    "postToolUse": [
      {
        "type": "command",
        "bash": "npx prettier --write \"$TOOL_INPUT_FILE_PATH\" 2>/dev/null || true",
        "timeout": 30,
        "description": "Auto-format edited files with Prettier"
      },
      {
        "type": "command",
        "bash": "npm run lint -- \"$TOOL_INPUT_FILE_PATH\" 2>/dev/null || true",
        "timeout": 20,
        "description": "Lint files after editing"
      }
    ],

    "preCompact": [
      {
        "type": "command",
        "bash": "echo 'Context about to be compacted. Saving state...'",
        "timeout": 5,
        "description": "Warning before context compaction (long sessions)"
      }
    ],

    "sessionEnd": [
      {
        "type": "command",
        "bash": "echo '✅ Session ended successfully'",
        "timeout": 5,
        "description": "Cleanup and final logging"
      }
    ],

    "errorOccurred": [
      {
        "type": "command",
        "bash": "echo 'Error detected. Check logs in .copilot/error.log'",
        "timeout": 5,
        "description": "Error notification and logging"
      }
    ]
  }
}
```

### Hook Events Completos

| Evento | Quando Dispara | Uso Típico | Pode Bloquear |
|--------|---------------|-----------|--------------|
| `sessionStart` | Inicia nova sessão | Validar projeto, log | ❌ Não |
| `userPromptSubmit` | Antes processar prompt | Audit requests | ❌ Não |
| `preToolUse` | Antes executar tool | Bloquear operações | ✅ SIM |
| `postToolUse` | Depois executar tool | Formatter, lint | ❌ Não |
| `preCompact` | Antes compactar contexto | Refresh estado | ❌ Não |
| `sessionEnd` | Fim da sessão | Cleanup, logs | ❌ Não |
| `errorOccurred` | Erro acontece | Log, notificação | ❌ Não |

### Exemplos de Hooks

#### Hook 1: Pre-Tool Security Check

```json
{
  "preToolUse": [
    {
      "type": "command",
      "bash": "cat > /tmp/hook-input.json << 'EOF'\n${HOOK_INPUT}\nEOF\n./scripts/validate-tool-safety.sh /tmp/hook-input.json",
      "timeout": 15,
      "description": "Validate tool use is safe (no prod changes without approval)"
    }
  ]
}
```

Script: `scripts/validate-tool-safety.sh`
```bash
#!/bin/bash

INPUT_FILE=$1
TOOL=$(jq -r '.toolName' $INPUT_FILE)
ARGS=$(jq -r '.args | join(" ")' $INPUT_FILE)

# Block dangerous commands
if [[ "$TOOL" == "shell" && "$ARGS" == *"rm -rf"* ]]; then
  echo "❌ BLOCKED: Dangerous rm -rf command"
  exit 1
fi

if [[ "$TOOL" == "shell" && "$ARGS" == *"DROP TABLE"* ]]; then
  echo "❌ BLOCKED: SQL injection attempt"
  exit 1
fi

# Allow
exit 0
```

#### Hook 2: Post-Tool Auto-Format

```json
{
  "postToolUse": [
    {
      "type": "command",
      "bash": "[ -f \"$TOOL_INPUT_FILE_PATH\" ] && npx prettier --write \"$TOOL_INPUT_FILE_PATH\" || true",
      "timeout": 30,
      "description": "Format with Prettier after file edit"
    }
  ]
}
```

#### Hook 3: Session Validation

```json
{
  "sessionStart": [
    {
      "type": "command",
      "bash": "npm run type-check && npm run lint --quiet || echo 'Warning: type or lint errors'",
      "timeout": 60,
      "description": "Validate project health"
    }
  ]
}
```

### Variables Disponíveis em Hooks

```bash
# Pre/Post ToolUse
$TOOL_NAME             # Tool being invoked (shell, edit, search, etc)
$TOOL_INPUT_FILE_PATH  # File path being modified
$HOOK_INPUT            # Full JSON input from Copilot

# Session
$COPILOT_SESSION_ID    # Unique session identifier
$COPILOT_USER          # User email/username
$COPILOT_WORKSPACE     # Current workspace path
```

### Output JSON Format (Pre-tool blocking)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "This command modifies production database",
    "systemMessage": "⚠️ Requires approval: Do you want to proceed?"
  }
}
```

Valores para `permissionDecision`:
- `"allow"` — Permitir e continuar
- `"ask"` — Pedir confirmação ao usuário
- `"deny"` — Bloquear comando

**Token Cost:** 0 tokens (executa em background)

---

## 🏷️ Tags Markdown Suportadas

### Tags Suportadas no Copilot (Não são HTML)

#### 1. **Referências de Tools** (Em agent, prompt, skill bodies)

```markdown
# Referenciando ferramentas no corpo do arquivo

Use #tool:read para ler arquivos
Use #tool:edit para modificar código
Use #tool:search para procurar no workspace
Use #tool:shell para executar comandos

Exemplo no corpo de um agent:
"Reference your tools using the #tool:tool-name syntax.
For example: #tool:web/fetch for browser fetching."
```

**Sintaxe:**
- `#tool:read` — Ler arquivo
- `#tool:edit` — Editar arquivo
- `#tool:search` — Procurar
- `#tool:shell` — Terminal
- `#tool:web/fetch` — Fetch HTTP
- `#tool:vscode/askQuestions` — Perguntar ao usuário

#### 2. **Referências de Prompts** (Em agent)

```markdown
# Referência a outros prompts
Para referenciar outro prompt, use:
#prompt:generate-component
#prompt:create-migration

Exemplo:
"After implementing, use #prompt:create-tests to generate tests."
```

#### 3. **Referências de Skills** (Em agent)

```markdown
# Referência a skills
Para referenciar uma skill:
#skill:testing
#skill:debugging
#skill:code-review

Exemplo:
"Use #skill:testing to generate comprehensive test coverage."
```

#### 4. **Referências de Agents** (Em handoffs)

```yaml
handoffs:
  - label: 'Code Review'
    agent: 'code-reviewer'    # Referência ao agent
    prompt: 'Review the above'
    send: false
```

#### 5. **Referências a Arquivos** (Markdown links)

```markdown
# Referência a arquivos no repositório
[copilot-instructions.md](../../.github/copilot-instructions.md)
[API Documentation](../../docs/API.md)
[Testing Guide](./references/testing-best-practices.md)

Caminhos relativos funcionam:
- `../../docs/` — sobe 2 níveis
- `./references/` — mesma pasta
```

#### 6. **Variáveis de Input** (Em prompts)

```markdown
# Perguntar ao usuário por input
${input:componentName}
${input:componentName:Enter component name}  # Com placeholder

# Usar seleção atual
${selection}

# Usar arquivo atual
${file}
```

Exemplo:
```markdown
Component name: ${input:componentName:e.g., UserCard}
Selected code:
${selection}
```

#### 7. **Blocos de Código** (Markdown padrão)

```markdown
# Blocos de código com sintaxe
\`\`\`typescript
interface Props {
  name: string;
}
\`\`\`

\`\`\`bash
npm test
\`\`\`

\`\`\`json
{ "version": "1.0" }
\`\`\`
```

Linguagens suportadas:
- `typescript`, `javascript`
- `bash`, `shell`
- `python`
- `json`, `yaml`
- `html`, `css`, `scss`
- `sql`
- etc...

#### 8. **Formatação Markdown Padrão** (Todas suportadas)

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
~~Strikethrough~~

- Bullet list
- Item 2

1. Numbered list
2. Item 2

> Blockquote
> Continued quote

| Table | Column |
|-------|--------|
| Data  | Data   |

[Link](https://example.com)
![Image](./path/to/image.png)

---  (Horizontal rule)

`inline code`
```

#### 9. **Checklist** (GitHub Markdown)

```markdown
- [ ] Incomplete task
- [x] Completed task
```

### Tags NÃO Suportadas

❌ **HTML Tags** — Não funciona
```html
<!-- Não funciona em Copilot -->
<div>...</div>
<style>...</style>
<script>...</script>
```

❌ **Custom Tags** — Não são padrão
```
<!-- Não são reconhecidas -->
<custom-tag>
@custom-tag
::custom-tag
```

### Tags Suportadas por Contexto

| Tag | Agent | Skill | Prompt | Instructions | Hooks |
|-----|-------|-------|--------|--------------|-------|
| `#tool:*` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `#skill:*` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `#prompt:*` | ✅ | ✅ | ✅ | ❌ | ❌ |
| Links `[](...)` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `${input:...}` | ❌ | ❌ | ✅ | ❌ | ❌ |
| Markdown padrão | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## 🌡️ Temperatura em Agents (Pesquisa e Evidências)

### STATUS ATUAL (Maio 2026)

**Pesquisa encontrou:**

Alguns usuários perguntaram se é possível ajustar a "temperatura" no GitHub Copilot do VSCode. A questão mencionou a possibilidade de adicionar configuração em settings.json, mas essa configuração não funciona mais. Não há referência na documentação oficial, sugerindo que o recurso pode ter sido removido ou alterado.

### Temperatura em Diferentes Contextos

#### 1. **Agents no GitHub Copilot (VS Code)**

**Status:** ⚠️ **NÃO SUPORTADO OFICIALMENTE** em frontmatter YAML

```yaml
# ❌ NÃO FUNCIONA:
name: developer
description: ...
temperature: 0.3  # Não é reconhecido
```

**Por quê?**
- GitHub Copilot usa modelo defaults (sem customização de temperatura)
- Temperatura é controlada pelo serviço, não pelo usuário
- Documentação oficial não menciona este campo

#### 2. **Prompts** (.prompt.md)

**Status:** ⚠️ **NÃO SUPORTADO OFICIALMENTE**

```yaml
# ❌ NÃO FUNCIONA:
agent: developer
temperature: 0.5  # Não é reconhecido
```

#### 3. **Alternativas (O que FUNCIONA)**

Você pode controlar "criatividade" através de:

**Opção 1: Seleção de Modelo**
```yaml
# Agent - escolher modelo mais/menos criativo
name: developer
model: 'claude-opus-4-6'      # Mais capaz
# vs
model: 'claude-sonnet-4.5'    # Mais rápido, menos criativo
```

**Opção 2: Instruções Explícitas**
```markdown
# No corpo do agent, seja explícito:

## When Generating Code
- Be CONSERVATIVE: Use established patterns only
- Avoid experimental approaches
- Follow proven solutions from project history

(Para "temperatura baixa" = determinístico)

---

## When Generating Ideas
- Be CREATIVE: Consider multiple approaches
- Suggest novel solutions
- Think outside the box

(Para "temperatura alta" = criativo)
```

**Opção 3: Seleção de Agent**
```yaml
# Criar agents diferentes para diferentes "temperaturas"

Agent 1: conservative-developer (para produção, rígido)
Agent 2: creative-developer (para brainstorm, flexível)
```

### Estudos & Evidências

Em Microsoft Copilot Studio, o parâmetro de temperatura varia entre 0 e 1, e guia o modelo generativo de IA sobre quanta criatividade (1) versus resposta determinística (0) ele fornecerá. No entanto, a configuração de temperatura não está disponível para o modelo GPT-5 reasoning.

Em alguns sistemas (como em Teleport), a temperatura foi definida como 0.3 para produzir resultados mais focados e consistentes, em vez do padrão 1.0.

### Recomendação Prática

```markdown
# MELHOR ABORDAGEM HOJE (Maio 2026)

❌ NÃO confie em temperatura nos agentes (não funciona)

✅ USE ESTE PADRÃO ao invés:

1. Criar 2 agents:
   - @developer-strict (prompt: "Be conservative, follow patterns")
   - @developer-creative (prompt: "Explore novel approaches")

2. Ou use instruções no agent body:
   "When implementing features:
    - Use ONLY established patterns from project history
    - Be conservative with dependencies
    - Prioritize stability over innovation"

3. Ou deixe que model selection faça isso:
   - Claude Opus 4.6 = mais criativo
   - Claude Sonnet 4.5 = mais focado
```

---

## 📊 Matriz Comparativa Completa

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                        5 COMPONENTES - COMPARAÇÃO COMPLETA                     │
├────────────────────────────────────────────────────────────────────────────────┤
│ Aspecto              │ Instructions  │ Agents      │ Skills       │ Prompts    │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Arquivo              │ .md (plain)   │ .agent.md   │ SKILL.md     │ .prompt.md │
│ Localização          │ .github/      │ .github/    │ .github/ ou  │ .github/   │
│                      │ (também ~/)   │ (ou ~/)     │ ~/ ambos ok  │ (ou ~/)    │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Carregamento         │ SEMPRE        │ Selecionado │ Sob demanda  │ Manual (/) │
│ (quando?)            │ (sempre on)   │ (quando @)  │ (automatch)  │ (quando /) │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Token Cost           │ 40-80 PER REQ │ ~50/session │ 5-10 discovery│ 0 if not  │
│ (por requisição)     │ (CARO)        │ (médio)     │ +250 se match │ ~150 if / │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Invocação            │ Automática     │ @developer  │ /testing ou  │ /nome      │
│ (como usar?)         │ (sempre)      │ @pm, @etc   │ automático   │ (manual)   │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Frontmatter YAML     │ Nenhum        │ Sim (name,  │ Sim (name,   │ Sim (desc, │
│ (requerido?)         │               │ desc, tools)│ desc)        │ agent, etc)│
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Temperatura          │ Não           │ Não support │ Não support  │ Não        │
│ (suportado?)         │ applicable    │ oficialmente│ oficialmente  │ support    │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Model Selection      │ Não           │ Sim         │ Não          │ Sim        │
│ (pode escolher?)     │               │ (frontmatter)│            │ (frontmatter)|
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Tools                │ Não           │ Sim (lista) │ Opcional (allowed-│ Sim   │
│ (definir tools?)     │               │             │ tools)       │             │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Reuso                │ Global/auto   │ Sessão só   │ Multi-agent  │ Slash cmd  │
│ (reutilizável?)      │               │             │ + portável   │ manual     │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Tamanho Recomendado  │ Max 50 linhas │ 50-100 lin. │ 100-300 lin. │ 50-150 lin │
│                      │ (MÍNIMO)      │ (focado)    │ (detalhado)  │ (conciso)  │
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Quando Usar          │ Convenções    │ Personas    │ Tarefas bem- │ Atalhos    │
│                      │ globais       │ diferentes  │ definidas    │ repetitivos│
├──────────────────────┼───────────────┼─────────────┼──────────────┼────────────┤
│ Precedência          │ Project >     │ Project >   │ (local)      │ (user >    │
│                      │ Org > Empresa │ Org > Emp   │              │ project)   │
└────────────────────────────────────────────────────────────────────────────────┘

HOOKS (Não aparece na tabela pois é diferente):
├────────────────────┬──────────────────────────────────────────────────────┤
│ Arquivo            │ .json (config JSON)                                  │
│ Localização        │ .github/hooks/ APENAS (não suporta ~/)               │
│ Trigger            │ Eventos (sessionStart, preToolUse, postToolUse...)   │
│ Token Cost         │ 0 tokens (background)                                │
│ Quando Usar        │ Policy enforcement, formatação, validação            │
└────────────────────┴──────────────────────────────────────────────────────┘
```

---

## 💻 Exemplos Práticos Enriquecidos

### Exemplo 1: Setup Completo User-Level

```bash
# Estrutura final
~/.copilot/
├── copilot-instructions.md          (50 linhas - global standards)
├── agents/
│   ├── developer.agent.md           (80 linhas)
│   ├── tech-lead.agent.md           (80 linhas)
│   ├── pm.agent.md                  (75 linhas)
│   └── data-analyst.agent.md        (70 linhas)
├── skills/
│   ├── testing/
│   │   ├── SKILL.md                 (200 linhas)
│   │   ├── scripts/
│   │   │   └── run-coverage.sh
│   │   └── templates/
│   │       └── test-template.ts
│   ├── debugging/SKILL.md           (150 linhas)
│   ├── code-review/SKILL.md         (180 linhas)
│   └── documentation/SKILL.md       (140 linhas)
└── prompts/
    ├── generate-component.prompt.md (120 linhas)
    ├── create-migration.prompt.md   (100 linhas)
    └── release-notes.prompt.md      (110 linhas)

TOTAL SETUP: ~2000 linhas, reutilizável em TODOS os projetos
TOKEN SAVINGS: 70-80% comparado a padrão ineficiente
```

### Exemplo 2: Usando Tudo Junto

```
WORKFLOW PRÁTICO:

1. Abre VSCode
   └─ copilot-instructions.md loaded (~50 tokens)

2. Clica em @developer
   └─ developer.agent.md loaded (~50 tokens)
   └─ Skills discovery: testing, debugging, etc (~40 tokens)

3. Digita: "Crie um componente de login"
   └─ /generate-component skill ativado (~250 tokens)
   └─ Cria LoginForm.tsx + testes

4. Digita: "Crie testes para sum()"
   └─ /testing skill ativado (~250 tokens)
   └─ Cria sum.test.ts com 100% cobertura

5. Usa handoff para code-review
   └─ code-reviewer agent (~50 tokens)
   └─ Usa /code-review skill (~250 tokens)

TOTAL: ~950 tokens spread across SESSION
(vs ~2000+ tokens se tudo no agent monolítico)
```

---

## 📌 Resumo Executivo

### ✅ Estrutura Recomendada (Maio 2026)

```yaml
# Cada componente tem sua estrutura específica:

Instructions:
  - Format: Markdown plain (NO YAML)
  - Size: max 50 linhas
  - Scope: global
  - Discovery: nenhuma (sempre-on)

Agents:
  - Format: Markdown + YAML frontmatter
  - Fields: name, description, tools, model, handoffs
  - Size: 50-100 linhas
  - Discovery: @nome (manual)

Skills:
  - Format: Markdown + YAML frontmatter
  - Fields: name, description, allowed-tools, license
  - Size: 100-300 linhas
  - Discovery: automatic + /nome (manual)
  - Structure: SKILL.md + scripts/ + examples/ + references/

Prompts:
  - Format: Markdown + YAML frontmatter
  - Fields: description, agent, model, tools, argument-hint
  - Size: 50-150 linhas
  - Discovery: /nome (manual)

Hooks:
  - Format: JSON (config)
  - Location: .github/hooks/ ONLY
  - Events: 7 tipos de eventos
  - Discovery: automatic (eventos)
```

### 🎯 Não se Esqueça

- ⚠️ **Temperatura NÃO funciona** em agents/prompts — use instruções ou model selection
- ⚠️ **Hooks APENAS em .github/hooks** — não suporta user-level
- ⚠️ **Skills descobertas por description** — keywords são críticas
- ⚠️ **Tags especiais:** `#tool:name`, `#skill:name`, `[links](path)`, `${input:}`
- ⚠️ **Sem HTML** — use Markdown puro

---

**Documento Completo v3.0 - Estruturas, Tags, Schemas, Temperatura, Exemplos**

**Pronto para implementação e treinamento de equipes em Maio 2026**

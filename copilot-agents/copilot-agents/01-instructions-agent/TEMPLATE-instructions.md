# PROJECT_NAME - Global Standards

**Descrição:** Convenções globais que SEMPRE devem ser seguidas em todo o projeto.

## Tech Stack Overview

- **Frontend:** [Framework] [version]+, [Language] [version]+, [CSS Framework] [version]+
- **Backend:** [Runtime] [version] LTS, [Framework] [version]+, [Database] [version]+
- **Testing:** [Framework] [version]+, [Library] [version]+
- **Package Manager:** [Manager] [version]+
- **Build Tool:** [Tool] [version]
- **CI/CD:** [Service]

## Naming Conventions (MANDATORY)

### Variables & Functions
```
✅ Correct: const userEmail = "..."
❌ Incorrect: const user_email = "..."
```
- camelCase ALWAYS for variables, functions, methods
- Descriptive names (no single letters except i, j, k in loops)

### Classes, Types, Interfaces
```
✅ Correct: class UserManager {}
❌ Incorrect: class user_manager {}
```
- PascalCase ALWAYS
- No redundant prefixes

### Constants
```
✅ Correct: const API_TIMEOUT = 5000
❌ Incorrect: const apiTimeout = 5000
```
- UPPER_SNAKE_CASE

### Files & Folders
```
✅ Correct: src/utils/date-formatter.ts
❌ Incorrect: src/utils/dateFormatter.ts
```
- kebab-case ALWAYS

## Project Structure (Canonical)

```
src/
├── components/        # UI components
├── hooks/            # Custom hooks
├── services/         # API integrations
├── utils/            # Helper functions
├── types/            # Type definitions
├── styles/           # Styles
└── tests/            # Test files
```

## Error Handling Pattern (MANDATORY)

```typescript
try {
  const data = await fetchData(id);
  return data;
} catch (error) {
  logger.error('Operation failed', {
    id,
    error: error instanceof Error ? error.message : 'Unknown',
    timestamp: new Date().toISOString()
  });
  throw new AppError('User-friendly message', 'ERROR_CODE', { originalError: error });
}
```

## TypeScript Requirements (MANDATORY)

```typescript
interface UserProps {
  id: string;
  name: string;
  email?: string;
}

const UserCard: React.FC<UserProps> = ({ id, name }) => {
  return <div>{name}</div>;
};
```

## Testing Standards (MANDATORY)

- **Coverage minimum**: 80% for new code
- **Framework**: Jest + React Testing Library
- **Test naming**: `describe('Component', () => { it('should...') })`
- **Async**: Always use `async/await`

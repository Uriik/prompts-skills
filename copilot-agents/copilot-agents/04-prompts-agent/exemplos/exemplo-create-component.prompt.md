---
description: "Generate React component scaffold with TypeScript, props validation, JSDoc, and test file"
agent: developer
model: claude-sonnet-4-20250514
tools:
  - code-generator
  - test-generator
  - formatter
argument-hint: "ComponentName and brief description"
---

# Create Component - React + TypeScript + Tests

## Purpose

This prompt automates scaffolding of new React components following your project standards. It creates a complete, production-ready component structure with TypeScript types, JSDoc documentation, and a test file—saving significant time and ensuring consistency.

## What This Prompt Does

1. **Analyzes your input** - Component name and brief description
2. **Generates component file** - React.FC with TypeScript props interface
3. **Creates TypeScript interface** - Typed props with JSDoc comments
4. **Adds JSDoc comments** - Clear documentation for future developers
5. **Creates test file** - Basic tests to start from (following 80% coverage target)
6. **Formats everything** - Applies Prettier and project style rules

The output follows your project's naming conventions, file structure, and testing standards.

## How to Use

Type `/create-component` followed by your component needs:

```
/create-component Modal dialog for user confirmation
```

The system will:
- Create `Modal.tsx` with the component
- Create `Modal.test.tsx` with initial tests
- Output JSDoc-documented interfaces
- Provide TypeScript types

And deliver complete, ready-to-edit files.

## Input Parameters

- `ComponentName`: PascalCase name (e.g., `UserProfile`, `AlertBanner`)
- `description`: 1-2 words describing the component's purpose (e.g., "user profile card", "navigation menu")

**Format**: `ComponentName description`

## Output Format

You will receive:

1. **Component file** - src/components/ComponentName/ComponentName.tsx
2. **Types interface** - TypeScript interface for props
3. **Test file** - src/components/ComponentName/__tests__/ComponentName.test.tsx
4. **Index export** - src/components/ComponentName/index.ts

All formatted and ready to integrate.

## Examples

### Example 1: Modal Dialog

**Input:**
```
/create-component Modal user confirmation dialog
```

**Output:**
```typescript
// Modal.tsx
interface ModalProps {
  /** Whether the modal is open */
  isOpen: boolean;
  /** Title displayed in modal header */
  title: string;
  /** Modal content */
  children: React.ReactNode;
  /** Callback when confirm button clicked */
  onConfirm: () => void;
  /** Callback when cancel button clicked */
  onCancel: () => void;
}

const Modal: React.FC<ModalProps> = ({ isOpen, title, children, onConfirm, onCancel }) => {
  if (!isOpen) return null;
  return (
    <div className="modal">
      <h2>{title}</h2>
      {children}
      <button onClick={onConfirm}>Confirm</button>
      <button onClick={onCancel}>Cancel</button>
    </div>
  );
};

export default Modal;
```

### Example 2: Card Component

**Input:**
```
/create-component UserCard display user information
```

**Output:**
```typescript
// UserCard.tsx
interface UserCardProps {
  /** User unique identifier */
  userId: string;
  /** User display name */
  userName: string;
  /** User email address */
  email: string;
  /** Optional avatar image URL */
  avatarUrl?: string;
  /** Callback when card is clicked */
  onClick?: () => void;
}

const UserCard: React.FC<UserCardProps> = ({ userId, userName, email, avatarUrl, onClick }) => {
  return (
    <div className="user-card" onClick={onClick}>
      {avatarUrl && <img src={avatarUrl} alt={userName} />}
      <h3>{userName}</h3>
      <p>{email}</p>
    </div>
  );
};

export default UserCard;
```

## Tips & Tricks

- **Tip 1**: Be specific in description - "Modal with confirmation" generates better than "Modal"
- **Tip 2**: After generation, run `/testing` prompt to create comprehensive tests
- **Tip 3**: Use `@developer` agent for maximum code quality suggestions
- **Tip 4**: The generated test file is a starting point—expand with edge cases

**Pro tip**: Chain with `/testing modal-dialog` to get 80% coverage immediately after creation.

## Related Prompts

- `/create-hook` - For creating custom React hooks
- `/testing ComponentName` - To add comprehensive tests
- `/refactor ComponentName` - To improve existing component

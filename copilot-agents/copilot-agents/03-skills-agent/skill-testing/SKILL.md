---
name: Testing
description: Create unit tests with Jest and React Testing Library, ensure 80% code coverage, validate test structure and assertions
allowed-tools:
  - test-runner
  - code-coverage-analyzer
  - linter
license: MIT
---

# Testing - Unit Test Creation & Coverage

## Overview

This skill helps you create comprehensive unit tests using Jest and React Testing Library. It ensures your code meets the 80% minimum coverage requirement and follows testing best practices established in your project.

Useful for both new test creation and adding coverage to existing code. Works with React components, utilities, and async functions.

## When to Use This Skill

This skill is most useful when you need to:
- Create new test files for components or functions
- Add tests to existing code that lacks coverage
- Validate test structure before PR
- Ensure async handling is correct

**Triggers**: When creating new code or reviewing coverage reports, use `/testing` to generate test suites.

## Step-by-Step Process

1. **Analyze the Code**
   - Identify functions, components, edge cases
   - Determine which branches to test
   - Plan mock strategies if needed

2. **Create Test Structure**
   - Set up test file with correct naming
   - Import required testing libraries
   - Create describe() blocks by feature

3. **Write Test Cases**
   - Happy path tests (normal operation)
   - Error path tests (what breaks?)
   - Edge case tests (boundaries)
   - Async tests with proper await

4. **Verify Coverage**
   - Run `npm run test:coverage`
   - Ensure ≥80% coverage achieved
   - Document any intentional omissions

5. **Validate & Commit**
   - All tests pass
   - No console warnings
   - Coverage check passes

## Code Templates

### Template 1: Function Testing

```typescript
describe('formatDate', () => {
  it('should format valid date correctly', () => {
    const result = formatDate(new Date('2026-05-08'));
    expect(result).toBe('May 8, 2026');
  });

  it('should handle invalid dates gracefully', () => {
    expect(() => formatDate(null)).toThrow('Invalid date');
  });
});
```

### Template 2: React Component Testing

```typescript
describe('UserCard', () => {
  it('should render user information', () => {
    render(<UserCard user={{ id: '1', name: 'John' }} />);
    expect(screen.getByText('John')).toBeInTheDocument();
  });

  it('should handle click events', async () => {
    const handleClick = jest.fn();
    render(<UserCard user={{ id: '1', name: 'John' }} onClick={handleClick} />);
    
    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### Template 3: Async Function Testing

```typescript
describe('fetchUser', () => {
  it('should fetch user data', async () => {
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      json: async () => ({ id: '1', name: 'John' })
    });

    const result = await fetchUser('1');
    expect(result.name).toBe('John');
  });
});
```

## Best Practices

- **Test Behavior, Not Implementation**: Test what the code does, not how it does it
- **Use Meaningful Assertions**: Each assertion should test one thing clearly
- **Mock External Dependencies**: Use jest.mock() for API calls, timers, etc
- **Name Tests Descriptively**: "should render user name when data loads" is better than "test 1"

**Anti-patterns** to avoid:
- ❌ Testing implementation details (internal state, private methods)
- ❌ Having multiple assertions that test different concerns in one test

## Troubleshooting

### Issue: Coverage still below 80%
**Solution**: Identify uncovered branches with `npm run test:coverage -- --verbose`. Add tests for error cases.

### Issue: Async tests are timing out
**Solution**: Use `async/await` and `waitFor()` from testing-library. Set timeout in jest config if needed.

### Issue: Mock not working in tests
**Solution**: Mock must be called before importing the module. Use `jest.mock()` at top of file.

## References

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library Guide](https://testing-library.com/react)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Coverage Configuration](https://jestjs.io/docs/coverage)

---

**Related Skills**: code-review (for validating test quality), debugging (for understanding test failures)

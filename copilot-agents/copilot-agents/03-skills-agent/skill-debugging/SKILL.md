---
name: Debugging
description: Debug production issues, analyze error logs, trace execution flow, identify root causes, create fix strategies
allowed-tools:
  - debugger
  - log-analyzer
  - error-tracker
license: MIT
---

# Debugging - Issue Investigation & Resolution

## Overview

This skill helps you systematically debug issues by analyzing error logs, tracing execution flows, and identifying root causes. It provides structured approaches to both common issues and complex edge cases.

Covers frontend errors, backend failures, async issues, and integration problems.

## When to Use This Skill

This skill is most useful when you need to:
- Debug production errors with stack traces
- Trace execution flow through multiple modules
- Understand why tests are failing
- Analyze performance issues

**Triggers**: When an error occurs, use `/debug` to systematically investigate.

## Step-by-Step Process

1. **Collect Information**
   - Gather error message and stack trace
   - Check logs (server, browser console)
   - Identify when issue started
   - Note reproduction steps

2. **Analyze the Error**
   - Read the stack trace from bottom to top
   - Identify the actual failure point
   - Check error type (TypeError, ReferenceError, etc)
   - Note the context (what was the code doing?)

3. **Trace Execution**
   - Add console.log() at key points
   - Use debugger breakpoints
   - Track variable values
   - Watch for async issues

4. **Identify Root Cause**
   - Is it a logic error?
   - Is it a data issue?
   - Is it a missing dependency?
   - Is it a configuration problem?

5. **Create Fix & Test**
   - Implement the fix
   - Write test case that reproduces the issue
   - Verify fix doesn't break other code

## Code Templates

### Template 1: Debug with Logging

```typescript
async function fetchAndProcess(id: string) {
  try {
    console.log('Starting fetch for id:', id);
    const data = await fetchUser(id);
    console.log('Fetch successful:', { dataKeys: Object.keys(data) });
    
    const processed = processData(data);
    console.log('Processing complete:', processed);
    return processed;
  } catch (error) {
    console.error('Error in fetchAndProcess:', {
      id,
      error: error instanceof Error ? error.message : error,
      stack: error instanceof Error ? error.stack : undefined
    });
    throw error;
  }
}
```

### Template 2: Debug with Error Boundaries

```typescript
describe('fetchUser', () => {
  it('should surface error with context', async () => {
    try {
      // This should fail
      await fetchUser('invalid-id');
    } catch (error) {
      console.log('Caught error:', {
        type: error.constructor.name,
        message: error.message,
        context: { id: 'invalid-id' }
      });
      throw error;
    }
  });
});
```

### Template 3: Browser Debugging

```javascript
// In browser console:
// 1. Find problematic element
const elem = document.querySelector('.broken-component');

// 2. Inspect computed styles
console.log(getComputedStyle(elem));

// 3. Check React props
console.log(elem.__reactProps$...); // React attaches to elements

// 4. Set breakpoint on events
elem.addEventListener('click', () => { debugger; });
```

## Best Practices

- **Read Error Messages Carefully**: The message usually tells you what went wrong
- **Use Browser DevTools**: Debugger is more powerful than console.log
- **Add Context to Errors**: Include variables, state, user info
- **Test Your Assumptions**: Don't assume you know what's happening

**Anti-patterns** to avoid:
- ❌ Adding console.log everywhere (makes logs unreadable)
- ❌ Ignoring errors (catch without handling)
- ❌ Debugging without understanding the feature first

## Troubleshooting

### Issue: Error happens randomly, can't reproduce
**Solution**: Add more context logging. Check for race conditions, timing issues, or browser inconsistencies.

### Issue: Stack trace shows minified code
**Solution**: Build in development mode or use source maps. Check webpack/rollup config.

### Issue: Error in async code is hard to trace
**Solution**: Use async/await syntax (makes stack traces better). Avoid Promise chains.

## References

- [Chrome DevTools Debugging](https://developer.chrome.com/docs/devtools/)
- [Node.js Debugging](https://nodejs.org/en/docs/guides/debugging-getting-started/)
- [React Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- [Error Handling Best Practices](https://javascript.info/custom-errors)

---

**Related Skills**: testing (for catching issues early), code-review (for preventing issues)

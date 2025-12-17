# Frontend Testing Approach: Behavioral "Black Box" Testing

## Philosophy
Our testing strategy focuses on **User Behavior** rather than **Implementation Details**. We treat the frontend application as a "Black Box": we care about what the user sees and does (inputs, clicks, text on screen), not how the code is structured internally (React components, state management, CSS classes).

This approach ensures that our tests remain valid and useful even as we heavily refactor the codebase, change UI libraries, or restructure our components.

## The Strategy: E2E with Network Mocking
We use **Playwright** to drive a real browser, but we **mock the backend API responses**.

### Core Concepts

1.  **Test the Contract, Not the Backend**: We are testing the frontend's ability to handle data, not the backend's ability to produce it. By mocking the API, we ensure our tests are deterministic, fast, and flake-free.
2.  **Resilient Selectors**: We select elements by their accessible attributes (what the user sees), not their code attributes.
    *   ✅ **Good**: `getByLabel('Pet Name')`, `getByRole('button', { name: 'Save' })`
    *   ❌ **Bad**: `page.locator('.pet-info-form > div:nth-child(2) input')`
3.  **Refactor-Proof**: Because we don't test internal component state or specific DOM structures, we can completely rewrite the implementation (e.g., switch from CSS Grid to Flexbox, or split one component into five) without breaking the tests, provided the user experience remains the same.

## Advantages for Product Evolution

*   **Fearless Refactoring**: You can change the underlying code structure with confidence. If the test passes, the feature still works for the user.
*   **Speed**: Mocking the backend (especially heavy operations like OCR) makes tests run in milliseconds rather than seconds or minutes.
*   **Stability**: Tests won't fail due to backend downtime, network jitter, or changes in OCR accuracy.
*   **Documentation**: The tests serve as live documentation of the user flows and data requirements.

## Example Scenario

**Goal**: Verify a user can edit the pet's name.

**Implementation-Focused Test (Fragile):**
```javascript
// Breaks if we rename the class or move the input
const input = wrapper.find('.name-input');
expect(input.props().value).toBe('Firulais');
```

**Behavioral "Black Box" Test (Robust):**
```javascript
// Works as long as there is an input labeled "Name"
await expect(page.getByLabel('Name')).toHaveValue('Firulais');
```

## Summary
By decoupling our tests from the implementation details, we create a safety net that supports rapid product evolution. We validate that the *application works for the user*, regardless of how it is built under the hood.

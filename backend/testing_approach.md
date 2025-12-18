# Backend Testing Approach: Behavioral & E2E Strategy

## Philosophy
Backend testing strategy prioritizes **End-to-End (E2E) Behavioral Testing** over isolated unit tests for every internal function. This approach treats the application primarily as a black box accessed via its public API endpoints.

This ensures that the tests validate the *business value* delivered to the client, rather than coupling them to the internal implementation details of services, repositories, or adapters.

## Core Concepts

### 1. E2E First (API -> Database)
The majority of the tests interact with the system through the **FastAPI endpoints** and verify the side effects in the **Database**.
*   **Input**: HTTP Requests (POST, PUT, GET).
*   **Output**: HTTP Responses & Database State.
*   **Why**: This guarantees that all layers (API, Service, Persistence) work together correctly. If there is a refactor in the internal service layer but the API response remains the same, the test passes.

### 2. Fixture-Driven Data
The testing approach leverages `pytest` fixtures heavily to manage state and data.
*   **Database Session**: A transactional fixture ensures every test runs in isolation and rolls back changes afterwards.
*   **Data Factories**: Fixtures create complex domain objects (e.g., `create_document`, `create_medical_record`) so tests remain readable and focused on the specific behavior being verified.

### 3. "Green" Refactoring
Because the tests focus on the *external behavior* (API contract), this allows for an aggressively refactor the internal code structure without breaking the test suite.
*   *Example*: switch from a raw SQL query to an ORM method, or split a large service into smaller sub-services. As long as the endpoint returns the correct JSON and updates the DB correctly, the test remains green.

### 4. Handling Third-Party Services
When the application relies on external systems (e.g., OCR engines, Cloud Storage, AI APIs), the proposal is to follow a split strategy:

*   **General Application Tests**: **mock** the external service interfaces.
    *   *Goal*: Verify how the application handles the *responses* (success, failure, data format) from the service, without making actual network calls or incurring costs/latency.
    *   *Mechanism*: Mock the Adapter interface (e.g., `OcrAdapter`), not the internal library calls.

*   **Specific Integration Tests**: Write a small set of dedicated tests that *do* hit the real external service.
    *   *Goal*: Verify the **contract**. Ensure that our adapter correctly communicates with the third-party API and that their API hasn't changed.
    *   *Frequency*: These can be run less frequently or in a separate pipeline stage.

## Summary
By focusing on the API surface and using realistic database fixtures, this approach creates a test suite that gives high confidence in the system's reliability while maintaining the flexibility to evolve the architecture.

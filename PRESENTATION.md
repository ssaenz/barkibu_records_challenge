# Project Presentation & Technical Overview

## Introduction

This document serves as a comprehensive guide to the architectural decisions, technical implementation, and future roadmap for the Barkibu Code Challenge. The solution is designed to be a production-ready, scalable, and maintainable full-stack application for processing and managing veterinary medical records.

## 1. Architecture and Design

The project follows a **Clean Architecture (Hexagonal Architecture)** pattern to ensure separation of concerns, testability, and independence from external frameworks.

### Backend Structure (`/backend`)
The backend is built with **Python** and **FastAPI**, organized into concentric layers:

*   **Domain Layer (`app/domain`)**: Contains the core business logic and entities (`Document`, `MedicalRecord`). This layer has no dependencies on outer layers.
    *   *Key Components*: `DocumentService`, `MedicalRecordExtractor` interface.
*   **Adapters Layer (`app/adapters`)**: Implements interfaces defined in the domain to interact with external systems.
    *   *Persistence*: PostgreSQL adapter using `SQLAlchemy` (async).
    *   *OCR*: Tesseract OCR adapter for text extraction.
    *   *NLP*: Spacy adapter for extracting medical entities (medications, vaccinations, etc.).
*   **API Layer (`app/api`)**: Handles HTTP requests and responses. It depends only on the Domain layer.
    *   *DTOs*: Pydantic models for data validation and serialization.
*   **Core (`app/core`)**: Configuration and dependency injection wiring.
*   **Testing (`tests/`)**: Refer to [backend/testing_approach.md](./backend/testing_approach.md) for the detailed behavioral testing strategy.

### Frontend Structure (`/frontend`)
The frontend is a **React** application built with **Vite** and **TypeScript**.

*   **Component-Based**: Modular components (`MedicalRecordEditor`, `FileUpload`) for reusability.
*   **Styling**: **Tailwind CSS** for utility-first, responsive styling.
*   **State Management**: React Hooks for local state management and API integration.

### Infrastructure (`/helm`)
The application is containerized and orchestrated using **Kubernetes** and **Helm**.

*   **Microservices**: Separate containers for Backend, Frontend, and Database.
*   **Helm Charts**: Templated deployment configuration allowing for environment-specific values (e.g., `dev.yaml`).
*   **Database**: PostgreSQL deployed as a stateful service within the cluster.

## 2. Technical Decisions

*   **FastAPI**: Chosen for its high performance, native async support, and automatic OpenAPI documentation generation. Its type-hinting system ensures code quality and reduces runtime errors.
*   **Clean Architecture**: Adopted to allow swapping out implementations (e.g., changing the OCR engine or Database) without affecting business logic. It also simplifies integration testing.
*   **Kubernetes & Helm**: "DevOps-first" mindset. Using K8s ensures the application is ready for cloud-native deployment and scaling.
*   **Alembic**: Used for database migrations to track schema changes version control.

## 3. Assumptions

*   **OCR Environment**: It is assumed that the host or container has Tesseract binaries installed (handled via Dockerfile).
*   **Single User**: The current iteration assumes a single-tenant environment (no authentication/authorization implemented yet).
*   **Deployment**: The primary deployment target for review is a local Kubernetes cluster (Minikube).

## 4. Development Best Practices

*   **Testing**:
    *   **E2E Tests**: `pytest` suite testing the full flow from API to Database.
    *   **Fixtures**: Reusable test data setup.
*   **Dependency Management**:
    *   `pyproject.toml` for Python backend.
    *   `package.json` for Node frontend.
*   **Automation**:
    *   `setup_and_run.sh`: A zero-config script to bootstrap the entire environment (install dependencies, build images, deploy to Minikube).
*   **Linting & Formatting**: Code follows standard PEP8 (Python) and ESLint (TypeScript) conventions.

## 5. Installation and Execution

For detailed step-by-step instructions, please refer to the [README.md](./README.md).

**Quick Start (macOS):**
```bash
./setup_and_run.sh
```
This script will:
1.  Install necessary tools (Docker, Minikube, Helm).
2.  Start the Kubernetes cluster.
3.  Build Docker images.
4.  Deploy the application using Helm.

## 6. Iterative Delivery Strategy

The problem of extracting structured data from heterogeneous medical records is complex. A "perfect" solution (e.g., custom-trained LLMs for every format) is resource-intensive and slow to market. Our strategy focuses on **delivering value early** while building a foundation for evolution.

It seems reasonable to assume that **80% of the medical records come from 20% of the clinics** (Pareto Principle), however this is something that should be verified and driven by business metrics. Anyhow, based on that assupmtion, the high level phases of this project might be:
*   **Phase 1 (Current)**: Implement robust heuristics and Regex-based extractors optimized for the most common formats. This reduces the manual workload for the veterinary team immediately.
*   **Phase 2 (Data-Driven)**: Collect metrics on input formats and extraction success rates. Identify the "long tail" of edge cases.
*   **Phase 3 (AI Integration)**: As the dataset grows, integrate more advanced NLP or LLM solutions for the complex 20% of cases that heuristics miss.

### Architecture for Adaptability
This challenge focuses on setting the **foundations**. The Clean Architecture ensures that the *extraction logic* is an implementation detail (an Adapter).
*   We can swap a `RegexMedicalRecordExtractor` for an `OpenAIMedicalRecordExtractor` without changing the Domain logic or the API contracts.
*   This allows the engineering team to iterate on accuracy without rewriting the application.

## 7. Future Improvements & Next Steps

If this project were to evolve into a production system, the following steps would be prioritized:

*  **Observability**: OpenTelemetry, Prometheus/Grafana, ELK stack or whatever observability system the company has to integrate traces, logs and metrics.
*  **Frontend Testing Strategy**: Refer to [frontend/testing_approach.md](./frontend/testing_approach.md) for the detailed behavioral testing strategy.
*  **Enhanced OCR/NLP**: Integrate with cloud-based AI services (e.g., AWS Textract, OpenAI) for higher accuracy in handwriting recognition and entity extraction.
*  **CI/CD Pipeline**: Set up GitHub Actions to run tests, linting, and auto-deploy to a staging cluster on push.
*  **Cloud Deployment**: Create Terraform scripts to provision managed infrastructure (EKS/GKE, RDS) instead of local Minikube.
*  **Authentication & Authorization**: Implement OAuth2/JWT to secure endpoints and manage user sessions.

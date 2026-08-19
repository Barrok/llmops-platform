# ADR-003: Docker Compose Development Environment

## Status

Accepted

## Context

The application consists of multiple runtime components, including the FastAPI application and the Ollama LLM runtime.

Running these components independently can lead to inconsistent environments and networking configurations.

## Decision

Use Docker Compose as the local multi-container development environment.

The initial Compose setup contains:

- FastAPI application
- Ollama LLM runtime

```mermaid
flowchart LR
    API[llmops-api] --> Ollama[llmops-ollama]
```

## Rationale

- Reproducible local environment
- Isolated services
- Explicit service-to-service networking
- Simple service lifecycle management
- Easy local setup

## Consequences

### Positive

- API and Ollama run as isolated services.
- Service communication is reproducible.
- The complete local environment can be started with a single command.
- The architecture can later be adapted to a more advanced orchestration platform.

### Negative

- Docker is required for the containerized development environment.
- GPU configuration introduces platform-specific requirements.

## Scope

Docker Compose is currently used as the local development environment.

It is not considered the final production orchestration platform.
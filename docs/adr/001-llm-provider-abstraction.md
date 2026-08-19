# ADR-001: LLM Provider Abstraction

## Status

Accepted

## Context

The AgentService needs to communicate with a language model.

Directly coupling the AgentService to a specific LLM provider would make the application dependent on that provider and make future provider changes more difficult.

## Decision

Introduce an `LLMClient` abstraction.

The AgentService communicates with the `LLMClient` interface instead of directly depending on Ollama.

```mermaid
flowchart LR
    AgentService --> LLMClient
    LLMClient --> OllamaClient
    OllamaClient --> Ollama
```

## Consequences

### Positive

- AgentService is independent of the specific LLM provider.
- LLM providers can be replaced without modifying the AgentService.
- LLM interactions can be mocked during testing.
- Provider-specific implementation details remain isolated.

### Negative

- Adds an additional abstraction layer.
- Provider-specific features may require extending the common interface.
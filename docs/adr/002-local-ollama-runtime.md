# ADR-002: Local Ollama Runtime

## Status

Accepted

## Context

The initial implementation requires a local LLM runtime for development and testing.

The project should be runnable without depending on a paid external LLM API.

## Decision

Use Ollama as the local LLM runtime.

The initial model is Qwen3:8b.

## Rationale

- Local model execution
- No external LLM API dependency
- No API usage costs during development
- Local GPU acceleration
- Simple local model management

## Consequences

### Positive

- The complete Agent Core can run locally.
- Development does not depend on an external LLM service.
- The LLM provider remains replaceable through the `LLMClient` abstraction.

### Negative

- Local hardware is required.
- Model performance depends on available hardware.
- Ollama becomes a local runtime dependency.

## Scope

This decision applies to the local development environment and initial implementation.

It does not define the final production LLM deployment strategy.
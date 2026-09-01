# Embedding Strategy

## Provider

The RAG pipeline uses local embedding generation through Ollama.

The application accesses the embedding provider through the `EmbeddingClient`
abstraction, keeping the embedding service independent from the concrete
provider implementation.

Current provider:

```text
EmbeddingService
      ↓
EmbeddingClient
      ↓
Ollama
      ↓
nomic-embed-text
```
## Vector dimensions

The current embedding model produces vectors with:

```vector_size = 768```

The vector size must match the Qdrant collection configuration.

## Rationale

Local embeddings allow the RAG pipeline to operate without external API
dependencies or cloud services.

The provider abstraction allows the embedding model or backend to be
replaced without changing application-level embedding logic.

## Future Optimization

The current embedding model is a baseline rather than a final production
choice.

Embedding model quality and retrieval performance will be evaluated during
future RAG evaluation stages.
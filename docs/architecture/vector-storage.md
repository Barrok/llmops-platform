# Vector storage

## Storage

The RAG pipeline uses Qdrant as its vector database.

Generated embeddings are persisted together with the document information
required to reconstruct retrieved chunks.

```text
EmbeddedChunk
      ↓
QdrantVectorStore
      ↓
Qdrant
```

## Vector Configuration

The current collection configuration uses:

```
vector_size = 768
distance = COSINE
```

## Stored Data

Each vector point contains:

- embedding vector
- document content
- source
- metadata

Point identifiers are generated deterministically from the document source
and chunk content.

## Abstraction

Application code accesses vector storage through the VectorStore
abstraction.
Retrieval is exposed through the ```Retriever``` abstraction.
The concrete ```QdrantVectorStore``` implements both interfaces.
This keeps Qdrant-specific implementation details outside the application
services.

## Rationale

Qdrant provides local persistent vector storage and similarity search
without introducing an external cloud dependency.

## Future Optimization

The current collection configuration is a baseline.

Indexing strategy, distance configuration and storage configuration may be
revisited as the retrieval workload and evaluation dataset grow.
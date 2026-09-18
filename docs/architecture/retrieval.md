# Retrieval Strategy

## Query Flow

At query time, the user query is converted into an embedding and compared
against vectors stored in Qdrant.

```text
User Query
    ↓
EmbeddingService
    ↓
Query Embedding
    ↓
Retriever
    ↓
QdrantVectorStore
    ↓
DocumentChunk[]
```

## Retrieval Service

```RetrievalService``` coordinates query embedding and vector retrieval.

The service depends on the ```Retriever``` abstraction rather than directly
depending on Qdrant.

This keeps retrieval logic independent from the concrete vector database.

## Similarity Search

The current implementation uses cosine similarity to identify the most
relevant document chunks.
The number of retrieved chunks is controlled by the limit parameter.

The current default is:

```limit = 5```

## Evaluation

Retrieval quality is evaluated using a controlled evaluation dataset and
Recall@K.

The current baseline is:

```Recall@1 = 1.0```

across three evaluation cases.

## Future Optimization

The retrieval configuration is considered a baseline.

Future evaluation may investigate:

- retrieval depth
- similarity thresholds
- embedding models
- chunking parameters
- reranking
- hybrid retrieval
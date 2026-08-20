# Chunking Strategy

## Strategy

The RAG pipeline uses recursive character-based text splitting.

The splitter attempts to preserve larger text structures before falling back to smaller separators.

The conceptual splitting order is:

```text
paragraph
    ↓
line
    ↓
sentence
    ↓
word
    ↓
character
```

## Baseline Parameters

```text
chunk_size = 1000
chunk_overlap = 200
```

These values provide the initial baseline for the RAG pipeline and may be adjusted based on evaluation results.

## Rationale

The strategy aims to preserve semantic context while keeping chunks small enough for efficient embedding and retrieval.

Chunk overlap helps preserve context between neighboring chunks and reduces the risk of losing information at chunk boundaries.

## Future Optimization

Chunk size and overlap are not considered final production values.

They will be evaluated and potentially adjusted during the RAG evaluation stage.
# RAG Pipeline

## Overview

The RAG pipeline consists of two separate flows:

- document indexing
- query-time retrieval

The flows share the embedding and vector storage layers but have different
responsibilities.

## Indexing Flow

Documents are processed and persisted as vector representations.

```text
Document
    ↓
Document Ingestion
    ↓
Document Chunking
    ↓
EmbeddingService
    ↓
EmbeddedChunk
    ↓
QdrantVectorStore
    ↓
Qdrant
```
The indexing flow is responsible for preparing document data for later
retrieval.

## Query Flow

At query time, the user query is embedded and used to retrieve relevant
document chunks

```text
User Query
    ↓
EmbeddingService
    ↓
Retriever
    ↓
QdrantVectorStore
    ↓
DocumentChunk[]
    ↓
ContextBuilder
    ↓
LLM Prompt
    ↓
   LLM
```

## Context Injection

Retrieved chunks are formatted by ContextBuilder and injected into the
prompt sent to the LLM.

The retrieved context is request-scoped and is not stored in the
conversation history.

The conversation history contains only:

- system messages
- user messages
- assistant messages

## Architecture

The application depends on abstractions at the boundaries:
```
Application
    │
    ├── EmbeddingClient
    ├── Retriever
    └── VectorStore
            │
            ▼
    Infrastructure
    ├── Ollama
    └── Qdrant
```
This keeps infrastructure-specific implementations replaceable without
changing the core RAG orchestration.

## Evaluation

The current retrieval baseline is evaluated using Recall@K.

The initial evaluation achieved:

```Recall@1 = 1.0```

across three controlled evaluation cases.

An end-to-end integration test verifies the complete flow from document
indexing through retrieval, context construction and LLM generation.

## Current Limitations

The current RAG pipeline is synchronous and locally executed.

It does not yet provide:

- asynchronous indexing
- background workers
- reranking
- hybrid retrieval
- advanced retrieval evaluation
- production observability
- distributed execution

These capabilities are planned for later milestones.
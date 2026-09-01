# Status
Project under active development.

---

# LLMOps Platform

Production-oriented LLM application platform built to demonstrate MLOps, LLMOps, DevOps and cloud-native engineering practices.

The goal of this project is to design and implement a scalable AI system using modern production patterns:
- containerization,
- infrastructure as code,
- CI/CD automation,
- observability,
- security hardening,
- asynchronous processing.

The project focuses on engineering practices required to operate AI systems reliably in production environments.

---

# Project Goals

The platform aims to demonstrate:

- designing scalable AI application architecture,
- building RAG-based systems,
- deploying services using containers and Kubernetes,
- implementing automated delivery pipelines,
- monitoring application health and performance,
- securing AI workloads against common threats.

---

## High-Level Architecture

The current system is implemented as a modular monolith following Clean Architecture principles.

The application is organized into independent domain modules with clear
boundaries and dependency inversion. This structure allows individual
components to be extracted into separate services as the platform evolves.

### Current architecture:

```mermaid
flowchart LR

User --> API

API --> Agent

Agent --> LLM
Agent --> Retrieval

Retrieval --> Embeddings
Embeddings --> VectorDB
```

---

# Planned Technology Stack

## Currently Implemented

### Backend
- Python
- FastAPI
- Pydantic

### AI / LLM
- RAG architecture
- Ollama
- Qwen3:8b
- nomic-embed-text
- Embeddings
- Vector search

### Data Layer
- Qdrant

### Infrastructure
- Docker
- Docker Compose

### Testing
- Pytest

## Planned

### Data Layer
- Redis

### Messaging
- RabbitMQ

### Infrastructure
- Kubernetes
- Helm
- Terraform

### CI/CD
- GitLab CI

### Observability
- Prometheus
- Grafana
- OpenTelemetry

### Testing
- Locust / Gatling

### Security
- Kubernetes Secrets
- Sealed Secrets
- JWT authentication
- RBAC
- Network Policies
- Threat modeling
- Prompt injection testing

---

# Project Roadmap

## Phase 1 — Foundation
- repository setup
- development environment
- project structure
- documentation baseline

## Phase 2 — Application Core
- API service
- RAG pipeline
- document ingestion
- vector search

## Phase 3 — Production Architecture
Current phase.
- asynchronous workers
- message queues
- caching
- service separation

## Phase 4 — Cloud Native Deployment
- Docker
- Kubernetes
- Helm
- Terraform

## Phase 5 — Operations
- monitoring
- tracing
- load testing
- security validation

---

# Local Development

Coming soon.

---

# Documentation

Architecture decisions and technical documentation are available in:
```text
docs/
├── architecture/
├── adr/
└── development/
```

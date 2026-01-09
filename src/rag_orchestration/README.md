# RAG Orchestration Module

## Purpose

This module manages retrieval-augmented generation workflows, combining vector search with LLM-powered responses.

## Responsibilities

- **Query Routing**: Direct queries to appropriate retrieval strategies
- **Hybrid Retrieval**: Combine vector search (pgvector) with keyword search (PostgreSQL full-text)
- **Context Assembly**: Gather relevant document chunks for LLM context
- **LLM Integration**: Interface with OpenAI, Anthropic, or local models
- **Response Generation**: Produce answers with citations and source attribution

## Future Features

- LangChain integration for flexible orchestration
- LlamaIndex for advanced indexing strategies
- LangGraph for agentic workflows (multi-step reasoning)
- Custom retrieval contract layer (framework-agnostic interface)
- GraphRAG for relationship-based queries across documents

## Architecture

```
rag_orchestration/
├── __init__.py
├── retrievers/       # Hybrid retrieval strategies
├── llm/              # LLM client wrappers (OpenAI, Anthropic)
├── prompts/          # Prompt templates with version control
├── agents/           # LangGraph agentic workflows
└── pipelines/        # End-to-end RAG pipelines
```

## Status

🚧 **Scaffolded** - Implementation planned for future feature development.

Refer to `/docs/chatgpt-2.md` for RAG architecture and best practices.

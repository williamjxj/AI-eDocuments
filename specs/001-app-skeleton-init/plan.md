# Implementation Plan: AgenticOmni Application Skeleton

**Branch**: `001-app-skeleton-init` | **Date**: January 9, 2026 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-app-skeleton-init/spec.md`

## Summary

This plan implements a production-ready skeleton for the AgenticOmni AI document intelligence platform. The skeleton establishes a modular ETL-to-RAG pipeline architecture with seven core modules (ingestion, storage, RAG orchestration, evaluation, security, API, and frontend). The implementation focuses on creating directory structure, dependency management, configuration framework, database schema with PostgreSQL + pgvector, FastAPI server scaffold, Docker development environment, testing framework, and Next.js frontend shell. This foundation enables parallel development of document processing features while enforcing enterprise best practices from day one.

## Technical Context

**Language/Version**: Python 3.12+ (backend), TypeScript 5.x (frontend), Node.js 18+  
**Primary Dependencies**: FastAPI, SQLAlchemy, Alembic, LangChain, LlamaIndex, psycopg2-binary, pgvector, Next.js, Tailwind CSS, shadcn/ui  
**Storage**: PostgreSQL 14+ with pgvector extension (1536-dimension vectors), Redis (caching)  
**Testing**: pytest with pytest-cov, pytest-mock for backend; Jest/React Testing Library for frontend  
**Target Platform**: Docker containers on Linux/macOS/WSL2, development-first with production-ready patterns  
**Project Type**: Web application (separate backend API + frontend SPA)  
**Performance Goals**: 
- Health check endpoint responds within 1 second
- Database migrations complete within 5 seconds
- Full environment startup within 2 minutes
- Development setup completes within 15 minutes

**Constraints**: 
- Vector embeddings fixed at 1536 dimensions (OpenAI text-embedding-3-small standard)
- Row-level multi-tenancy isolation (shared schema, tenant_id filtering)
- JSON structured logging mandatory for all modules
- Python 3.12+ required for latest type hints and performance improvements
- Docker Compose for local development (no cloud dependencies)

**Scale/Scope**: 
- 6 database entities with migration framework
- 7 backend modules with clear separation of concerns
- 1 health check API endpoint (baseline for future expansion)
- Complete development environment with hot-reload support
- Foundation for multi-tenant document AI platform

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles for AgenticOmni

#### I. Modular Architecture (NON-NEGOTIABLE)
- **Separation of Concerns**: Each module (`ingestion_parsing`, `storage_indexing`, `rag_orchestration`, `eval_harness`, `security_auth`, `api`, `shared`) must have a single, well-defined responsibility
- **Independent Testability**: Every module must be testable in isolation with clearly defined interfaces
- **No Circular Dependencies**: Modules can only depend on `shared` and must not create circular import chains
- **Status**: ✅ PASS - Spec defines 7 distinct modules with clear boundaries

#### II. Type Safety & Documentation (NON-NEGOTIABLE)
- **Type Annotations**: All functions, methods, and class attributes must have complete type hints following PEP 484
- **Docstrings**: All public APIs must have Google-style docstrings (PEP 257)
- **Validation**: mypy type checking must pass with zero errors
- **Status**: ✅ PASS - FR-015 mandates type hints and docstrings; SC-009 requires mypy compliance

#### III. Test-First Development (NON-NEGOTIABLE)
- **pytest Standard**: All tests use pytest framework exclusively (no unittest)
- **Coverage Target**: Minimum 80% code coverage for all skeleton code
- **Test Structure**: Tests mirror source structure (`/tests` matches `/src`)
- **Fixtures**: Reusable fixtures for database, API client, mocks
- **Status**: ✅ PASS - FR-009 and FR-018 mandate pytest with fixtures; SC-005 requires 100% test pass rate

#### IV. Configuration Management
- **Environment-Based**: All configuration via environment variables (no hardcoded secrets)
- **Validation on Startup**: Missing or invalid config must fail fast with clear error messages
- **Multi-Environment**: Support for development, testing, staging, production
- **Status**: ✅ PASS - FR-004, FR-014, and SC-011 define comprehensive config management

#### V. Data Integrity & Multi-Tenancy
- **Row-Level Isolation**: All tenant-scoped entities must include non-null tenant_id foreign key
- **Migration Discipline**: All schema changes via Alembic migrations (no manual SQL)
- **Enums for State**: Use database enums for ProcessingJob status values
- **Vector Consistency**: All embedding vectors must be exactly 1536 dimensions
- **Status**: ✅ PASS - FR-005a/b/c define strict data constraints; clarifications specify isolation strategy

#### VI. Observability
- **Structured Logging**: JSON format with standard fields (timestamp, log_level, module, message, tenant_id, request_id, error)
- **Request Tracing**: All API calls must have unique request_id propagated through logs
- **Error Context**: All exceptions must include sufficient context for debugging
- **Status**: ✅ PASS - FR-017 mandates JSON structured logging with standard fields

#### VII. Developer Experience
- **Fast Setup**: Complete environment setup in under 15 minutes
- **Single Command Start**: `docker-compose up` starts all services
- **Hot Reload**: Backend and frontend support code changes without restart
- **Clear Documentation**: README sufficient for new developer onboarding
- **Status**: ✅ PASS - SC-001 and SC-012 define strict timing requirements

### Gate Evaluation

| Gate | Requirement | Status | Evidence |
|------|-------------|--------|----------|
| **Architecture** | Modular design with clear boundaries | ✅ PASS | 7 modules defined with specific responsibilities (FR-001) |
| **Type Safety** | Complete type annotations and docstrings | ✅ PASS | FR-015 mandates PEP 257 docstrings and type hints |
| **Testing** | pytest framework with fixtures | ✅ PASS | FR-009, FR-018, SC-005 define complete testing strategy |
| **Configuration** | Environment-based with validation | ✅ PASS | FR-004, FR-014 define env var management |
| **Data Model** | Strict schemas with migrations | ✅ PASS | FR-005a/b/c + FR-006 define Alembic-based migrations |
| **Observability** | JSON structured logging | ✅ PASS | FR-017 specifies JSON format with required fields |
| **DX** | Fast setup and clear docs | ✅ PASS | SC-001, SC-010, SC-012 define measurable DX goals |

**Overall Constitution Check**: ✅ **PASS** - All gates satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-app-skeleton-init/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output - technology decisions and best practices
├── data-model.md        # Phase 1 output - database schema and entity relationships
├── quickstart.md        # Phase 1 output - developer setup guide
├── contracts/           # Phase 1 output - API specifications
│   └── health-api.yaml  # OpenAPI spec for health check endpoint
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Backend (Python FastAPI + SQLAlchemy)
src/
├── __init__.py
├── ingestion_parsing/          # Document upload, OCR, multimedia processing (scaffolded)
│   ├── __init__.py
│   └── README.md               # Module purpose and future features
├── storage_indexing/           # Database models, repositories, migrations
│   ├── __init__.py
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py             # Base model class
│   │   ├── tenant.py           # Tenant entity
│   │   ├── user.py             # User entity
│   │   ├── document.py         # Document entity
│   │   ├── document_chunk.py   # DocumentChunk entity with pgvector
│   │   ├── permission.py       # Permission entity
│   │   └── processing_job.py   # ProcessingJob entity with state enum
│   ├── repositories/           # Data access layer (scaffolded)
│   │   └── __init__.py
│   └── migrations/             # Alembic migrations
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
│           └── 001_initial_schema.py
├── rag_orchestration/          # LangChain/LlamaIndex integration (scaffolded)
│   ├── __init__.py
│   └── README.md
├── eval_harness/               # Metrics and evaluation (scaffolded)
│   ├── __init__.py
│   └── README.md
├── security_auth/              # RBAC, tenant isolation utilities (scaffolded)
│   ├── __init__.py
│   └── README.md
├── api/                        # FastAPI application
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization, CORS, middleware
│   ├── dependencies.py         # Dependency injection (DB session, config)
│   ├── middleware/             # Logging, request ID, error handling
│   │   ├── __init__.py
│   │   ├── logging.py          # JSON structured logging middleware
│   │   └── error_handler.py    # Global exception handler
│   └── routes/                 # API endpoints organized by domain
│       ├── __init__.py
│       └── health.py           # Health check endpoint
└── shared/                     # Common utilities, base classes
    ├── __init__.py
    ├── config.py               # Configuration loading and validation
    ├── logging_config.py       # JSON logging setup
    └── exceptions.py           # Custom exception classes

# Configuration
config/
├── __init__.py
└── settings.py                 # Pydantic settings model

# Tests (mirrors src/ structure)
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures (DB, API client, mocks)
├── unit/
│   ├── __init__.py
│   ├── test_config.py          # Configuration validation tests
│   └── test_models.py          # ORM model tests
├── integration/
│   ├── __init__.py
│   ├── test_database.py        # Database connection and migration tests
│   └── test_api.py             # API endpoint tests
└── fixtures/
    ├── __init__.py
    └── sample_data.py          # Test data factories

# Scripts
scripts/
├── setup_db.sh                 # Initialize database and run migrations
├── run_dev.sh                  # Start development servers
└── validate_env.sh             # Check environment variable configuration

# Frontend (Next.js + TypeScript + Tailwind)
frontend/
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
├── postcss.config.js
├── .eslintrc.json
├── app/                        # Next.js App Router
│   ├── layout.tsx              # Root layout with providers
│   ├── page.tsx                # Home page
│   └── globals.css             # Tailwind imports
├── components/                 # React components
│   ├── ui/                     # shadcn/ui components
│   └── layout/                 # Layout components (header, footer)
├── lib/                        # Utilities and helpers
│   ├── api-client.ts           # Backend API client
│   └── utils.ts                # Common utilities
├── public/                     # Static assets
│   └── favicon.ico
└── __tests__/                  # Frontend tests
    └── components/

# Root configuration files
.env.example                    # Documented environment variables template
.gitignore                      # Python, Node.js, IDE, secrets
README.md                       # Project overview, setup, architecture
pyproject.toml                  # Python project config, dependencies, tool settings
alembic.ini                     # Alembic configuration
docker-compose.yml              # PostgreSQL, pgvector, Redis services
Dockerfile                      # Optional: API container definition
```

**Structure Decision**: 

This implementation uses **Option 2: Web Application** structure with separate `src/` (backend) and `frontend/` directories. This separation is chosen because:

1. **Clear Boundaries**: Backend (Python/FastAPI) and frontend (Next.js/TypeScript) have different toolchains, dependencies, and deployment requirements
2. **Independent Development**: Frontend and backend teams can work in parallel once API contracts are defined
3. **Scalability**: Each can scale independently (e.g., multiple API instances, static frontend on CDN)
4. **Tooling**: Each ecosystem has its own linting, testing, and build tools that work best in isolated environments

The backend follows a modular architecture with 7 domain-specific modules under `src/`, enabling future feature development without monolithic entanglement. The `shared/` module provides common utilities while maintaining the dependency hierarchy (modules depend on `shared`, not on each other).

## Complexity Tracking

No constitution violations detected. All requirements align with established principles.

| Principle | Justification |
|-----------|---------------|
| 7 Modules | Each module has a distinct domain purpose; necessary for ETL-to-RAG pipeline separation |
| Separate Frontend/Backend | Different languages, toolchains, and deployment models justify physical separation |
| Repository Pattern (deferred) | Not implemented in skeleton; will be evaluated when implementing actual data access logic |

---

## Phase 0: Research & Technology Decisions

See [research.md](./research.md) for detailed technology evaluations and decisions.

## Phase 1: Design Artifacts

- **Data Model**: See [data-model.md](./data-model.md) for complete entity schemas and relationships
- **API Contracts**: See [contracts/](./contracts/) for OpenAPI specifications
- **Quickstart Guide**: See [quickstart.md](./quickstart.md) for developer onboarding

## Phase 2: Task Breakdown

Phase 2 (task generation) is handled by the `/speckit.tasks` command and will produce `tasks.md`.

---

**Plan Status**: ✅ Constitution gates passed. Ready for Phase 0 research.

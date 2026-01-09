# Feature Specification: AgenticOmni Application Skeleton

**Feature Branch**: `001-app-skeleton-init`  
**Created**: January 9, 2026  
**Status**: Draft  
**Input**: User description: "Initialize AgenticOmni app skeleton with ETL-to-RAG pipeline architecture"

## Clarifications

### Session 2026-01-09

- Q: What are the valid status values and state transitions for the ProcessingJob entity? → A: Comprehensive state machine with states: pending → processing → completed/failed/cancelled (with retrying state for automatic retries)
- Q: What is the vector dimensionality for the DocumentChunk embedding_vector field? → A: 1536 dimensions (OpenAI text-embedding-3-small standard)
- Q: What is the multi-tenancy isolation strategy? → A: Row-level with tenant_id in shared schema (all tenants share tables, filtered by tenant_id)
- Q: What logging format should be used for structured logging? → A: JSON structured logging (machine-parseable, standard for cloud/container environments)
- Q: What database migration tool should be used? → A: Alembic with auto-generation from SQLAlchemy models (industry standard, excellent tooling)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Core Project Structure Initialization (Priority: P1)

As a developer, I need a well-organized project directory structure that separates concerns into logical modules (ingestion, storage, RAG orchestration, security, API, and frontend) so that the codebase is maintainable and scalable from day one.

**Why this priority**: This is the foundation upon which all other features will be built. Without a clear, modular structure, the project will become difficult to maintain and extend. This structure follows enterprise best practices and enables parallel development of different modules.

**Independent Test**: Can be fully tested by verifying that all required directories exist with proper structure, that configuration files are present and valid, and that basic dependency management (requirements.txt, pyproject.toml) is in place. Delivers immediate value by providing a working development environment.

**Acceptance Scenarios**:

1. **Given** an empty project repository, **When** the skeleton is initialized, **Then** the following top-level directories exist: `/src`, `/tests`, `/docs`, `/config`, `/scripts`, `/frontend`
2. **Given** the project structure is created, **When** examining the `/src` directory, **Then** it contains subdirectories for: `ingestion_parsing`, `storage_indexing`, `rag_orchestration`, `eval_harness`, `security_auth`, `api`, `shared`
3. **Given** the directory structure exists, **When** checking each module directory, **Then** each contains an `__init__.py` file to mark it as a Python package
4. **Given** the project is initialized, **When** examining the root directory, **Then** it contains: `.env.example`, `.gitignore`, `README.md`, `pyproject.toml` or `requirements.txt`, and `docker-compose.yml`

---

### User Story 2 - Dependency Management Setup (Priority: P1)

As a developer, I need proper dependency management configured with all required libraries for ETL processing, RAG orchestration, vector storage, and API development so that I can immediately start building features without wrestling with environment setup.

**Why this priority**: Without proper dependency management, development cannot proceed. This ensures all team members and deployment environments have consistent, reproducible setups. It's a prerequisite for any actual feature development.

**Independent Test**: Can be tested by running dependency installation commands and verifying all packages install without conflicts. Delivers value by providing a working Python environment with all required libraries for document AI development.

**Acceptance Scenarios**:

1. **Given** the dependency file exists, **When** installing dependencies, **Then** the following core libraries are available: `langchain`, `llama-index`, `psycopg2-binary`, `pgvector`, `sqlalchemy`, `alembic`, `fastapi`, `uvicorn`
2. **Given** the dependency file exists, **When** installing dependencies, **Then** document processing libraries are available: `docling` (or document parsers), `python-multipart`, `pillow`, `pytesseract`, `opencv-python`
3. **Given** the dependency file exists, **When** installing dependencies, **Then** testing and code quality libraries are available: `pytest`, `pytest-cov`, `pytest-mock`, `ruff`, `mypy`
4. **Given** dependencies are installed, **When** running `pytest --version` and `ruff --version`, **Then** both commands execute successfully without errors

---

### User Story 3 - Configuration Management Foundation (Priority: P1)

As a developer or operator, I need centralized configuration management using environment variables and config files so that I can easily switch between development, staging, and production environments without modifying code.

**Why this priority**: Configuration management is critical for security (keeping secrets out of code) and operational flexibility. This enables the application to run in different environments (local dev, Docker, cloud) with minimal changes.

**Independent Test**: Can be tested by setting environment variables, running a simple config loader, and verifying values are correctly loaded. Delivers value by establishing security best practices and multi-environment support from the start.

**Acceptance Scenarios**:

1. **Given** the project root, **When** checking for configuration files, **Then** a `.env.example` file exists with documented placeholders for all required environment variables
2. **Given** the `.env.example` file, **When** examining its contents, **Then** it includes sections for: database connection, vector store settings, LLM API keys, authentication secrets, and logging configuration
3. **Given** the `/config` directory exists, **When** examining its contents, **Then** it contains Python configuration modules that load and validate environment variables
4. **Given** configuration is set up, **When** a module attempts to access undefined configuration, **Then** it raises a clear error with guidance on which environment variable is missing

---

### User Story 4 - Database Schema Foundation (Priority: P2)

As a developer, I need initial database schema definitions and migration setup for storing document metadata, tenant information, and vector embeddings so that the storage layer is ready for ETL pipeline development.

**Why this priority**: The database schema is foundational for data storage and retrieval. Having it defined early prevents architectural issues later. However, it can be developed after the basic project structure is in place.

**Independent Test**: Can be tested by running database migrations against a test PostgreSQL instance and verifying all tables and indexes are created correctly. Delivers value by providing a working data persistence layer.

**Acceptance Scenarios**:

1. **Given** the `/src/storage_indexing` module, **When** examining the directory, **Then** it contains subdirectories or files for: `models/`, `repositories/`, and `migrations/`
2. **Given** database models are defined, **When** examining the models, **Then** they include entities for: `Tenant`, `User`, `Document`, `DocumentChunk`, `Permission`, `ProcessingJob`
3. **Given** PostgreSQL with pgvector is available, **When** running the initial migration, **Then** all tables are created with appropriate indexes and the pgvector extension is enabled
4. **Given** database models exist, **When** examining the `DocumentChunk` model, **Then** it includes a vector field for storing embeddings and appropriate indexing for similarity search

---

### User Story 5 - API Server Scaffold (Priority: P2)

As a developer, I need a basic FastAPI application structure with health check endpoints, proper CORS configuration, and API documentation so that frontend development and API integration can begin in parallel.

**Why this priority**: The API layer is the interface between frontend and backend. Having the basic server structure allows parallel development of frontend and backend features. It's not as critical as the core structure but enables broader team productivity.

**Independent Test**: Can be tested by starting the FastAPI server and accessing the health check endpoint and auto-generated API documentation at `/docs`. Delivers value by providing a working API server ready for endpoint development.

**Acceptance Scenarios**:

1. **Given** the `/src/api` module exists, **When** examining its structure, **Then** it contains: `main.py` (app entry point), `routes/`, `dependencies.py`, and `middleware/`
2. **Given** the FastAPI app is defined, **When** starting the server with `uvicorn`, **Then** the server starts successfully and responds to requests on the configured port
3. **Given** the API server is running, **When** accessing `/health` or `/api/v1/health`, **Then** it returns a 200 status with basic system information
4. **Given** the API server is running, **When** accessing `/docs` or `/api/v1/docs`, **Then** the auto-generated Swagger UI documentation is accessible

---

### User Story 6 - Docker Development Environment (Priority: P2)

As a developer, I need Docker Compose configuration that spins up PostgreSQL with pgvector extension and the API server so that I can develop and test locally without manual infrastructure setup.

**Why this priority**: Docker containerization ensures consistent development environments across all team members and simplifies onboarding. While important, it can be added after the basic application structure is in place.

**Independent Test**: Can be tested by running `docker-compose up` and verifying all services start successfully and can communicate. Delivers value by eliminating "works on my machine" problems and streamlining developer onboarding.

**Acceptance Scenarios**:

1. **Given** a `docker-compose.yml` file in the project root, **When** examining its contents, **Then** it defines services for: PostgreSQL with pgvector, Redis (for caching), and optional nginx/reverse proxy
2. **Given** Docker Compose is configured, **When** running `docker-compose up -d`, **Then** all services start without errors and health checks pass
3. **Given** the PostgreSQL container is running, **When** connecting to it, **Then** the pgvector extension is installed and functional
4. **Given** all containers are running, **When** the API server attempts to connect to PostgreSQL, **Then** the connection succeeds and the application can perform database operations

---

### User Story 7 - Testing Framework Setup (Priority: P3)

As a developer, I need a testing framework configured with pytest, test directory structure, and example tests so that test-driven development practices can be followed from the start.

**Why this priority**: Testing is essential for code quality, but the framework can be set up slightly later as actual features are being developed. Having example tests and configuration helps establish testing culture early.

**Independent Test**: Can be tested by running `pytest` and verifying it discovers and runs all tests successfully. Delivers value by establishing quality assurance practices and providing confidence in code changes.

**Acceptance Scenarios**:

1. **Given** the `/tests` directory exists, **When** examining its structure, **Then** it mirrors the `/src` structure with test files for each module
2. **Given** pytest is configured, **When** examining `pyproject.toml` or `pytest.ini`, **Then** it includes configuration for: test discovery patterns, coverage settings, and pytest plugins
3. **Given** at least one test file exists, **When** running `pytest`, **Then** tests are discovered and executed successfully with a coverage report generated
4. **Given** the test framework is set up, **When** examining test files, **Then** they include fixtures for: database connections, test client for API, and mock objects for external services

---

### User Story 8 - Frontend Application Shell (Priority: P3)

As a developer, I need a Next.js frontend application initialized with Tailwind CSS, TypeScript, and basic routing structure so that UI development can begin once API endpoints are ready.

**Why this priority**: While important for the complete application, frontend development can start slightly later once API contracts are defined. The skeleton structure enables frontend developers to start building UI components.

**Independent Test**: Can be tested by running `npm run dev` and verifying the Next.js development server starts and the default page renders. Delivers value by providing a modern React-based frontend ready for component development.

**Acceptance Scenarios**:

1. **Given** the `/frontend` directory exists, **When** examining its structure, **Then** it follows Next.js App Router conventions with directories: `/app`, `/components`, `/lib`, `/public`, `/styles`
2. **Given** the frontend is initialized, **When** checking the root files, **Then** it contains: `package.json`, `tsconfig.json`, `tailwind.config.js`, `next.config.js`
3. **Given** dependencies are installed, **When** running `npm run dev`, **Then** the Next.js development server starts on the configured port
4. **Given** the frontend server is running, **When** accessing the root URL, **Then** a landing page renders successfully with basic styling applied

---

### Edge Cases

- What happens when required environment variables are missing or invalid during application startup?
- How does the system handle database connection failures during initialization?
- What happens if the PostgreSQL version doesn't support pgvector extension?
- How does Docker Compose handle port conflicts if default ports are already in use?
- What happens when dependency installation fails due to platform-specific issues (e.g., missing system libraries for OCR)?
- How does the system handle missing or incorrect Python version (below 3.12)?
- What happens when the frontend and backend API ports conflict?
- How does the system validate that all required database tables and extensions are properly set up before allowing operations?
- How does the system prevent cross-tenant data leakage when using row-level isolation with shared schema?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create a modular directory structure with separate modules for ingestion, storage, RAG orchestration, evaluation, security, and API
- **FR-002**: System MUST include Python package markers (`__init__.py`) in all module directories to enable proper imports
- **FR-003**: System MUST provide dependency management configuration (pyproject.toml or requirements.txt) with all required libraries for document AI, RAG, vector storage, and API development
- **FR-004**: System MUST include configuration management using environment variables with a documented `.env.example` template
- **FR-005**: System MUST define database models for core entities: Tenant, User, Document, DocumentChunk, Permission, ProcessingJob
- **FR-005a**: ProcessingJob model MUST enforce status values as an enumeration with exactly these states: pending, processing, completed, failed, cancelled, retrying
- **FR-005b**: DocumentChunk embedding_vector field MUST be defined as a pgvector type with exactly 1536 dimensions
- **FR-005c**: All tenant-scoped entities (User, Document, DocumentChunk, ProcessingJob) MUST include a tenant_id foreign key column with NOT NULL constraint for row-level isolation
- **FR-006**: System MUST provide database migration setup using Alembic for PostgreSQL with pgvector extension, including initial migration script and auto-generation configuration
- **FR-007**: System MUST include a FastAPI application scaffold with health check endpoint and CORS configuration
- **FR-008**: System MUST provide Docker Compose configuration for local development with PostgreSQL, pgvector, and Redis services
- **FR-009**: System MUST include pytest configuration with test directory structure mirroring the source structure
- **FR-010**: System MUST provide a Next.js frontend application with TypeScript, Tailwind CSS, and App Router structure
- **FR-011**: System MUST include comprehensive README.md with setup instructions, architecture overview, and development guidelines
- **FR-012**: System MUST provide `.gitignore` configured for Python, Node.js, environment files, and IDE-specific files
- **FR-013**: System MUST include scripts for common development tasks (database setup, running Alembic migrations, starting services)
- **FR-014**: Configuration module MUST validate required environment variables on application startup and provide clear error messages for missing values
- **FR-015**: Database models MUST include appropriate type hints and docstrings following PEP 257 conventions
- **FR-016**: API routes MUST be organized by domain (documents, users, tenants, queries) in separate router modules
- **FR-017**: System MUST include logging configuration with JSON structured logging for all modules, including standard fields: timestamp, log_level, module, message, tenant_id (when applicable), request_id (for API calls), and error details
- **FR-018**: System MUST provide example test files demonstrating fixture usage, mocking, and API testing patterns

### Key Entities *(mandatory)*

- **Tenant**: Represents an organization or client using the system. Stores tenant-specific configuration, subscription details, and serves as the root for multi-tenancy isolation. Isolation strategy: row-level security using tenant_id in shared database schema. Key attributes: tenant_id, name, domain, settings, created_at, status.

- **User**: Represents an individual user within a tenant. Stores authentication details, role assignments, and user preferences. Relationships: belongs to one Tenant, has many Permissions. Key attributes: user_id, tenant_id, email, hashed_password, role, full_name, last_login.

- **Document**: Represents an uploaded or ingested document. Stores metadata, processing status, and original file information. Relationships: belongs to one Tenant, has many DocumentChunks. Key attributes: document_id, tenant_id, filename, file_type, file_size, storage_path, upload_date, processing_status, metadata.

- **DocumentChunk**: Represents a processed segment of a document with its vector embedding. Used for RAG retrieval. Relationships: belongs to one Document. Key attributes: chunk_id, document_id, content_text, embedding_vector (pgvector type with 1536 dimensions), chunk_order, metadata, created_at.

- **Permission**: Represents access control rules defining which users can access which documents or perform which actions. Relationships: links User to Document or resource. Key attributes: permission_id, user_id, resource_type, resource_id, permission_level (read/write/admin).

- **ProcessingJob**: Represents a background task for document ingestion, OCR, embedding generation, or reprocessing. Tracks job status and error information. Key attributes: job_id, document_id, tenant_id, job_type, status (valid values: pending, processing, completed, failed, cancelled, retrying), started_at, completed_at, error_message, retry_count. State transitions: pending → processing → [completed | failed | retrying] → [completed | failed | cancelled].

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can complete initial project setup (clone repository, install dependencies, start services) in under 15 minutes on a clean development machine
- **SC-002**: Running `docker-compose up` successfully starts all required services (PostgreSQL with pgvector, Redis) with health checks passing within 30 seconds
- **SC-003**: The FastAPI health check endpoint responds with 200 status within 1 second of server startup
- **SC-004**: Database migrations complete successfully and create all required tables with proper indexes within 5 seconds
- **SC-005**: Running `pytest` discovers and executes all example tests with 100% pass rate
- **SC-006**: The Next.js development server starts and renders the default page within 10 seconds
- **SC-007**: Project structure validation (checking all required directories and files exist) completes with 100% compliance
- **SC-008**: All Python modules can be imported without errors, confirming proper package structure
- **SC-009**: Code quality checks (ruff linting, mypy type checking) pass with zero errors on all skeleton code
- **SC-010**: Documentation in README.md is sufficient for a new developer to understand the architecture and start contributing without additional guidance
- **SC-011**: Environment variable validation catches missing configuration and provides helpful error messages listing all missing variables
- **SC-012**: The complete development environment (backend + database + frontend) can be started with a single command and becomes operational within 2 minutes

## Assumptions

- **AS-001**: Development will occur on macOS, Linux, or WSL2 on Windows, with Docker Desktop or compatible container runtime available
- **AS-002**: Python 3.12+ is available on the development machine
- **AS-003**: Node.js 18+ and npm are available for frontend development
- **AS-004**: PostgreSQL 14+ with pgvector extension support is available (either via Docker or local installation)
- **AS-005**: Developers have basic familiarity with FastAPI, SQLAlchemy, and Next.js frameworks
- **AS-006**: The project will use PostgreSQL as the primary database rather than alternative vector databases
- **AS-007**: Authentication implementation (Auth0, Supabase Auth, or Keycloak) will be added in a future iteration after the skeleton is in place
- **AS-008**: LLM API keys (OpenAI, Anthropic, etc.) will be configured by developers according to their preferences
- **AS-009**: The project will use LangChain as the primary RAG orchestration framework, with the architecture allowing for future framework swaps
- **AS-010**: Document parsing will use Docling or similar libraries, with specific OCR implementation (PaddleOCR, Tesseract) to be finalized during implementation
- **AS-011**: The evaluation harness module will be scaffolded but detailed metrics implementation will come in later iterations
- **AS-012**: Frontend will use shadcn/ui component library for consistent UI components

## Dependencies

- **DEP-001**: Docker and Docker Compose must be available for local development environment
- **DEP-002**: Git must be configured for version control operations
- **DEP-003**: Internet connectivity required for downloading dependencies and Docker images
- **DEP-004**: Sufficient disk space (minimum 5GB) for Docker images, dependencies, and development database

## Out of Scope

- **OOS-001**: Actual implementation of ETL processing logic (document parsing, OCR, embedding generation)
- **OOS-002**: RAG retrieval algorithms and query processing implementation
- **OOS-003**: Authentication and authorization implementation (RBAC, JWT, OAuth integration)
- **OOS-004**: Frontend UI components and pages beyond the basic shell
- **OOS-005**: API endpoints beyond the health check
- **OOS-006**: Deployment configuration for production environments (Kubernetes, cloud-specific configuration)
- **OOS-007**: CI/CD pipeline setup (GitHub Actions, GitLab CI)
- **OOS-008**: Monitoring and observability setup (Prometheus, Grafana, application performance monitoring)
- **OOS-009**: Data migration tools or scripts for importing existing documents
- **OOS-010**: GraphRAG implementation or graph database integration
- **OOS-011**: LoRA fine-tuning infrastructure
- **OOS-012**: Background job queue implementation (Celery, RQ)
- **OOS-013**: Cloud storage integration (S3, GCS, Azure Blob)
- **OOS-014**: Email notification system
- **OOS-015**: Admin dashboard UI implementation

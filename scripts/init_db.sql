-- AgenticOmni Database Initialization Script
-- This script is automatically executed by PostgreSQL on first container startup
-- via docker-entrypoint-initdb.d/

-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify pgvector extension is installed
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'AgenticOmni database initialized with pgvector extension';
END
$$;

#!/usr/bin/env python3
"""Validate project directory structure completeness.

This script checks that all required directories and files exist for the
AgenticOmni application skeleton.
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Required directories
REQUIRED_DIRS = [
    "src",
    "src/ingestion_parsing",
    "src/storage_indexing",
    "src/rag_orchestration",
    "src/eval_harness",
    "src/security_auth",
    "src/api",
    "src/shared",
    "tests",
    "docs",
    "config",
    "scripts",
    "frontend",
]

# Required files
REQUIRED_FILES = [
    "README.md",
    ".gitignore",
    "src/__init__.py",
    "src/ingestion_parsing/__init__.py",
    "src/storage_indexing/__init__.py",
    "src/rag_orchestration/__init__.py",
    "src/eval_harness/__init__.py",
    "src/security_auth/__init__.py",
    "src/api/__init__.py",
    "src/shared/__init__.py",
]


def validate_structure(root_dir: Path) -> Tuple[bool, List[str]]:
    """Validate that all required directories and files exist.
    
    Args:
        root_dir: Project root directory path
        
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    errors = []
    
    # Check directories
    for dir_path in REQUIRED_DIRS:
        full_path = root_dir / dir_path
        if not full_path.exists():
            errors.append(f"Missing directory: {dir_path}")
        elif not full_path.is_dir():
            errors.append(f"Not a directory: {dir_path}")
    
    # Check files
    for file_path in REQUIRED_FILES:
        full_path = root_dir / file_path
        if not full_path.exists():
            errors.append(f"Missing file: {file_path}")
        elif not full_path.is_file():
            errors.append(f"Not a file: {file_path}")
    
    return len(errors) == 0, errors


def main() -> int:
    """Main validation function.
    
    Returns:
        0 if validation passes, 1 if validation fails
    """
    project_root = Path(__file__).parent.parent
    
    print("=" * 70)
    print("AgenticOmni Project Structure Validation")
    print("=" * 70)
    print()
    
    success, errors = validate_structure(project_root)
    
    if success:
        print("✅ All required directories and files are present!")
        print()
        print(f"Validated {len(REQUIRED_DIRS)} directories")
        print(f"Validated {len(REQUIRED_FILES)} files")
        return 0
    else:
        print("❌ Validation failed!")
        print()
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
        print()
        print(f"Total errors: {len(errors)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

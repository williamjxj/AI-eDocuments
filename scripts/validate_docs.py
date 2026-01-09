#!/usr/bin/env python3
"""Documentation validation script for AgenticOmni.

This script validates that all documentation follows the versioning standards
and checks for common issues like broken links, missing version headers, etc.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


class Color:
    """ANSI color codes for terminal output."""
    
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def check_version_header(file_path: Path) -> Tuple[bool, List[str]]:
    """Check if a markdown file has proper version header.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Check for YAML frontmatter
        if not content.startswith("---\n"):
            issues.append("Missing YAML frontmatter (should start with '---')")
            return False, issues
        
        # Extract frontmatter
        parts = content.split("---\n", 2)
        if len(parts) < 3:
            issues.append("Invalid YAML frontmatter structure")
            return False, issues
        
        frontmatter = parts[1]
        
        # Required fields
        required_fields = ["title", "version", "date", "authors", "status"]
        
        for field in required_fields:
            if not re.search(rf"^{field}:", frontmatter, re.MULTILINE):
                issues.append(f"Missing required field: {field}")
        
        # Validate version format (semantic versioning)
        version_match = re.search(r'^version:\s*"([^"]+)"', frontmatter, re.MULTILINE)
        if version_match:
            version = version_match.group(1)
            if not re.match(r"^\d+\.\d+\.\d+$", version):
                issues.append(f"Invalid version format: {version} (expected X.Y.Z)")
        
        # Validate date format
        date_match = re.search(r'^date:\s*"([^"]+)"', frontmatter, re.MULTILINE)
        if date_match:
            date = date_match.group(1)
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                issues.append(f"Invalid date format: {date} (expected YYYY-MM-DD)")
        
        # Validate status
        status_match = re.search(r'^status:\s*"([^"]+)"', frontmatter, re.MULTILINE)
        if status_match:
            status = status_match.group(1)
            valid_statuses = ["draft", "review", "approved", "deprecated"]
            if status not in valid_statuses:
                issues.append(
                    f"Invalid status: {status} (expected one of {valid_statuses})"
                )
        
        return len(issues) == 0, issues
    
    except Exception as e:
        issues.append(f"Error reading file: {e}")
        return False, issues


def check_broken_links(file_path: Path, project_root: Path) -> Tuple[bool, List[str]]:
    """Check for broken internal links in markdown file.
    
    Args:
        file_path: Path to the markdown file
        project_root: Project root directory
        
    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Find all markdown links
        link_pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
        links = re.findall(link_pattern, content)
        
        for text, url in links:
            # Skip external links
            if url.startswith(("http://", "https://", "#")):
                continue
            
            # Resolve relative path
            link_path = (file_path.parent / url).resolve()
            
            if not link_path.exists():
                issues.append(f"Broken link: [{text}]({url})")
        
        return len(issues) == 0, issues
    
    except Exception as e:
        issues.append(f"Error checking links: {e}")
        return False, issues


def check_last_updated(file_path: Path) -> Tuple[bool, List[str]]:
    """Check if document has 'Last Updated' timestamp.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
        
        if not re.search(r"\*\*Last Updated\*\*:", content, re.IGNORECASE):
            issues.append("Missing 'Last Updated' timestamp")
        
        return len(issues) == 0, issues
    
    except Exception as e:
        issues.append(f"Error checking timestamp: {e}")
        return False, issues


def validate_documentation(docs_dir: Path) -> int:
    """Validate all markdown documentation in the docs directory.
    
    Args:
        docs_dir: Path to docs directory
        
    Returns:
        Exit code (0 for success, 1 for failures)
    """
    print(f"{Color.BOLD}AgenticOmni Documentation Validator{Color.RESET}")
    print("=" * 70)
    print()
    
    # Find all markdown files (exclude templates and CHANGELOG)
    md_files = [
        f for f in docs_dir.rglob("*.md")
        if "templates" not in f.parts and f.name != "CHANGELOG.md"
    ]
    
    if not md_files:
        print(f"{Color.YELLOW}⚠️  No markdown files found{Color.RESET}")
        return 0
    
    print(f"Found {len(md_files)} documentation files to validate\n")
    
    total_issues = 0
    failed_files = 0
    project_root = docs_dir.parent
    
    for md_file in sorted(md_files):
        relative_path = md_file.relative_to(project_root)
        print(f"{Color.BLUE}Checking:{Color.RESET} {relative_path}")
        
        file_issues = []
        
        # Check version header
        valid_header, header_issues = check_version_header(md_file)
        if not valid_header:
            file_issues.extend([f"  ❌ {issue}" for issue in header_issues])
        
        # Check broken links
        valid_links, link_issues = check_broken_links(md_file, project_root)
        if not valid_links:
            file_issues.extend([f"  ❌ {issue}" for issue in link_issues])
        
        # Check last updated
        valid_timestamp, timestamp_issues = check_last_updated(md_file)
        if not valid_timestamp:
            file_issues.extend([f"  ❌ {issue}" for issue in timestamp_issues])
        
        if file_issues:
            print(f"{Color.RED}  ✗ Failed{Color.RESET}")
            for issue in file_issues:
                print(issue)
            failed_files += 1
            total_issues += len(file_issues)
        else:
            print(f"{Color.GREEN}  ✓ Passed{Color.RESET}")
        
        print()
    
    # Print summary
    print("=" * 70)
    print(f"{Color.BOLD}Validation Summary{Color.RESET}")
    print("=" * 70)
    print(f"Total files checked: {len(md_files)}")
    print(f"Passed: {Color.GREEN}{len(md_files) - failed_files}{Color.RESET}")
    print(f"Failed: {Color.RED}{failed_files}{Color.RESET}")
    print(f"Total issues: {Color.RED}{total_issues}{Color.RESET}")
    print()
    
    if failed_files > 0:
        print(f"{Color.RED}❌ Validation failed!{Color.RESET}")
        print()
        print("To fix issues:")
        print("  1. Add version headers to documents missing them")
        print("  2. Fix broken internal links")
        print("  3. Add 'Last Updated' timestamp to documents")
        print()
        print("See docs/README.md for documentation standards")
        return 1
    else:
        print(f"{Color.GREEN}✅ All documentation is valid!{Color.RESET}")
        return 0


def main() -> int:
    """Main validation function.
    
    Returns:
        Exit code
    """
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    docs_dir = project_root / "docs"
    
    if not docs_dir.exists():
        print(f"{Color.RED}Error: docs directory not found{Color.RESET}")
        return 1
    
    return validate_documentation(docs_dir)


if __name__ == "__main__":
    sys.exit(main())

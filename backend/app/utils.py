"""Utility functions for LegacyMap backend."""

import os
import re
from pathlib import Path
from typing import Optional


def normalize_path(path: str) -> str:
    """Normalize file path to use forward slashes."""
    return path.replace("\\", "/")


def get_file_extension(filename: str) -> str:
    """Get file extension in lowercase."""
    return Path(filename).suffix.lower()


def is_supported_file(filename: str) -> bool:
    """Check if file is a supported code file."""
    # User requested ONLY Java support
    supported_extensions = {".java"}
    return get_file_extension(filename) in supported_extensions


def get_language(filename: str) -> Optional[str]:
    """Determine programming language from file extension."""
    ext = get_file_extension(filename)
    if ext == ".java":
        return "java"
    return None


def count_lines(content: str) -> int:
    """Count non-empty lines in file content."""
    return len([line for line in content.split("\n") if line.strip()])


def extract_imports_python(content: str) -> list[str]:
    """Extract import statements from Python code."""
    imports = []
    import_pattern = r"^\s*(?:from\s+([a-zA-Z0-9_.]+)\s+import|import\s+([a-zA-Z0-9_.]+))"
    for line in content.split("\n"):
        match = re.match(import_pattern, line)
        if match:
            module = match.group(1) or match.group(2)
            if module:
                imports.append(module.split(".")[0])
    return list(set(imports))


def extract_imports_javascript(content: str) -> list[str]:
    """Extract import/require statements from JavaScript/TypeScript code."""
    imports = []
    import_patterns = [
        r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
        r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
    ]
    for pattern in import_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            module = match.group(1)
            if not module.startswith(".") and not module.startswith("/"):
                imports.append(module)
    return list(set(imports))


def extract_imports_java(content: str) -> list[str]:
    """Extract import statements from Java code."""
    imports = []
    # Match: import com.example.package;
    # Match: import static com.example.package.Class;
    import_pattern = r"^\s*import\s+(?:static\s+)?([a-zA-Z0-9_.]+);"
    
    for line in content.split("\n"):
        match = re.match(import_pattern, line)
        if match:
            full_import = match.group(1)
            # For analysis, we might want the top-level package or the specific class
            # Let's keep the full import path for now, or maybe just the class name?
            # Usually dependency graphs in Java map classes to classes.
            # If we import 'java.util.List', we depend on 'List'.
            # But often we want to see internal project dependencies.
            # Let's store the full package for now.
            imports.append(full_import)
            
    return list(set(imports))


def calculate_risk_score(loc: int, imported_by_count: int, imports_count: int) -> float:
    """
    Calculate risk score for a file.
    
    Formula: (LOC / 10) + (imported_by * 3) + (imports * 2)
    """
    return (loc / 10) + (imported_by_count * 3) + (imports_count * 2)


def get_risk_level(risk_score: float) -> str:
    """Get risk level category based on score."""
    if risk_score < 10:
        return "LOW"
    elif risk_score < 25:
        return "MEDIUM"
    else:
        return "HIGH"

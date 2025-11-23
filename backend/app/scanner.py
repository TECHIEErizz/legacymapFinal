"""Code scanner and analyzer for LegacyMap."""

import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import networkx as nx

from .utils import (
    normalize_path,
    is_supported_file,
    get_language,
    count_lines,
    extract_imports_python,
    extract_imports_javascript,
    extract_imports_java,
    calculate_risk_score,
    get_risk_level,
)
from .function_extractor import FunctionExtractor


class CodeScanner:
    """Scan and analyze code repositories."""
    
    def __init__(self):
        self.function_extractor = FunctionExtractor()
        self.temp_dir = None
    
    def extract_zip(self, zip_path: str) -> str:
        """Extract ZIP file to temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        
        return self.temp_dir
    
    def cleanup(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def scan_directory(self, directory: str) -> Dict[str, Any]:
        """
        Scan directory and analyze code files.
        
        Returns:
            Dictionary with analysis results including files, functions, and dependencies.
        """
        files_data = {}
        all_functions = []
        dependency_graph = nx.DiGraph()
        
        # Walk through directory
        for root, dirs, files in os.walk(directory):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in {
                'node_modules', '.git', '__pycache__', 'venv', 'env',
                '.venv', 'dist', 'build', '.next', 'coverage', 'target', 'bin', 'obj'
            }]
            
            for file in files:
                if not is_supported_file(file):
                    continue
                
                file_path = os.path.join(root, file)
                relative_path = normalize_path(os.path.relpath(file_path, directory))
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    language = get_language(file)
                    if not language:
                        continue
                    
                    # Count lines
                    loc = count_lines(content)
                    
                    # Extract imports
                    if language == "python":
                        imports = extract_imports_python(content)
                    elif language == "java":
                        imports = extract_imports_java(content)
                    else:
                        imports = extract_imports_javascript(content)
                    
                    # Extract functions
                    functions = self.function_extractor.extract_functions(
                        content, relative_path, language
                    )
                    
                    # Store file data
                    files_data[relative_path] = {
                        "path": relative_path,
                        "language": language,
                        "loc": loc,
                        "imports": imports,
                        "imports_count": len(imports),
                        "functions": [f["name"] for f in functions],
                        "function_count": len(functions),
                        "content": content,  # Store for later analysis
                    }
                    
                    # Add functions to list
                    all_functions.extend(functions)
                    
                    # Add to dependency graph
                    dependency_graph.add_node(relative_path)
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    continue
        
        # Build dependency relationships
        for file_path, file_data in files_data.items():
            for imported_module in file_data["imports"]:
                # Try to find matching file
                for other_file in files_data.keys():
                    # Simple matching: check if import matches filename
                    other_basename = Path(other_file).stem
                    if imported_module == other_basename or imported_module.endswith(other_basename):
                        dependency_graph.add_edge(file_path, other_file)
        
        # Calculate imported_by counts
        for file_path in files_data.keys():
            imported_by = list(dependency_graph.predecessors(file_path))
            files_data[file_path]["imported_by"] = imported_by
            files_data[file_path]["imported_by_count"] = len(imported_by)
        
        # Calculate risk scores
        for file_path, file_data in files_data.items():
            risk_score = calculate_risk_score(
                file_data["loc"],
                file_data["imported_by_count"],
                file_data["imports_count"]
            )
            files_data[file_path]["risk_score"] = round(risk_score, 2)
            files_data[file_path]["risk_level"] = get_risk_level(risk_score)
        
        # Prepare summary
        total_files = len(files_data)
        total_functions = len(all_functions)
        total_loc = sum(f["loc"] for f in files_data.values())
        avg_risk = sum(f["risk_score"] for f in files_data.values()) / total_files if total_files > 0 else 0
        
        return {
            "summary": {
                "total_files": total_files,
                "total_functions": total_functions,
                "total_loc": total_loc,
                "average_risk_score": round(avg_risk, 2),
            },
            "files": list(files_data.values()),
            "functions": all_functions,
            "dependency_graph": {
                "nodes": list(dependency_graph.nodes()),
                "edges": list(dependency_graph.edges()),
            }
        }
    
    def get_function_details(
        self,
        files_data: List[Dict[str, Any]],
        file_path: str,
        function_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific function.
        
        Args:
            files_data: List of file data from scan results
            file_path: Path to the file containing the function
            function_name: Name of the function
        
        Returns:
            Dictionary with function details including call sites and dependencies
        """
        # Find the file
        target_file = None
        for file_data in files_data:
            if file_data["path"] == file_path:
                target_file = file_data
                break
        
        if not target_file:
            return None
        
        content = target_file.get("content", "")
        language = target_file.get("language", "")
        
        # Find where this function is called
        call_sites = []
        for file_data in files_data:
            file_content = file_data.get("content", "")
            file_lang = file_data.get("language", "")
            
            call_lines = self.function_extractor.find_function_calls(
                file_content, function_name, file_lang
            )
            
            if call_lines:
                call_sites.append({
                    "file": file_data["path"],
                    "lines": call_lines,
                    "count": len(call_lines)
                })
        
        # Find what this function depends on
        dependencies = self.function_extractor.extract_function_dependencies(
            content, function_name, language
        )
        
        return {
            "name": function_name,
            "file": file_path,
            "language": language,
            "called_in": call_sites,
            "dependencies": dependencies,
            "call_count": sum(site["count"] for site in call_sites),
        }
    
    def analyze_zip(self, zip_path: str) -> Dict[str, Any]:
        """
        Analyze a ZIP file containing code.
        
        Args:
            zip_path: Path to ZIP file
        
        Returns:
            Analysis results
        """
        try:
            # Extract ZIP
            extract_dir = self.extract_zip(zip_path)
            
            # Scan directory
            results = self.scan_directory(extract_dir)
            
            return results
        
        finally:
            # Always cleanup
            self.cleanup()

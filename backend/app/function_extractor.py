"""Function and class extraction from code files."""

import re
from typing import List, Dict, Any


class FunctionExtractor:
    """Extract functions and classes from source code."""
    
class FunctionExtractor:
    """Extract functions and classes from source code."""
    
    def __init__(self):
        # Python patterns
        self.python_function_pattern = r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
        self.python_class_pattern = r"^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]"
        
        # JavaScript/TypeScript patterns
        self.js_function_patterns = [
            r"function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(",
            r"const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
            r"let\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
            r"var\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
            r"([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:\s*(?:async\s+)?\([^)]*\)\s*=>",
            r"([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)\s*\{",
        ]
        self.js_class_pattern = r"class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)"

        # Java patterns
        # Class: public class MyClass {
        self.java_class_pattern = r"(?:public|protected|private|static|\s)*class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)"
        # Method: public void myMethod(String arg) {
        # This is complex in regex. Simplified: access modifiers? return type name (args) {
        self.java_method_pattern = r"(?:public|protected|private|static|\s)*[\w<>[\]]+\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\s*\{"

    def extract_python_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Python functions and classes."""
        functions = []
        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            func_match = re.match(self.python_function_pattern, line)
            if func_match:
                functions.append({
                    "name": func_match.group(1),
                    "type": "function",
                    "file": file_path,
                    "line": line_num,
                    "language": "python"
                })
            class_match = re.match(self.python_class_pattern, line)
            if class_match:
                functions.append({
                    "name": class_match.group(1),
                    "type": "class",
                    "file": file_path,
                    "line": line_num,
                    "language": "python"
                })
        return functions
    
    def extract_javascript_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract JavaScript/TypeScript functions and classes."""
        functions = []
        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            class_match = re.search(self.js_class_pattern, line)
            if class_match:
                functions.append({
                    "name": class_match.group(1),
                    "type": "class",
                    "file": file_path,
                    "line": line_num,
                    "language": "javascript"
                })
            for pattern in self.js_function_patterns:
                func_match = re.search(pattern, line)
                if func_match:
                    func_name = func_match.group(1)
                    if func_name not in {"if", "for", "while", "switch", "catch"}:
                        functions.append({
                            "name": func_name,
                            "type": "function",
                            "file": file_path,
                            "line": line_num,
                            "language": "javascript"
                        })
                    break
        return functions

    def extract_java_functions(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Java functions (methods) and classes."""
        functions = []
        lines = content.split("\n")
        
        for line_num, line in enumerate(lines, 1):
            # Check for class definition
            class_match = re.search(self.java_class_pattern, line)
            if class_match:
                class_name = class_match.group(1)
                functions.append({
                    "name": class_name,
                    "type": "class",
                    "file": file_path,
                    "line": line_num,
                    "language": "java"
                })
                continue # Usually don't have class and method on same line

            # Check for method definition
            # We need to avoid matching control structures like 'if (condition) {'
            method_match = re.search(self.java_method_pattern, line)
            if method_match:
                method_name = method_match.group(1)
                # Filter out common keywords that might match the pattern
                if method_name not in {"if", "for", "while", "switch", "catch", "synchronized"}:
                    functions.append({
                        "name": method_name,
                        "type": "function", # method
                        "file": file_path,
                        "line": line_num,
                        "language": "java"
                    })
        
        return functions
    
    def extract_functions(self, content: str, file_path: str, language: str) -> List[Dict[str, Any]]:
        """Extract functions based on language."""
        if language == "python":
            return self.extract_python_functions(content, file_path)
        elif language in {"javascript", "typescript"}:
            return self.extract_javascript_functions(content, file_path)
        elif language == "java":
            return self.extract_java_functions(content, file_path)
        return []
    
    def find_function_calls(self, content: str, function_name: str, language: str) -> List[int]:
        """Find line numbers where a function is called."""
        call_lines = []
        lines = content.split("\n")
        
        # Java/JS/Python all use name(args) syntax mostly
        pattern = rf"\b{re.escape(function_name)}\s*\("
        
        for line_num, line in enumerate(lines, 1):
            # Skip definition lines
            if language == "java":
                if re.search(rf"(?:class|void|int|String|public|private|protected|static)\s+{re.escape(function_name)}\b", line):
                    continue
            elif language == "python":
                if re.search(rf"^\s*def\s+{re.escape(function_name)}\b", line):
                    continue
            else:
                if re.search(rf"^\s*(?:function|const|let|var|class)\s+{re.escape(function_name)}\b", line):
                    continue
            
            if re.search(pattern, line):
                call_lines.append(line_num)
        
        return call_lines
    
    def extract_function_dependencies(self, content: str, function_name: str, language: str) -> List[str]:
        """Extract what other functions this function calls."""
        dependencies = []
        lines = content.split("\n")
        func_start = None
        
        # Find start
        for line_num, line in enumerate(lines):
            if language == "java":
                match = re.search(rf"\b{re.escape(function_name)}\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\s*\{{", line)
            elif language == "python":
                match = re.match(rf"^(\s*)def\s+{re.escape(function_name)}\s*\(", line)
            else:
                match = re.search(rf"\b{re.escape(function_name)}\s*[=:]?\s*(?:async\s+)?\([^)]*\)\s*(?:=>|\{{)", line)
            
            if match:
                func_start = line_num
                break
        
        if func_start is None:
            return dependencies
            
        # Extract body - simplified for Java (brace counting is hard with regex/line-by-line)
        # We'll just read until the next method definition or end of file for now as a heuristic
        # Or use indentation for Python
        
        func_body_lines = []
        brace_count = 0
        started = False
        
        for i in range(func_start, len(lines)):
            line = lines[i]
            
            if language == "python":
                if i > func_start:
                    # Check indentation
                    if line.strip() and not line.startswith(" " * 4): # Assuming 4 spaces
                         # This is weak without knowing original indentation, but okay for MVP
                         pass 
                    # Actually, let's just grab next 50 lines or until next def
                    if re.match(r"^\s*def\s+", line):
                        break
            elif language == "java" or language in {"javascript", "typescript"}:
                brace_count += line.count("{")
                brace_count -= line.count("}")
                if brace_count == 0 and started:
                    break
                if not started and "{" in line:
                    started = True
            
            func_body_lines.append(line)
            
        func_body = "\n".join(func_body_lines)
        call_pattern = r"\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\("
        
        for match in re.finditer(call_pattern, func_body):
            called_func = match.group(1)
            if called_func not in {"if", "for", "while", "switch", "catch", "print", "println", "return", function_name}:
                dependencies.append(called_func)
                
        return list(set(dependencies))

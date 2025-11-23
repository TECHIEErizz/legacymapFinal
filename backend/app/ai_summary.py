import os
import requests
import json
from typing import Dict, Any

# Configuration for Local AI (Ollama)
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")  # Default to mistral, can be llama3, etc.

def generate_summary(analysis_data: Dict[str, Any]) -> str:
    """
    Generate a natural language summary of the codebase analysis using Local AI (Ollama).
    """
    try:
        # Construct a prompt from the analysis data
        summary_stats = analysis_data.get("summary", {})
        files = analysis_data.get("files", [])
        
        # Get high risk files
        high_risk_files = sorted(files, key=lambda x: x.get("risk_score", 0), reverse=True)[:3]
        
        # Get key classes/functions (just a sample)
        functions = analysis_data.get("functions", [])
        classes = [f["name"] for f in functions if f.get("type") == "class"]
        
        prompt = f"""
        You are an expert Senior Software Architect. I have analyzed a legacy codebase and need you to provide a professional executive summary.
        
        Here is the data I extracted:
        
        **Project Stats:**
        - Total Files: {summary_stats.get('total_files')}
        - Total Functions/Methods: {summary_stats.get('total_functions')}
        - Total Lines of Code: {summary_stats.get('total_loc')}
        
        **Key Components (Classes):**
        {', '.join(classes[:10])}
        
        **Top 3 High-Risk Files (Complex & Heavily Used):**
        {', '.join([f"{f['path']} (Risk Score: {f.get('risk_score')})" for f in high_risk_files])}
        
        **Task:**
        Write a concise but insightful summary of this codebase.
        1. **Overview:** What does this project likely do based on the class names?
        2. **Architecture:** Describe the structure (e.g., is it a simple script, a web app, a data processing tool?).
        3. **Risk Assessment:** Comment on the high-risk files and why they might be critical.
        4. **Recommendations:** Give 1-2 quick tips for refactoring or maintenance.
        
        Keep the tone professional and constructive. Format with Markdown.
        """
        
        # Payload for Ollama
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        print(f"Sending request to Ollama ({OLLAMA_MODEL})...")
        # Increased timeout to 300s (5 min) as local AI can be slow on first load
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response generated.")
        else:
            return f"Error from Local AI: {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Make sure Ollama is running locally (http://localhost:11434)."
    except Exception as e:
        return f"Error generating summary: {str(e)}"

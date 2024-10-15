import os
import subprocess
from typing import List
from embeddings import generate_embeddings, search_similar_code

def analyze_code_diff() -> str:
    try:
        result = subprocess.run(['git', 'diff'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(result.stderr.decode())
        diff_output = result.stdout.decode()
        embeddings = generate_embeddings(diff_output)
        similar_code = search_similar_code(embeddings)
        return f"Análisis del Diff:\n{diff_output}\nCódigo Similar:\n{similar_code}"
    except Exception as e:
        raise Exception(f"Error al analizar el diff del código: {e}")

def scan_project() -> str:
    try:
        project_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    project_files.append(os.path.join(root, file))
        project_summary = f"Total de archivos: {len(project_files)}"
        return project_summary
    except Exception as e:
        raise Exception(f"Error al escanear el proyecto: {e}")

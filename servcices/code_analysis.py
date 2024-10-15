import os
import subprocess
from typing import List
from embeddings import generate_embeddings, search_similar_code

def get_gitignored_files() -> List[str]:
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--others', '--ignored', '--exclude-standard'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(result.stderr.decode())
        gitignored_files = result.stdout.decode().splitlines()
        return gitignored_files
    except Exception as e:
        raise Exception(f"Error al obtener archivos ignorados por Git: {e}")

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
        gitignored_files = get_gitignored_files()
        project_files = []
        for root, dirs, files in os.walk('.'):
            # Excluir directorios ocultos como .git
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                filepath = os.path.relpath(os.path.join(root, file))
                if not any(filepath.startswith(ignored) for ignored in gitignored_files):
                    project_files.append(filepath)
        project_summary = f"Total de archivos (excluyendo .gitignore): {len(project_files)}"
        return project_summary
    except Exception as e:
        raise Exception(f"Error al escanear el proyecto: {e}")
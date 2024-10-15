import os
import subprocess
from typing import List, Tuple
from embeddings import generate_embeddings, save_embedding
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import ast
import sys
import numpy as np

# Variables para seguimiento del progreso
_progress = {
    'total': 0,
    'completed': 0
}

def get_analysis_progress():
    return _progress

def get_gitignored_files() -> set:
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--others', '--ignored', '--exclude-standard'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(result.stderr.decode())
        gitignored_files = set(result.stdout.decode().splitlines())
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

def process_file(file_path: str) -> Tuple[str, str]:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Generar y guardar embeddings
        embedding = generate_embeddings(content)
        save_embedding(file_path, embedding)

        # Análisis estático utilizando AST (solo para archivos Python)
        if file_path.endswith('.py'):
            try:
                tree = ast.parse(content)
                analysis = f"Archivo {file_path}: Sintaxis correcta."
            except SyntaxError as e:
                analysis = f"Archivo {file_path}: Error de sintaxis - {e}"
        else:
            analysis = f"Archivo {file_path}: Embedding generado y guardado."

        # Actualizar progreso
        _progress['completed'] += 1

        return (file_path, analysis)
    except Exception as e:
        return (file_path, f"Error al procesar el archivo: {e}")

def scan_project() -> Tuple[str, List[Tuple[str, str]]]:
    try:
        gitignored_files = get_gitignored_files()
        project_files = []
        for root, dirs, files in os.walk('.'):
            # Excluir directorios ocultos como .git
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                filepath = os.path.relpath(os.path.join(root, file))
                if filepath not in gitignored_files:
                    project_files.append(filepath)
        total_files = len(project_files)

        # Actualizar el progreso total
        _progress['total'] = total_files
        _progress['completed'] = 0

        num_workers = min(4, cpu_count())  # Limitar el número de procesos para evitar sobrecarga
        analysis_results = []

        with Pool(num_workers) as pool:
            # Usar tqdm para mostrar la barra de progreso
            for result in tqdm(pool.imap_unordered(process_file, project_files), total=total_files, desc="Escaneando archivos"):
                analysis_results.append(result)

        project_summary = f"Total de archivos analizados (excluyendo .gitignore): {total_files}"
        return project_summary, analysis_results
    except Exception as e:
        raise Exception(f"Error al escanear el proyecto: {e}")
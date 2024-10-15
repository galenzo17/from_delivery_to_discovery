import os
import subprocess
from typing import List, Tuple
from embeddings import generate_embeddings, search_similar_code
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# Variable global para almacenar el progreso
progress = {
    'total': 0,
    'completed': 0
}

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

def process_file(file_path: str) -> Tuple[str, str]:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Aquí puedes agregar lógica adicional si es necesario
        return (file_path, content)
    except Exception as e:
        return (file_path, f"Error al procesar el archivo: {e}")

def scan_project() -> str:
    try:
        gitignored_files = set(get_gitignored_files())
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
        progress['total'] = total_files
        progress['completed'] = 0

        num_workers = cpu_count()
        with Pool(num_workers) as pool:
            # Usar tqdm para mostrar la barra de progreso
            for _ in tqdm(pool.imap_unordered(process_file, project_files), total=total_files, desc="Escaneando archivos"):
                # Actualizar el progreso completado
                progress['completed'] += 1

        project_summary = f"Total de archivos (excluyendo .gitignore): {total_files}"
        return project_summary
    except Exception as e:
        raise Exception(f"Error al escanear el proyecto: {e}")
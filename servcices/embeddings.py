import openai
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Embedding
import numpy as np

def generate_embeddings(text: str):
    try:
        response = openai.Embedding.create(
            input=text,
            engine="text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        return embeddings
    except Exception as e:
        raise Exception(f"Error al generar embeddings: {e}")

def save_embedding(file_path: str, embedding: list):
    try:
        db: Session = SessionLocal()
        embedding_data = Embedding(
            file_path=file_path,
            embedding=np.array(embedding).tobytes()
        )
        db.add(embedding_data)
        db.commit()
        db.refresh(embedding_data)
        db.close()
    except Exception as e:
        raise Exception(f"Error al guardar el embedding en la base de datos: {e}")

def search_similar_code(embedding: list):
    # Implementación de búsqueda de código similar utilizando la base de datos
    try:
        db: Session = SessionLocal()
        # Recuperar todos los embeddings de la base de datos
        embeddings = db.query(Embedding).all()
        db.close()

        # Convertir los embeddings almacenados en bytes a arrays numpy
        stored_embeddings = [
            (e.file_path, np.frombuffer(e.embedding, dtype=np.float32))
            for e in embeddings
        ]

        # Calcular similitud (por ejemplo, utilizando el producto punto)
        similarities = []
        embedding_array = np.array(embedding, dtype=np.float32)
        for file_path, stored_embedding in stored_embeddings:
            similarity = np.dot(embedding_array, stored_embedding)
            similarities.append((file_path, similarity))

        # Ordenar por similitud descendente
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Devolver los 5 más similares
        similar_files = similarities[:5]
        result = "\n".join([f"{file}: {score}" for file, score in similar_files])
        return result
    except Exception as e:
        raise Exception(f"Error en la búsqueda de código similar: {e}")
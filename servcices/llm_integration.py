import openai
from models import Ticket

def generate_ticket_content(ticket: Ticket, code_diff_analysis: str, project_summary: str):
    try:
        prompt = f"""
        Ticket ID: {ticket.id}
        Título: {ticket.title}
        Resumen del Proyecto: {project_summary}
        Análisis del Código:
        {code_diff_analysis}
        Genera una descripción detallada y criterios de aceptación para este ticket.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        content = response.choices[0].text.strip()
        return {"description": content, "acceptance_criteria": ["Criterio 1", "Criterio 2"]}
    except Exception as e:
        raise Exception(f"Error al generar contenido del ticket: {e}")

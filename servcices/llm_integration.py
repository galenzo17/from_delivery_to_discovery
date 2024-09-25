def generate_ticket_content(ticket, code_diff, project_summary):
    # Lógica para interactuar con el LLM y generar contenido
    generated_description = f"Descripción generada para el ticket {ticket.id}"
    acceptance_criteria = ["Criterio de aceptación 1", "Criterio de aceptación 2"]
    return {
        "description": generated_description,
        "acceptance_criteria": acceptance_criteria
    }

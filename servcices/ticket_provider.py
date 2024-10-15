from models import Ticket, TicketUpdateRequest

def get_ticket_details(ticket_id: str) -> Ticket:
    # Simulación de obtención de detalles del ticket
    return Ticket(id=ticket_id, title="Título del Ticket")

def update_ticket(ticket_id: str, request: TicketUpdateRequest) -> Ticket:
    # Simulación de actualización del ticket
    updated_ticket = get_ticket_details(ticket_id)
    if request.description:
        updated_ticket.description = request.description
    if request.acceptance_criteria:
        updated_ticket.acceptance_criteria = request.acceptance_criteria
    return updated_ticket

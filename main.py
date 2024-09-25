from fastapi import FastAPI, Depends, HTTPException
from models import User, TicketUpdateRequest, Ticket
from services.authentication import get_current_user
from services.ticket_provider import get_ticket_details, update_ticket
from services.code_analysis import analyze_code_diff, scan_project
from services.llm_integration import generate_ticket_content

app = FastAPI()

@app.get("/ticket/{branch_name}")
async def refine_ticket(branch_name: str, user: User = Depends(get_current_user)):
    ticket_id = extract_ticket_id(branch_name)
    ticket = get_ticket_details(ticket_id, user)
    project_summary = scan_project()
    code_diff = analyze_code_diff()
    generated_content = generate_ticket_content(ticket, code_diff, project_summary)
    return {"ticket": ticket, "generated_content": generated_content}

@app.post("/ticket/{ticket_id}/update")
async def update_ticket_endpoint(ticket_id: str, request: TicketUpdateRequest, user: User = Depends(get_current_user)):
    updated_ticket = update_ticket(ticket_id, request, user)
    return {"updated_ticket": updated_ticket}

def extract_ticket_id(branch_name: str) -> str:
    # Suponiendo que el branch_name sigue el formato "feature/PROJ-1234-description"
    try:
        ticket_id = branch_name.split("/")[1].split("-")[0] + "-" + branch_name.split("-")[1]
        return ticket_id
    except IndexError:
        raise HTTPException(status_code=400, detail="Nombre de rama inválido")

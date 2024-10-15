from fastapi import FastAPI, Depends, HTTPException
from models import TicketUpdateRequest, User
from services.authentication import get_current_user
from services.ticket_provider import get_ticket_details, update_ticket
from services.code_analysis import analyze_code_diff, scan_project, get_analysis_progress
from services.llm_integration import generate_ticket_content

app = FastAPI()

@app.get("/ticket/{branch_name}")
async def refine_ticket(branch_name: str, user: User = Depends(get_current_user)):
    try:
        ticket_id = extract_ticket_id(branch_name)
        ticket = get_ticket_details(ticket_id)
        project_summary, code_analysis_results = scan_project()
        code_diff_analysis = analyze_code_diff()
        generated_content = generate_ticket_content(ticket, code_diff_analysis, project_summary)
        return {
            "ticket": ticket,
            "content": generated_content,
            "code_analysis": code_analysis_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ticket/{ticket_id}/update")
async def update_ticket_endpoint(ticket_id: str, request: TicketUpdateRequest, user: User = Depends(get_current_user)):
    try:
        updated_ticket = update_ticket(ticket_id, request)
        return {"updated_ticket": updated_ticket}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress")
async def get_progress():
    progress = get_analysis_progress()
    return progress

def extract_ticket_id(branch_name: str) -> str:
    try:
        parts = branch_name.split('/')
        if len(parts) < 2:
            raise ValueError("Formato de rama inválido")
        ticket_part = parts[1]
        ticket_id = ticket_part.split('-')[0]
        return ticket_id
    except Exception as e:
        raise ValueError(f"Error al extraer el ID del ticket: {e}")
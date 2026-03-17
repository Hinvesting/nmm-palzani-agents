from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the NMM Assistant Manager (Palzani-1)
app = FastAPI(title="NMM Palzani Orchestrator", version="1.0")

# Define the structure of an incoming ticket (Schema Enforcement)
class WorkflowRequest(BaseModel):
    task: str

@app.get("/")
def read_root():
    return {"status": "The NMM Kitchen is open. Palzani-1 is listening."}

@app.post("/workflows/start")
def start_workflow(request: WorkflowRequest):
    # Phase 3 stub: Future logic for routing tasks to specialist agents
    return {
        "workflow_id": "ticket_001",
        "state": "IDEA",
        "message": "Workflow logged. Awaiting GM HITL approval."
    }

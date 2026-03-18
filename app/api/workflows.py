from fastapi import APIRouter, HTTPException
from app.models.state import WorkflowState
from app.core.database import get_database
import uuid

router = APIRouter()

@router.post("/workflows/product/start")
def start_product_workflow(task_name: str):
    """Palzani-1 logs a new idea and stages it for research."""
    db = get_database()
    workflow_id = f"ticket_{uuid.uuid4().hex[:8]}"

    new_ticket = {
        "workflow_id": workflow_id,
        "task_name": task_name,
        "state": WorkflowState.IDEA.value,
        "metadata": {"source": "GM_request", "assigned_to": "Palzani-4"}
    }

    # Securely log to MongoDB
    db.workflows.insert_one(new_ticket)
    new_ticket.pop("_id", None) # Remove local Mongo ID for clean JSON output

    return {"message": "Workflow started successfully.", "ticket": new_ticket}

@router.post("/workflows/{workflow_id}/decision")
def hitl_decision(workflow_id: str, decision: str):
    """Handles GM HITL Checkpoints (Approve / Revise / Reject)."""
    db = get_database()
    ticket = db.workflows.find_one({"workflow_id": workflow_id})

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found in Data House.")

    decision = decision.upper()

    if decision == "APPROVE":
        # Advance to the next logical phase; stubbed as PUBLISHED for this endpoint
        db.workflows.update_one(
            {"workflow_id": workflow_id},
            {"$set": {"state": WorkflowState.PUBLISHED.value}}
        )
        return {"message": f"Workflow {workflow_id} APPROVED. Advancing state."}

    elif decision == "REVISE":
        return {"message": f"Workflow {workflow_id} marked for REVISIONS. Routing back to specialist agents."}

    elif decision == "REJECT":
        db.workflows.update_one(
            {"workflow_id": workflow_id},
            {"$set": {"state": "REJECTED_BY_GM"}}
        )
        return {"message": f"Workflow {workflow_id} REJECTED. Logged for future tuning."}

    raise HTTPException(status_code=400, detail="Invalid decision. Use Approve, Revise, or Reject.")

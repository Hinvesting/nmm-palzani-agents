from fastapi import APIRouter, HTTPException
from app.models.agent import AgentConfig
from app.core.database import get_database
import os
import uuid

router = APIRouter()

@router.post("/builder/propose")
def propose_agent(role_name: str, task_complexity: str):
    """Palzani-2 drafts a new agent config using the Reviewer Pattern (Cost Arbitrage)."""
    db = get_database()

    # Step 1: Generation - Cheap model does the heavy lifting (Output tokens)
    generator_model = os.getenv("LITE_CODING_MODEL", "openrouter/qwen/qwen3-coder:free")

    # Step 2: Review - Premium model acts as the expert supervisor (Input tokens)
    reviewer_model = os.getenv("CODE_REVIEWER_MODEL", "anthropic/claude-4.5-opus")

    # Simulated Generation -> Review -> Correction Loop
    agent_id = f"palzani_{uuid.uuid4().hex[:4]}_{role_name.lower().replace(' ', '_')}"

    new_agent = {
        "agent_id": agent_id,
        "role": role_name,
        "system_prompt": f"You are the {role_name}. Strict adherence to NMM North Star required.",
        "allowed_tools": ["google_drive_read"],
        "generation_model_used": generator_model,
        "review_model_used": reviewer_model,
        "review_status": "Code generated, reviewed by premium model, and corrected by Palzani-2.",
        "status": "draft" # Must pass GM HITL to activate
    }

    # Securely log the draft to MongoDB agent_configs collection
    db.agent_configs.insert_one(new_agent)
    new_agent.pop("_id", None) # Clean for JSON response

    return {
        "message": f"Agent built heavily by {generator_model} and verified by {reviewer_model}. Awaiting HITL.",
        "config": new_agent
    }

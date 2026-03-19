from fastapi import APIRouter, HTTPException
from app.core.database import get_database
from app.models.state import WorkflowState
import uuid

router = APIRouter()

@router.post("/content/draft")
def draft_brand_content(topic: str, content_mode: str = "VALUE"):
    """Palzani-5 drafts content in the Haze voice, enforcing the 75/15/10 ratio modes."""
    db = get_database()
    mode = content_mode.upper()

    if mode not in ["VALUE", "HYBRID", "REVENUE"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Must be VALUE, HYBRID, or REVENUE.")

    draft_id = f"draft_{uuid.uuid4().hex[:8]}"

    # Simulated Palzani-5 Generation (Haze Voice + 757 Focus)
    if mode == "VALUE":
        simulated_body = f"Yo 757, let's talk about {topic}. Automating your workflows saves you 20 hours a week. Learn the tech before you get left behind! *Disclaimer: For educational purposes, not financial advice.*"
    elif mode == "HYBRID":
        simulated_body = f"757 entrepreneurs, {topic} is changing the game. I use these free tools daily. If you want the exact templates I use to skip the headache, hit the link. Stay building! *Disclaimer: Educational purposes only.*"
    else:
        simulated_body = f"The 90-Day {topic} Blueprint is live. We took the best strategies working right now in Hampton Roads and packed them into this. Grab it now and get your time back. *Disclaimer: No guaranteed returns.*"

    draft_record = {
        "draft_id": draft_id,
        "agent_id": "Palzani-5",
        "topic": topic,
        "mode": mode,
        "content": simulated_body,
        "state": WorkflowState.DRAFTED.value
    }

    # Securely log to MongoDB 'drafts' collection
    db.drafts.insert_one(draft_record)
    draft_record.pop("_id", None) # Clean for JSON response

    return {
        "message": f"Palzani-5 drafted {mode} content. Ready for Palzani-3 Security Check and GM HITL.",
        "draft": draft_record
    }

@router.post("/content/{draft_id}/stage")
def stage_for_publishing(draft_id: str):
    """Palzani-6 (Publisher) prepares the approved draft for external platforms."""
    db = get_database()

    # Verify the draft exists
    draft = db.drafts.find_one({"draft_id": draft_id})
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found in Data House.")

    # In a live environment, this checks if HITL is complete before allowing Palzani-6 to touch it.
    db.drafts.update_one(
        {"draft_id": draft_id},
        {"$set": {"state": WorkflowState.PRODUCTIZED.value}}
    )

    return {"message": f"Palzani-6 has staged draft {draft_id} for publishing to WordPress/Social Media."}

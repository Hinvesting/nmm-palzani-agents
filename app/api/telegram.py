from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
import os

router = APIRouter()

class TelegramPayload(BaseModel):
    """Strict schema enforcement for incoming Telegram webhooks."""
    message: Dict[str, Any]

@router.post("/telegram/webhook")
def telegram_webhook(payload: TelegramPayload):
    """Palzani-1 receives remote HITL commands and checks via Telegram."""
    admin_id = os.getenv("TELEGRAM_ADMIN_ID", "your_personal_telegram_id_here")

    # Extract message data from Telegram's JSON payload
    message = payload.message
    sender_id = str(message.get("from", {}).get("id", ""))
    text = message.get("text", "").strip()

    # Security Check: Ignore anyone who is not the GM
    if sender_id != admin_id:
        return {"status": "ignored", "reason": "Unauthorized user. Palzani-3 blocked access."}

    # Process standard GM Walkie-Talkie commands
    if text == "/approvals":
        reply_msg = "You have 1 item waiting for GM HITL approval. Reply APPROVE, REVISE, or REJECT."
    elif text == "/status":
        reply_msg = "Palzani Crew Status: All agents online. No errors in the kitchen."
    elif text == "/budget":
        reply_msg = "Budget: $0.08 / $50.00 (0.16% used). Status: Normal."
    elif text.upper() in ["APPROVE", "REVISE", "REJECT"]:
        reply_msg = f"HITL Decision '{text.upper()}' logged. Orchestrator advancing workflow."
    else:
        reply_msg = "Command not recognized. Use /approvals, /status, /budget, or /newproduct."

    return {
        "status": "success",
        "simulated_bot_reply": reply_msg
    }

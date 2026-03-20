from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from app.core.database import get_database
from datetime import datetime
import uuid

router = APIRouter()

class StripePayload(BaseModel):
    """Strict schema enforcement for incoming Stripe webhooks."""
    type: str
    data: Dict[str, Any]

@router.post("/stripe/webhook")
def stripe_revenue_webhook(payload: StripePayload):
    """Phase 10: Palzani-1 logs Stripe purchases to calculate the AI P&L."""
    db = get_database()

    if payload.type == "checkout.session.completed":
        # Stripe processes money in cents, perfectly matching our BUDGET_MONTHLY_CENTS
        revenue_cents = payload.data.get("object", {}).get("amount_total", 0)
        product_id = payload.data.get("object", {}).get("metadata", {}).get("product_id", "unknown")

        pl_record = {
            "transaction_id": f"txn_{uuid.uuid4().hex[:8]}",
            "date": datetime.utcnow().isoformat(),
            "event": "sale",
            "product_id": product_id,
            "revenue_cents": revenue_cents,
            "status": "logged_for_ai_pnl"
        }

        # Securely log the revenue to the MongoDB metrics collection
        db.metrics.insert_one(pl_record)
        pl_record.pop("_id", None) # Clean for JSON response

        return {
            "status": "success",
            "message": "Revenue successfully logged to the Data House P&L.",
            "record": pl_record
        }

    return {"status": "ignored", "message": "Unhandled Stripe event type."}

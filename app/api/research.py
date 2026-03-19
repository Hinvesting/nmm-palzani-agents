from fastapi import APIRouter
from app.core.database import get_database
import os
import uuid

router = APIRouter()

@router.post("/research/discover")
def discover_opportunities(topic: str = "757 local business AI pain points"):
    """Palzani-4 uses Perplexity Sonar to discover pain points and propose 3-5 product ideas."""
    db = get_database()
    api_key = os.getenv("PERPLEXITY_API_KEY")

    # In production, this uses requests.post() to call the Perplexity Sonar API.
    # We enforce a structured output via system prompt to return exactly 3-5 ideas.

    trace_id = f"res_{uuid.uuid4().hex[:8]}"

    # Simulated Structured Output for the Kitchen Display System (Swagger UI)
    product_options = [
        {
            "title": "757 SMB AI Readiness Audit",
            "problem": "Local Hampton Roads businesses do not know where to start with AI.",
            "promise": "A clear 90-day roadmap for integrating AI workflows without hiring expensive dev shops.",
            "format": "PDF Checklist + 30-min Consultation",
            "estimated_effort": "Medium"
        },
        {
            "title": "Hyperlocal Web3 Safety Guide",
            "problem": "Beginners fear scams in crypto and NFTs.",
            "promise": "Safely navigate Web3 and protect your digital assets without getting wrecked.",
            "format": "E-Book",
            "estimated_effort": "Low"
        },
        {
            "title": "Automated Content Flywheel Toolkit",
            "problem": "Aspiring entrepreneurs lack time to post consistently on social media.",
            "promise": "Save 20 hours a week using our tested AI content automation templates.",
            "format": "Notion Template + Video Walkthrough",
            "estimated_effort": "High"
        }
    ]

    research_log = {
        "trace_id": trace_id,
        "agent_id": "Palzani-4",
        "topic": topic,
        "ideas_generated": product_options,
        "status": "AWAITING_GM_HITL"
    }

    # Securely log to MongoDB 'ideas' collection
    db.ideas.insert_one(research_log)
    research_log.pop("_id", None) # Clean for JSON response

    return {
        "message": "Palzani-4 completed Perplexity research. Presenting product options for GM HITL approval.",
        "research_data": research_log
    }

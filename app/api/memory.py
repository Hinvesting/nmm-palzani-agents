from fastapi import APIRouter
from app.core.database import get_database
from datetime import datetime
import os

router = APIRouter()

@router.post("/memory/log")
def update_build_log(phase: str, change: str, reason: str, agent_id: str = "Palzani-7"):
    """Palzani-7 Summarizer securely updates the Build Log and MongoDB Data House."""
    db = get_database()

    log_entry = {
        "date": datetime.utcnow().isoformat(),
        "phase": phase,
        "change": change,
        "reason": reason,
        "agent_id": agent_id
    }

    # 1. Securely log to MongoDB
    db.build_logs.insert_one(log_entry)
    log_entry.pop("_id", None) # Clean for JSON response

    # 2. Write to the local Markdown Build Log in the Memory Folder
    log_path = "drive_mount/00_MEMORY/BUILD_LOG.md"

    # Create the file with a header if it doesn't exist
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("# NMM BUILD LOG\n\n")

    with open(log_path, "a") as f:
        f.write(f"- **{log_entry['date']}** | Phase {phase} | {change} | Reason: {reason}\n")

    return {"message": "Build Log successfully updated by Palzani-7.", "entry": log_entry}

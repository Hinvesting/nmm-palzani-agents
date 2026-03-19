from pydantic import BaseModel
from typing import List

class SecurityAudit(BaseModel):
    """Strict schema for logging security and budget events to the Data House."""
    trace_id: str
    agent_id: str
    action: str
    passed: bool
    flags: List[str]
    cost_cents: float = 0.0

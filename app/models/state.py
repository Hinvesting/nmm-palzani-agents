from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict

class WorkflowState(str, Enum):
    """Strict state machine for NMM outward-facing workflows."""
    IDEA = "IDEA"
    RESEARCHED = "RESEARCHED"
    DRAFTED = "DRAFTED"
    SECURITY_CHECK = "SECURITY_CHECK"
    LEGAL_CHECK = "LEGAL_CHECK"
    LOGGED = "LOGGED"
    GM_REVIEW = "GM_REVIEW"
    PRODUCTIZED = "PRODUCTIZED"
    PUBLISHED = "PUBLISHED"
    MEASURED = "MEASURED"

class WorkflowTicket(BaseModel):
    workflow_id: str
    task_name: str
    state: WorkflowState
    metadata: Optional[Dict] = {}

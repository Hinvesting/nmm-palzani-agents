from pydantic import BaseModel
from typing import List, Optional

class AgentConfig(BaseModel):
    """Strict schema for defining new Palzani crew members."""
    agent_id: str
    role: str
    system_prompt: str
    allowed_tools: List[str]
    generation_model_used: Optional[str] = None
    review_model_used: Optional[str] = None
    review_status: Optional[str] = None
    status: str = "draft"

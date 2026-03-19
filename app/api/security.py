from fastapi import APIRouter
from app.models.security import SecurityAudit
from app.core.database import get_database
import uuid

router = APIRouter()

# Hard cap budget limit defined in Master Plan
BUDGET_MONTHLY_CENTS = 5000

@router.post("/security/scan")
def security_scan(content: str, agent_id: str, estimated_cost_cents: float = 0.0):
    """Palzani-3 Security, Legal Compliance, and Budget check middleware."""
    db = get_database()
    flags = []

    content_lower = content.lower()

    # 1. Palzani-22 Budget Director Check
    if estimated_cost_cents > BUDGET_MONTHLY_CENTS:
        flags.append("BUDGET_EXCEEDED_HALT")

    # 2. Palzani-3 Security Guard Check (Prompt Injection & Risk)
    if "ignore all previous instructions" in content_lower:
        flags.append("PROMPT_INJECTION_DETECTED")

    # 3. Legal Compliance Agent Check (YMYL & Financial Rules)
    if "guaranteed return" in content_lower or "risk-free" in content_lower:
        flags.append("FINANCIAL_GUARANTEE_VIOLATION")
    if "not financial advice" not in content_lower:
        flags.append("MISSING_YMYL_DISCLAIMER")

    passed = len(flags) == 0
    trace_id = f"sec_{uuid.uuid4().hex[:8]}"

    audit_log = {
        "trace_id": trace_id,
        "agent_id": agent_id,
        "action": "content_scan",
        "passed": passed,
        "flags": flags,
        "cost_cents": estimated_cost_cents
    }

    # Securely log to MongoDB audit_logs collection
    db.audit_logs.insert_one(audit_log)
    audit_log.pop("_id", None) # Clean for JSON response

    if not passed:
        return {"status": "FAILED", "message": "Red-Flag Stop-The-Line triggered.", "audit": audit_log}

    return {"status": "PASSED", "message": "Content passed Security, Legal, and Budget checks. Safe for HITL.", "audit": audit_log}

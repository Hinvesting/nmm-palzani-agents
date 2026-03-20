from fastapi import FastAPI
from app.api.workflows import router as workflows_router
from app.api.builder import router as builder_router
from app.api.security import router as security_router
from app.api.memory import router as memory_router
from app.api.research import router as research_router
from app.api.content import router as content_router
from app.api.telegram import router as telegram_router
from app.api.stripe_pnl import router as stripe_router

# Initialize the NMM Assistant Manager (Palzani-1)
app = FastAPI(title="NMM Palzani Orchestrator", version="1.0")

# Plug in all routing boards
app.include_router(workflows_router)
app.include_router(builder_router)
app.include_router(security_router)
app.include_router(memory_router)
app.include_router(research_router)
app.include_router(content_router)
app.include_router(telegram_router)
app.include_router(stripe_router)

@app.get("/")
def read_root():
    return {"status": "The NMM Kitchen is open. Stripe P&L Engine is online."}

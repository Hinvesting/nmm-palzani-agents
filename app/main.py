from fastapi import FastAPI
from app.api.workflows import router as workflows_router
from app.api.builder import router as builder_router
from app.api.security import router as security_router
from app.api.memory import router as memory_router

# Initialize the NMM Assistant Manager (Palzani-1)
app = FastAPI(title="NMM Palzani Orchestrator", version="1.0")

# Plug in all routing boards
app.include_router(workflows_router)
app.include_router(builder_router)
app.include_router(security_router)
app.include_router(memory_router)

@app.get("/")
def read_root():
    return {"status": "The NMM Kitchen is open. Palzani 1, 2, 3, and 7 are online."}

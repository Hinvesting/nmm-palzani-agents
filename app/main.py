from fastapi import FastAPI
from app.api.workflows import router as workflows_router

# Initialize the NMM Assistant Manager (Palzani-1)
app = FastAPI(title="NMM Palzani Orchestrator", version="1.0")

# Plug in the workflow routing board
app.include_router(workflows_router)

@app.get("/")
def read_root():
    return {"status": "The NMM Kitchen is open. Palzani-1 is listening with full workflow routing."}

# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as step1_router
from app.api.langgraph_routes import router as langgraph_router  # ✅ Add this line

app = FastAPI()

# ✅ Add this before including routers
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],  # V0/Next.js runs on 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Now include your routers
app.include_router(step1_router)
app.include_router(langgraph_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Schema Generator Pro!"}

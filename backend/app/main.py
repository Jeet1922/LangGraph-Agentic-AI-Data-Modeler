# # app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import router

# app = FastAPI(title="Schema Generator Pro Backend")

# # Allow frontend like V0 to access the backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace "*" with your actual frontend domain in prod
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount router
# app.include_router(router)

# app/services/main.py

from fastapi import FastAPI
from app.api.routes import router as step1_router
from app.api.langgraph_routes import router as langgraph_router  # ✅ Add this line

app = FastAPI()

app.include_router(step1_router)  # This line is key!
# ✅ Include your LangGraph route
app.include_router(langgraph_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Schema Generator Pro!"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # V0/Next.js runs on 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

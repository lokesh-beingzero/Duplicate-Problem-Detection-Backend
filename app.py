from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.problem_routes import router

app = FastAPI()

# CORS (important for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)
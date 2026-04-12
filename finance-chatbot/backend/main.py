from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router  # Correct: no 'backend.' prefix

app = FastAPI()

expenses = []

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)
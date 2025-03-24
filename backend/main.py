from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import random

app = FastAPI()

# CORS Middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request body model
class CodeRequest(BaseModel):
    code: str

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    code = request.code.strip()
    
    if not code:
        return {"error": "No code provided"}
    
    # Mocked analysis logic - you can integrate actual static analysis tools here
    analysis_result = {
        "overall_score": 82,
        "breakdown": {
            "naming": 8,
            "modularity": 17,
            "comments": 20,
            "formatting": 12,
            "reusability": 10,
            "best_practices": 15,
        },
        "recommendations": [
            "Avoid deeply nested components in your React render logic.",
            "Function 'calculateTotal' in app.py is too long—consider refactoring.",
            "Use camelCase for variable 'Total_Amount'."
        ]
    }

    return analysis_result

@app.get("/")
async def home():
    return {"message": "Carbon Crunch API is running!"}
import os
import random
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=os.getenv("ALLOW_CREDENTIALS", "True") == "True",
    allow_methods=os.getenv("ALLOW_METHODS", "*").split(","),
    allow_headers=os.getenv("ALLOW_HEADERS", "*").split(","),
)

# Request schema
class CodeInput(BaseModel):
    code: str
    language: Optional[str] = "python"

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "AI Code Analyzer API",
        "environment": os.getenv("ENV", "development")
    }

# Code analysis endpoint
@app.post("/analyze")
async def analyze_code(
    code_input: CodeInput,
    use_ai: bool = Query(False, description="Enable AI-powered analysis (currently disabled)"),
    detail_level: str = Query("basic", enum=["basic", "full"])
):
    code = code_input.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    breakdown = {
        "naming": random.randint(5, 80),
        "modularity": random.randint(5, 80),
        "comments": random.randint(5, 70),
        "formatting": random.randint(5, 90),
        "reusability": random.randint(5, 95),
        "best_practices": random.randint(5, 99),
    }
    overall_score = sum(breakdown.values()) // len(breakdown)

    return {
        "overall_score": overall_score,
        "breakdown": breakdown,
        "language": code_input.language
    }

# Run the app (if running directly)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

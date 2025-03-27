import os
import random
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ CORS Middleware (Change `allow_origins` in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"message": "Carbon Crunch API is running!"}

@app.post("/analyze")
def analyze_code(code_input: CodeInput):
    code = code_input.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    overall_score = random.randint(50, 100)
    breakdown = {
        "naming": random.randint(5, 20),
        "modularity": random.randint(5, 20),
        "comments": random.randint(5, 20),
        "formatting": random.randint(5, 20),
        "reusability": random.randint(5, 20),
        "best_practices": random.randint(5, 20),
    }
    recommendations = [
        "Avoid deeply nested components in your React render logic.",
        "Refactor long functions for better readability.",
        "Use consistent variable naming conventions.",
    ]

    return {
        "overall_score": overall_score,
        "breakdown": breakdown,
        "recommendations": recommendations[:2],  # Show top 2 recommendations
    }

# ✅ Run Uvicorn server properly with dynamic port
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Get PORT from env, default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)


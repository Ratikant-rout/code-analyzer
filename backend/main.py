import os
import random
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update if needed
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

    # ✅ Generate breakdown scores dynamically
    breakdown = {
        "naming": random.randint(5, 80),
        "modularity": random.randint(5, 20),
        "comments": random.randint(5, 50),
        "formatting": random.randint(5, 90),
        "reusability": random.randint(5, 95),
        "best_practices": random.randint(5, 99),
    }

    # ✅ Calculate overall score
    overall_score = sum(breakdown.values()) // len(breakdown)

    # ✅ Generate recommendations based on weakest areas
    recommendations_list = {
        "naming": "Use meaningful variable and function names.",
        "modularity": "Break large functions into smaller, reusable ones.",
        "comments": "Ensure your code has sufficient comments for clarity.",
        "formatting": "Follow consistent indentation and styling conventions.",
        "reusability": "Use functions and classes to avoid redundant code.",
        "best_practices": "Follow industry best practices such as DRY and SOLID principles.",
    }
    
    weakest_areas = sorted(breakdown, key=breakdown.get)[:2]
    recommendations = [recommendations_list[area] for area in weakest_areas]

    return {
        "overall_score": overall_score,
        "breakdown": breakdown,
        "recommendations": recommendations,
    }

# ✅ Ensure backend runs correctly
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Render dynamically assigns a PORT
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)

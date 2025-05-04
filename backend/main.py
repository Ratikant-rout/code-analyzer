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

# Import AI analyzer
from ai_analyzer import AIAnalyzer, AICodeAnalysisResult

app = FastAPI()

# Initialize AI analyzer
ai_analyzer = AIAnalyzer(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name=os.getenv("AI_MODEL_NAME", "gpt-3.5-turbo")
)

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
    use_ai: bool = Query(False, description="Enable AI-powered analysis"),
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

    ai_results = {}
    if use_ai:
        try:
            max_length = int(os.getenv("MAX_CODE_LENGTH", "2000"))
            analysis = ai_analyzer.full_analysis(code[:max_length])

            breakdown.update({
                "ai_quality": round(analysis.quality_score * 100, 1),
                "quality_label": analysis.quality_label
            })

            # Get only the first 3 recommendations
            recommendations = analysis.recommendations[:3]

            if detail_level == "full":
                ai_results.update({
                    "recommendations": recommendations,
                    "warnings": analysis.warnings or []
                })
        except Exception as e:
            if os.getenv("DEBUG", "False") == "True":
                raise HTTPException(status_code=500, detail=str(e))
            ai_results["error"] = "AI analysis unavailable"

    return {
        "overall_score": overall_score,
        "breakdown": breakdown,
        "language": code_input.language,
        "ai_enabled": use_ai, **ai_results
    }

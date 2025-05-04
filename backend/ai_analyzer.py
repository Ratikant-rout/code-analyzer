from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
import os

app = FastAPI()


class AICodeAnalysisResult(BaseModel):
    quality_score: float
    quality_label: str
    recommendations: List[str]
    warnings: Optional[List[str]] = []


class AIAnalyzer:
    def __init__(self, openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
        openai.api_key = openai_api_key
        self.model_name = model_name

    def full_analysis(self, code: str) -> AICodeAnalysisResult:
        prompt = (
            "Analyze the following code and provide a detailed analysis:\n"
            "1. A quality score (0 to 1)\n"
            "2. A short quality label (e.g., Poor, Average, Excellent)\n"
            "3. Recommendations for improving code quality (organized as bullet points)\n"
            "4. Warnings or potential issues (organized as bullet points)\n"
            "5. Categorize suggestions as 'Performance', 'Security', 'Readability', or 'Best Practices' if applicable\n\n"
            f"Code:\n```python\n{code}\n```"
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=700
            )
            content = response['choices'][0]['message']['content']
            lines = content.strip().split("\n")

            quality_score = float(lines[0].split(":")[-1].strip())
            quality_label = lines[1].split(":")[-1].strip()

            recommendations = []
            warnings = []
            for line in lines:
                if line.startswith("- "):
                    if "warning" in line.lower():
                        warnings.append(line.strip("- ").strip())
                    else:
                        recommendations.append(line.strip("- ").strip())

            return AICodeAnalysisResult(
                quality_score=quality_score,
                quality_label=quality_label,
                recommendations=recommendations[:3],
                warnings=warnings
            )

        except Exception as e:
            print(f"Error analyzing code: {e}")
            return AICodeAnalysisResult(
                quality_score=0.0,
                quality_label="Error",
                recommendations=["Failed to analyze code."],
                warnings=[]
            )


# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OpenAI API Key in environment variable 'OPENAI_API_KEY'.")

ai_analyzer = AIAnalyzer(openai_api_key=OPENAI_API_KEY)


class CodeInput(BaseModel):
    code: str


@app.post("/api/analyze", response_model=AICodeAnalysisResult)
def analyze_code(input: CodeInput):
    try:
        return ai_analyzer.full_analysis(input.code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

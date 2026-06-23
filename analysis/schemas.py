from typing import Literal

from pydantic import BaseModel, Field


class TextIssue(BaseModel):
    type: Literal["spelling", "grammar", "suspicious_phrasing"]
    original: str
    suggestion: str = ""
    reason: str = ""


class TextAnalysisResult(BaseModel):
    errors: list[TextIssue] = Field(default_factory=list)


class ModelBenchmarkResult(BaseModel):
    model: str
    catalog_name: str
    description: str
    prior_score: float
    json_score: float
    latency_seconds: float
    latency_score: float
    total_score: float
    installed: bool
    valid_json: bool
    error: str = ""


class ModelSelection(BaseModel):
    model: str
    language: str
    rationale: str
    benchmarks: list[ModelBenchmarkResult] = Field(default_factory=list)
    candidates_compared: int = 0

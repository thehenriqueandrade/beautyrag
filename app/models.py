from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    question: str
    max_results: Optional[int] = 4

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    tokens_used: int
    latency_ms: int
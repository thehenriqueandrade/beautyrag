from fastapi import FastAPI, HTTPException
from app.models import AskRequest, AskResponse
from app.rag_pipeline import run_rag

app = FastAPI(
    title="BeautyRAG API",
    description="Assistente de marketing para profissionais de beleza, baseado em RAG.",
    version="1.0.0"
)

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "service": "BeautyRAG"}

@app.post("/api/v1/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    result = run_rag(question=request.question, max_results=request.max_results)
    return AskResponse(**result)
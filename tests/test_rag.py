from app.rag_pipeline import run_rag

def test_rag_returns_answer():
    result = run_rag("Como precificar meus servicos?", max_results=2)
    assert "answer" in result
    assert len(result["answer"]) > 30
    assert len(result["sources"]) > 0

def test_rag_sources_are_known_files():
    known_files = [
        "captacao_clientes.md",
        "scripts_whatsapp.md",
        "precificacao_servicos.md",
        "estrategia_instagram.md",
        "retencao_clientes.md"
    ]
    result = run_rag("Como reter clientes?", max_results=3)
    for source in result["sources"]:
        assert source in known_files
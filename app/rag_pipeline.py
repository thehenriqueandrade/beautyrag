import os
import time
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

SYSTEM_PROMPT = """Você é um consultor especialista em marketing para profissionais 
de beleza autônomos como nail designers, lash designers e esteticistas.

Responda com base APENAS no contexto fornecido abaixo. Se a resposta não estiver 
no contexto, diga que não tem essa informação na base de conhecimento.

Seja direto, prático e use linguagem acessível. Quando relevante, sugira ações concretas.

Contexto:
{context}"""

def get_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(
        persist_directory=os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db"),
        collection_name=os.getenv("COLLECTION_NAME", "beauty_marketing_docs"),
        embedding_function=embeddings
    )

def run_rag(question: str, max_results: int = 4) -> dict:
    start = time.time()

    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(question, k=max_results)

    context = "\n\n---\n\n".join([d.page_content for d in docs])
    sources = list(set([d.metadata.get("source", "unknown") for d in docs]))

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}")
    ])
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "question": question})

    latency_ms = int((time.time() - start) * 1000)
    tokens_used = len(context.split()) + len(question.split()) + len(answer.split())

    return {
        "answer": answer,
        "sources": sources,
        "tokens_used": tokens_used,
        "latency_ms": latency_ms
    }
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    persist_directory=os.getenv("CHROMA_PERSIST_DIR"),
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings
)

results = vectorstore.similarity_search("como responder cliente perguntando preco no WhatsApp", k=3)
for r in results:
    print(f"\n📄 Fonte: {r.metadata['source']}")
    print(r.page_content[:200])

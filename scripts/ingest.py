import os
import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DOCS_DIR = "./data/raw"
CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
COLLECTION = os.getenv("COLLECTION_NAME", "beauty_marketing_docs")


def load_documents(docs_dir: str):
    documents = []
    for filepath in glob.glob(f"{docs_dir}/*.md"):
        loader = TextLoader(filepath, encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = os.path.basename(filepath)
        documents.extend(docs)
    print(f"✅ {len(documents)} documento(s) carregado(s)")
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ {len(chunks)} chunks gerados")
    return chunks


def index_documents(chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION
    )
    print(f"✅ Indexação concluída em {CHROMA_DIR}")
    return vectorstore


def main():
    print("🚀 Iniciando ingestão de documentos...")
    documents = load_documents(DOCS_DIR)
    chunks = split_documents(documents)
    index_documents(chunks)
    print("🎉 Base de conhecimento pronta!")


if __name__ == "__main__":
    main()
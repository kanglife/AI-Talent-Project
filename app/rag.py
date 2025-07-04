# RAG 구성 (FAISS or Chroma)
# RAG: 퀀트 논문과 시장 보고서 임베딩, FAISS/ChromaDB 기반 검색

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings


load_dotenv()

DATA_DIR = "data"
VECTOR_DB_PATH = "vector_db"

def get_embedding():
    api_key = os.getenv("AOAI_API_KEY")
    endpoint = os.getenv("AOAI_ENDPOINT")
    deployment = os.getenv("AOAI_DEPLOY_EMBED_3_LARGE")
    version = os.getenv("AOAI_API_VERSION", "2024-05-01-preview")

    if not all([api_key, endpoint, deployment]):
        raise ValueError("❌ .env 환경변수가 누락되었습니다.")

    return AzureOpenAIEmbeddings(
        azure_deployment=deployment,
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=version
    )


# def load_finance_docs():
#     docs = []
#     if not os.path.exists(DATA_DIR):
#         return docs
#     for fname in os.listdir(DATA_DIR):
#         if fname.endswith(".txt"):
#             loader = TextLoader(os.path.join(DATA_DIR, fname), encoding="utf-8")
#             loaded_docs = loader.load()
#             splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
#             docs += splitter.split_documents(loaded_docs)
#     return docs

def load_finance_docs():
    loader = DirectoryLoader("data", glob="**/*.txt", show_progress=True)
    documents = loader.load()

    # 메타데이터 추가 (예: 폴더명을 category로)
    for doc in documents:
        category = doc.metadata.get("source", "").split(os.sep)[-2]  # 예: data/news/xxx.txt → news
        doc.metadata["category"] = category

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
    return splitter.split_documents(documents)


def create_vector_db(docs):
    embedding = get_embedding()
    db = FAISS.from_documents(docs, embedding)
    db.save_local(VECTOR_DB_PATH)
    return db

def load_vector_db():
    embedding = get_embedding()
    return FAISS.load_local(VECTOR_DB_PATH, embedding, allow_dangerous_deserialization=True)

# def rag_search(query, db):
#     results = db.similarity_search(query, k=3)
#     return "\n\n---\n\n".join([doc.page_content for doc in results])

def rag_search(query, db, category_filter=None):
    if category_filter and category_filter != "전체":
        docs = db.similarity_search(query, k=3, filter={"category": category_filter})
    else:
        docs = db.similarity_search(query, k=3)
    return "\n\n---\n\n".join([doc.page_content for doc in docs])

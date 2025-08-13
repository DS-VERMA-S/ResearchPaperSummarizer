from __future__ import annotations

import math
from typing import List, Tuple

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.config import EMBEDDING_API_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, get_openai_model, get_openai_api_key


def load_pdf_documents(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", ".", " "]
    )
    return splitter.split_documents(documents)


class LocalEmbeddingIndex:
    def __init__(self, documents, embeddings: List[List[float]], embedder: OpenAIEmbeddings):
        self.documents = documents
        self.embeddings = [normalize_vector(vec) for vec in embeddings]
        self.embedder = embedder

    def as_retriever(self, k: int):
        index = self

        class _Retriever:
            def get_relevant_documents(self, query: str):
                query_vec = normalize_vector(index.embedder.embed_query(query))
                scores = [cosine_similarity(query_vec, doc_vec) for doc_vec in index.embeddings]
                top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
                return [index.documents[i] for i in top_indices]

        return _Retriever()


def build_local_index_from_docs(documents) -> LocalEmbeddingIndex:
    embedder = OpenAIEmbeddings(model=EMBEDDING_API_MODEL)
    texts = [d.page_content for d in documents]
    vectors = embedder.embed_documents(texts)
    index = LocalEmbeddingIndex(documents=documents, embeddings=vectors, embedder=embedder)
    return index


def cosine_similarity(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def vector_norm(a: List[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def normalize_vector(a: List[float]) -> List[float]:
    n = vector_norm(a)
    return [x / n if n else 0.0 for x in a]


def get_llm(temperature: float = 0.2):
    model = get_openai_model()
    get_openai_api_key(required=True)
    return ChatOpenAI(model=model, temperature=temperature)


def join_context_with_citations(docs: List) -> str:
    parts: List[str] = []
    for d in docs:
        page = d.metadata.get("page")
        page_note = f" [page {page}]" if page is not None else ""
        text = d.page_content.strip()
        parts.append(f"{text}{page_note}")
    return "\n\n".join(parts)
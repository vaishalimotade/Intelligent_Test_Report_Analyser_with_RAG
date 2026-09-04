import os
import hashlib
import json
import re
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .embedding_service import get_embeddings


def get_vector_store():
    persist_directory = os.getenv("CHROMADB_DIR", "/data/chromadb")
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=get_embeddings(),
    )


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _chunk_failure(record: Dict[str, Any]) -> List[str]:
    failure = record.get("failure_reason") or "Unknown failure"
    trace = record.get("stack_trace") or "Not available"
    structured_chunks = [
        f"Test Name: {record.get('test_name') or 'Unknown test'}\nFinal Status: failed\nError Summary: {failure}",
        f"Technical Context\nStack Traces / Exception Logs: {trace}",
    ]
    chunks = [chunk for chunk in structured_chunks if chunk.strip()]
    max_chars = int(os.getenv("RAG_CHUNK_MAX_CHARS", "4000"))
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=max_chars,
        chunk_overlap=min(200, max_chars // 10),
        length_function=len,
    )
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chars:
            final_chunks.append(chunk)
            continue
        final_chunks.extend(splitter.split_text(chunk))
    return final_chunks


async def index_failure_records(records: List[Dict[str, Any]]) -> None:
    failures = [record for record in records if record.get("status") == "failed"]
    if not failures:
        return
    documents = []
    ids = []
    namespace = os.getenv("RAG_NAMESPACE", "test-report-analyzer")
    for record in failures:
        parent_id = str(record.get("_id"))
        for chunk_index, chunk_text in enumerate(_chunk_failure(record)):
            content_hash = hashlib.sha256(_normalize_text(chunk_text).encode("utf-8")).hexdigest()
            child_id = f"{namespace}:{content_hash}"
            ids.append(child_id)
            documents.append(
                Document(
                    page_content=chunk_text,
                    metadata={
                        "namespace": namespace,
                        "mongo_id": parent_id,
                        "mongo_ids": json.dumps([parent_id]),
                        "chunk_index": chunk_index,
                        "content_hash": content_hash,
                        "test_name": record.get("test_name") or "Unknown test",
                        "module_name": record.get("module_name") or "Unknown feature",
                        "pipeline": record.get("pipeline") or "Unknown pipeline",
                        "build_number": record.get("build_number") or "Unknown build",
                        "run_id": record.get("run_id") or "Unknown run",
                        "timestamp": record["timestamp"].isoformat(),
                    },
                )
            )
    vector_store = get_vector_store()
    existing = vector_store.get(ids=ids, include=["metadatas"]) if ids else {"ids": [], "metadatas": []}
    existing_ids = set(existing.get("ids", []))
    existing_metadata = dict(zip(existing.get("ids", []), existing.get("metadatas", [])))
    for child_id in existing_ids:
        metadata = existing_metadata.get(child_id) or {}
        parent_ids = set(json.loads(metadata.get("mongo_ids", "[]")))
        parent_ids.add(metadata.get("mongo_id"))
        parent_ids.discard(None)
        parent_ids.add(next((document.metadata["mongo_id"] for document, current_id in zip(documents, ids) if current_id == child_id), ""))
        parent_ids.discard("")
        if hasattr(vector_store, "_collection"):
            vector_store._collection.update(
                ids=[child_id],
                metadatas=[{**metadata, "mongo_ids": json.dumps(sorted(parent_ids))}],
            )
    new_documents = [document for document, child_id in zip(documents, ids) if child_id not in existing_ids]
    new_ids = [child_id for child_id in ids if child_id not in existing_ids]
    if new_documents:
        vector_store.add_documents(new_documents, ids=new_ids)

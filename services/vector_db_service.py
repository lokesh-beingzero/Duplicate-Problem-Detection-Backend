import chromadb
from config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(name=COLLECTION_NAME)

def add_to_db(normalized_text, req):
    collection.add(
        documents=[normalized_text],
        metadatas=[{
            "slug": req.slug,
            "title": req.title,
            "description": req.description,
            "inputFormat": req.inputFormat,
            "outputFormat": req.outputFormat,
            "constraints": req.constraints,
            "tags": ", ".join(req.tags)
        }],
        ids=[req.slug]
    )

def query_db(embedding, top_k=5):
    return collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
import chromadb

CHROMA_PATH = "./chroma_db"   # your path
COLLECTION_NAME = "coding_problems"

def get_embedding_by_slug(slug):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    result = collection.get(
        ids=[slug],
        include=["embeddings"]
    )

    if not result["ids"]:
        print("Problem not found")
        return None

    embedding = result["embeddings"][0]

    print("Embedding length:", len(embedding))
    print("First 10 values:", embedding[:10])

    return embedding


# Example usage
embedding = get_embedding_by_slug("list-cycle")

print("embeddings = ", embedding)
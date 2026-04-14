import lancedb
import pyarrow as pa
from config import LANCE_PATH, TABLE_NAME

def get_embedding_by_slug(slug):
    # Connect to the database
    db = lancedb.connect(LANCE_PATH)
    
    # Check if table exists to avoid errors
    if TABLE_NAME not in db.table_names():
        print(f"Table '{TABLE_NAME}' not found.")
        return None

    table = db.open_table(TABLE_NAME)

    # Search for the row where 'slug' matches. 
    # LanceDB uses SQL-like filtering for metadata.
    result = table.search().where(f"slug = '{slug}'").to_list()

    if not result:
        print("Problem not found")
        return None

    # In LanceDB, the vector column is typically named 'vector'
    # but it depends on what you named it during 'add_to_db'
    embedding = result[0].get("vector")

    if embedding is None:
        print("Embedding data missing for this record")
        return None

    print("Embedding length:", len(embedding))
    print("First 10 values:", embedding[:10])

    return embedding

# Example usage
embedding = get_embedding_by_slug("list-cycle")
print("embeddings =", embedding)
import lancedb
import pandas as pd
from config import LANCE_PATH, TABLE_NAME

db = lancedb.connect(LANCE_PATH)

def add_to_db(normalized_text, req, embedding):
    data = [{
        "vector": embedding,
        "text": normalized_text,
        "id": req.slug,
        "slug": req.slug,
        "title": req.title,
        "description": req.description,
        "inputFormat": req.inputFormat,
        "outputFormat": req.outputFormat,
        "constraints": req.constraints,
        "tags": ", ".join(req.tags)
    }]

    # Open existing table or create a new one if it doesn't exist
    if TABLE_NAME in db.table_names():
        table = db.open_table(TABLE_NAME)
        table.add(data)
    else:
        # Initial creation infers the schema from the first data batch
        db.create_table(TABLE_NAME, data=data)

def query_db(embedding, top_k=5):
    if TABLE_NAME not in db.table_names():
        return []
    
    table = db.open_table(TABLE_NAME)
    
    # LanceDB uses a fluent API for searching
    results = (
        table.search(embedding)
        .limit(top_k)
        .to_list()
    )

    print('results = ', results)
    return results
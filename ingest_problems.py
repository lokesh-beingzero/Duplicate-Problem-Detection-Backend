import json
import time
from services.embedding_service import get_embedding
from services.llm_service import normalize_problem 
from services.vector_db_service import add_to_db
from routes.problem_routes import build_problem_text
from pydantic import BaseModel
from typing import List

class AddProblemSchema(BaseModel):
    title: str
    slug: str
    description: str
    constraints: str
    inputFormat: str
    outputFormat: str
    tags: List[str]

def ingest_problems(json_file):
    with open(json_file, "r") as f:
        problems = json.load(f)

    for idx, prob_dict in enumerate(problems):
        try:
            prob = AddProblemSchema(**prob_dict)
            problem_text = build_problem_text(prob)

            # Respecting your rate limit/delay
            time.sleep(4)

            # 1. Get the clean text
            normalized = normalize_problem(problem_text)
            
            # 2. Generate the actual vector (REQUIRED for LanceDB)
            # Replace this with whatever function you use to get the float list
            embedding = get_embedding(normalized)

            # 3. Pass both to your updated vector_db_service
            add_to_db(normalized, prob, embedding)

            print(f"[{idx+1}] Inserted: {prob.slug}")

        except Exception as e:
            print(f"[{idx+1}] Failed: {prob_dict.get('slug')} → {e}")

if __name__ == "__main__":
    ingest_problems("mentorpick_problems.json")
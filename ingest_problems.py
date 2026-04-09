import json
import time
from services.llm_service import normalize_problem
from services.vector_db_service import add_to_db
from routes.problem_routes import build_problem_text
from pydantic import BaseModel
from typing import List

# Reuse schema
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

            time.sleep(4)

            normalized = normalize_problem(problem_text)

            add_to_db(normalized, prob)

            print(f"[{idx+1}] Inserted: {prob.slug}")

        except Exception as e:
            print(f"[{idx+1}] Failed: {prob_dict.get('slug')} → {e}")


if __name__ == "__main__":
    ingest_problems("mentorpick_problems.json")
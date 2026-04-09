from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from services.llm_service import normalize_problem
from services.embedding_service import get_embedding
from services.vector_db_service import add_to_db, query_db

router = APIRouter()

class AddProblemSchema(BaseModel):
    slug: str
    title: str
    description: str
    constraints: str
    inputFormat: str
    outputFormat: str
    tags: List[str]

class DuplicateProblemSchema(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    constraints: Optional[str] = ""
    inputFormat: Optional[str] = ""
    outputFormat: Optional[str] = ""
    tags: Optional[List[str]] = []

def build_problem_text(req: AddProblemSchema) -> str:
    return f"""
TITLE:
{req.title}

DESCRIPTION:
{req.description}

CONSTRAINTS:
{req.constraints}

INPUT FORMAT:
{req.inputFormat}

OUTPUT FORMAT:
{req.outputFormat}

TAGS:
{", ".join(req.tags)}
"""

@router.post("/add-problem")
def add_problem(prob: AddProblemSchema):
    problem_text = build_problem_text(prob)

    normalized = normalize_problem(problem_text)

    print('normalized problem ', normalized)

    add_to_db(normalized, prob)

    return {
        "slug": prob.slug,
        "status": "stored"
    }

@router.post("/check-duplicate")
def check_duplicate(prob: DuplicateProblemSchema):
    if not any([
        prob.title,
        prob.description,
        prob.constraints,
        prob.inputFormat,
        prob.outputFormat,
        prob.tags
    ]):
        return {"error": "At least one field must be provided"}
    
    problem_text = build_problem_text(prob)

    normalized = normalize_problem(problem_text)

    print('normalized = \n', normalized)

    embedding = get_embedding(normalized)

    results = query_db(embedding)

    matches = []

    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]

        similarity = round(1 - distance, 4)

        matches.append({
            "slug": metadata["slug"],
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "similarity": similarity
        })

    return {
        "matches": matches
    }
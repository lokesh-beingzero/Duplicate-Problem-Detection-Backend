from google import genai
from config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

models = client.models.list()

# print("models supported by gemini")

# for m in models:
#     print(m.name)

def normalize_problem(problem_text: str) -> str:
    prompt = f"""
Convert this programming problem into its core computational task. Anaylyse the story present in the problem statement and only find mathematical computation from the story.

Remove story and keep only:
- Task
- Inputs
- Output
- Category

Only give me four outputs
1. Task
2. Input
3. Output
4. Category of the problem

Explain the input and output in one or two sentences. The category can have multiple values based on the description of the problem. Don't give anything else in the output.

Example 1:
Problem Data:

Title: "Ram and Shyam"
Description: "Ram and Shyam are two friends. Their ages is given as input. Find the sum of their ages"
Constraints: "1 <= T <= 100. 1 <= A, B <= 100
InputFormat: "First line of input contains a single integer T, Where T is number of Test Cases. First line of each Test Case contains two space separated integers denoting the age of Ram and Shyam"
OutputFormat: "Print the sum of their ages in a new line"
Tags: "math, bruteforce"

Expected Output:
1. Task - Find the sum of two integers.
2. Input - Two integers are given as input
3. Ouput - Print the sum of two integers in a new line.
4. Category - math and bruteforce

Problem:
{problem_text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()
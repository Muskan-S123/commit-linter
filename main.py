from fastapi import FastAPI
from pydantic import BaseModel
from analyse import analyse_commit, get_git_diff, get_commit_message

app = FastAPI()

class CommitInput(BaseModel):
    diff: str | None = None
    message: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyse")
def analyse(input: CommitInput):
    result = analyse_commit(input.diff, input.message)
    return {"verdict": result}
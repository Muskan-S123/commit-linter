import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from git_utils import get_git_diff, get_commit_message
load_dotenv()
def analyse_commit(diff:str|None=None, message:str|None=None):
    if diff is None:
        diff=get_git_diff()
    if message is None:
        message=get_commit_message()

    if not diff:
        return "No changes to analyze"
    llm=ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )
    prompt = f"""You are a commit message linter. Judge ONLY the commit message against the rules below — do not require the message to mention every file changed in the diff.

Commit message: "{message}"

Diff (for context only, to check the message isn't misleading):
{diff}

Rules — FAIL only if one of these is clearly violated:
1. Message is in imperative mood ("Add X", not "Added X" or "Adds X").
2. Message is under 72 characters for the summary line.
3. Message describes the main change and is not vague (e.g. "fix stuff", "updates", "changes").
4. Message is not misleading — it must not claim something the diff doesn't do.

Do NOT fail a message just because it omits a secondary or incidental change (e.g. a file rename, a minor refactor) as long as it accurately describes the primary change.

Respond in EXACTLY this format, nothing else:
VERDICT: PASS OR VERDICT: FAIL
REASON: one sentence, citing which rule (1-4) was violated if FAIL"""
    response=llm.invoke(prompt)
    if isinstance(response.content,list):
        return "".join(
            block.get("text","") for block in response.content
            if isinstance(block,dict) and block.get("type") == "text"
        )
    return response.content
if __name__ == "__main__":
    result = analyse_commit()
    print(result)


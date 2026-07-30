import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from git_utils import get_git_diff, get_commit_message
load_dotenv()
def analyse_commit():
    diff=get_git_diff()
    message=get_commit_message()
    if not diff:
        return "No changes to analyze"
    llm=ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )
    prompt= f"""You are a strict code reviewer analyze a git commit.
commit message:"{message}"
Diff:
{diff}
Judge whether the commit message accurately describes the diff, and whether the message follows good commit message conventions (clear, descriptive, imperative mood).
Respond in EXACTLY this format nothing else:
VERDICT: PASS OR VERDICT: FAIL
REASON:one or two sentences of reasoning"""
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


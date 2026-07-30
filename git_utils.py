import subprocess
def get_git_diff():
    result=subprocess.run(
        ["git","diff","--staged"],
        capture_output=True,
        text=True
    )
    return result.stdout
def get_commit_message():
    with open(".git/COMMIT_EDITMSG","r") as f:
        return f.read().strip()
    
if __name__=="__main__":
    diff=get_git_diff()
    print(diff)
    message=get_commit_message()
    print(message)





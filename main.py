from fastapi import FastAPI
app=FastAPI()

@app.get("/health")
def health():
    return {"status":"ok"}

#test change
#checking
#checking2
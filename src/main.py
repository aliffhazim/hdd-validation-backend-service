from fastapi import FastAPI

app = FastAPI(title="HDD Validation Backend Service")


@app.get("/health")
def health():
    return {"status": "ok"}

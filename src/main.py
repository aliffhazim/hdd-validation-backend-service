from fastapi import FastAPI, HTTPException, UploadFile

from src.parser import parse_log

ALLOWED_EXTENSIONS = (".log", ".txt")

app = FastAPI(title="HDD Validation Backend Service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/validate-log")
def validate_log(file: UploadFile):
    filename = (file.filename or "").lower()
    if not filename.endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Only .log and .txt files are accepted",
        )
    lines = (raw.decode("utf-8", errors="replace") for raw in file.file)
    result = parse_log(lines)
    return {
        "message": "Log analyzed",
        "metadata": {
            "filename": file.filename,
            "lines_processed": result["lines_processed"],
        },
        "analytics_data": {
            "status": result["status"],
            "max_temperature_c": result["max_temperature_c"],
            "errors_found": result["errors_found"],
        },
    }

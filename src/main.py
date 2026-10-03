from fastapi import FastAPI, UploadFile

from src.parser import parse_log

app = FastAPI(title="HDD Validation Backend Service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/validate-log")
def validate_log(file: UploadFile):
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

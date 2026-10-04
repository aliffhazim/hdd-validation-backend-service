from pathlib import Path

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)
FIXTURES = Path(__file__).parent.parent / "test_fixtures"


def upload(name):
    with open(FIXTURES / name, "rb") as f:
        return client.post("/api/v1/validate-log", files={"file": (name, f)})


def test_upload_pass_log():
    response = upload("sample_pass.log")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_data"]["status"] == "PASS"
    assert data["analytics_data"]["max_temperature_c"] == 44
    assert data["analytics_data"]["errors_found"] == []
    assert data["metadata"]["lines_processed"] == 8


def test_upload_fail_log():
    response = upload("sample_fail.log")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_data"]["status"] == "FAIL"
    assert data["analytics_data"]["max_temperature_c"] == 61
    assert len(data["analytics_data"]["errors_found"]) == 4
    assert data["metadata"]["lines_processed"] == 12


def test_rejects_unsupported_extension():
    response = client.post(
        "/api/v1/validate-log",
        files={"file": ("notes.exe", b"not a log")},
    )
    assert response.status_code == 400
    assert "Only .log and .txt" in response.json()["detail"]

from pathlib import Path

from src.parser import parse_log

FIXTURES = Path(__file__).parent.parent / "test_fixtures"


def test_pass_log():
    with open(FIXTURES / "sample_pass.log") as f:
        result = parse_log(f)
    assert result["status"] == "PASS"
    assert result["max_temperature_c"] == 44
    assert result["errors_found"] == []
    assert result["lines_processed"] == 8


def test_fail_log():
    with open(FIXTURES / "sample_fail.log") as f:
        result = parse_log(f)
    assert result["status"] == "FAIL"
    assert result["max_temperature_c"] == 61
    assert result["lines_processed"] == 12
    assert len(result["errors_found"]) == 4
    assert result["errors_found"][0]["type"] == "BAD_SECTOR"
    assert result["errors_found"][0]["line"] == 6
    assert result["errors_found"][-1]["type"] == "CRITICAL"
    assert result["errors_found"][-1]["line"] == 11


def test_empty_input():
    result = parse_log([])
    assert result["status"] == "PASS"
    assert result["max_temperature_c"] is None
    assert result["errors_found"] == []
    assert result["lines_processed"] == 0

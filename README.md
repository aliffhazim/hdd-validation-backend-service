# hdd-validation-backend-service

![tests](https://github.com/aliffhazim/hdd-validation-backend-service/actions/workflows/ci.yml/badge.svg)

A small Python backend that reads a hard drive test log and returns PASS or FAIL, the highest temperature, and any faults with their line numbers.

> Learning project on synthetic logs with an invented format. It is not connected to any real tester or company data.

## The problem

Test rigs write long log files after every run. Engineers open them one by one and search for errors by hand, which is slow and easy to get wrong. This service turns that into one API call. (Illustrative scenario, not real company data.)

## What it does

- Upload a `.log` or `.txt` file and get back the status, the highest temperature, and every fault with its line number
- Rejects any other file type with HTTP 400

## How it works

```
curl or browser upload
        |
        v
  src/main.py     checks the file type, calls the parser, builds the JSON
        |
        v
  src/parser.py   reads the log one line at a time and returns the results
```

The parser has no web code in it, so it can be tested on its own.

## Log format (invented for this project)

```
2026-10-01 02:10:41 TEMP_CELSIUS: 47
2026-10-01 02:14:07 [BAD_SECTOR] LBA 48213 unreadable
2026-10-01 02:16:02 [TIMEOUT] Controller did not respond within 30s
2026-10-01 02:25:03 [CRITICAL] Firmware assertion failed in write path
```

Rule: if a log contains any `[BAD_SECTOR]`, `[TIMEOUT]` or `[CRITICAL]` line, the status is FAIL. Otherwise it is PASS.

## Run it

Tested on Python 3.12 (Ubuntu 24.04).

```bash
git clone https://github.com/aliffhazim/hdd-validation-backend-service.git
cd hdd-validation-backend-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app
```

The service runs at http://127.0.0.1:8000. Open http://127.0.0.1:8000/docs for a page with an upload button.

## Try it

```bash
curl -s -F "file=@test_fixtures/sample_fail.log" http://127.0.0.1:8000/api/v1/validate-log
```

Response:

```json
{
  "message": "Log analyzed",
  "metadata": {"filename": "sample_fail.log", "lines_processed": 12},
  "analytics_data": {
    "status": "FAIL",
    "max_temperature_c": 61,
    "errors_found": [
      {"type": "BAD_SECTOR", "line": 6, "details": "LBA 48213 unreadable"},
      {"type": "TIMEOUT", "line": 8, "details": "Controller did not respond within 30s"},
      {"type": "BAD_SECTOR", "line": 10, "details": "LBA 90417 unreadable"},
      {"type": "CRITICAL", "line": 11, "details": "Firmware assertion failed in write path"}
    ]
  }
}
```

Uploading an unsupported file type returns HTTP 400:

```json
{"detail": "Only .log and .txt files are accepted"}
```

## Expected results

| File | Status | Max temp | Faults | Lines |
|---|---|---|---|---|
| sample_pass.log | PASS | 44 | 0 | 8 |
| sample_fail.log | FAIL | 61 | 4 | 12 |

## Run the tests

```bash
python -m pytest
```

6 tests cover the parser and the API. GitHub Actions runs them on every push.

## Limitations

- Logs are synthetic and the format is invented
- The file type check looks only at the file name, so renaming a file to `.log` gets past it. This is a basic guard, not real security
- No file size limit
- Only three fault types are recognised
- A malformed temperature line such as `TEMP_CELSIUS: abc` is not handled and makes the request fail with HTTP 500
- Results are not stored anywhere

## Next steps

- Handle malformed temperature readings and add a test for it
- Add a file size limit
- Store results in SQLite and add a summary endpoint
- Add Docker
- Measure speed and memory on a large generated log before making any performance claims

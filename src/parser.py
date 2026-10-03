FAULT_TAGS = ["[BAD_SECTOR]", "[TIMEOUT]", "[CRITICAL]"]


def parse_log(lines):
    status = "PASS"
    for line in lines:
        for tag in FAULT_TAGS:
            if tag in line:
                status = "FAIL"
    return {"status": status}

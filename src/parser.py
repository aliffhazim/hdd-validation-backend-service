FAULT_TAGS = ["[BAD_SECTOR]", "[TIMEOUT]", "[CRITICAL]"]
TEMP_KEY = "TEMP_CELSIUS:"


def parse_log(lines):
    status = "PASS"
    max_temp = None
    for line in lines:
        for tag in FAULT_TAGS:
            if tag in line:
                status = "FAIL"
        if TEMP_KEY in line:
            temp = int(line.split(TEMP_KEY)[1].strip())
            if max_temp is None or temp > max_temp:
                max_temp = temp
    return {"status": status, "max_temperature_c": max_temp}

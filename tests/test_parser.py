from data_validation.parser import parse_log_line

def run_tests():
    valid_logs = [
        "2025-07-20 10:23:45.123 2931 INFO nova.compute.manager [req-abc123] Starting instance: instance-001",
        "2025-07-20 10:23:46 2931 ERROR nova.scheduler.utils [req-ghi789] Error scheduling instance: instance-003",
        "2025-07-20 10:23:47.321 1001 DEBUG glance.api.v2.image_data Uploading image data"
    ]

    invalid_logs = [
        "July 20th nova-compute failed to start",
        "2025/07/20 nova-scheduler::ERROR -- instance launch failed",
        "[ERROR] Something bad happened!"
    ]

    print("\nValid Log Tests:")
    for log in valid_logs:
        try:
            parsed = parse_log_line(log)
            print(f"PASS: {parsed}")
        except Exception as e:
            print(f"FAIL: {log} => {e}")

    print("\nInvalid Log Tests:")
    for log in invalid_logs:
        try:
            parse_log_line(log)
            print(f"FAIL: {log} => Should have failed")
        except Exception as e:
            print(f"PASS: {log} => {e}")

if __name__ == "__main__":
    run_tests()

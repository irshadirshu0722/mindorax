import os
import socket
import sys
import time


def wait_for(host: str, port: int, service_name: str, timeout: int) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"{service_name} is reachable on {host}:{port}")
                return
        except OSError:
            print(f"waiting for {service_name} on {host}:{port} ...")
            time.sleep(2)

    raise TimeoutError(f"Timed out waiting for {service_name} on {host}:{port}")


def main() -> int:
    timeout = int(os.getenv("SERVICE_WAIT_TIMEOUT", "120"))
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = int(os.getenv("DB_PORT", "5432"))
    redis_host = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))

    try:
        wait_for(db_host, db_port, "postgres", timeout)
        wait_for(redis_host, redis_port, "redis", timeout)
    except TimeoutError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

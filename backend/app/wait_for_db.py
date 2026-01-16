import os
import time

import psycopg2


def main() -> None:
    url = os.environ["DATABASE_URL"]
    url = url.replace("postgresql+psycopg2://", "postgresql://", 1)
    deadline = time.time() + 20

    while True:
        try:
            conn = psycopg2.connect(url)
            conn.close()
            print("DB is ready")
            return
        except Exception as e:
            if time.time() > deadline:
                raise RuntimeError(f"DB not ready after timeout: {e}") from e
            print("Waiting for DB...")
            time.sleep(1)


if __name__ == "__main__":
    main()
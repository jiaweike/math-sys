import os

from redis import Redis
from rq import Connection, Worker


QUEUE_NAMES = ["default", "render"]


def main() -> None:
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    conn = Redis.from_url(redis_url)

    with Connection(conn):
        worker = Worker(QUEUE_NAMES)
        worker.work(with_scheduler=False)


if __name__ == "__main__":
    main()

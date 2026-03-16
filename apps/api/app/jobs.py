import os
from typing import Any


def enqueue_render(trace_payload: dict[str, Any]) -> str:
    try:
        from redis import Redis
        from rq import Queue
    except ModuleNotFoundError as exc:
        raise RuntimeError("queue dependencies not installed") from exc

    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    conn = Redis.from_url(redis_url)
    queue = Queue("render", connection=conn)
    job = queue.enqueue("tasks.render_trace_job", trace_payload)
    return job.id


def get_job_status(job_id: str) -> dict[str, Any]:
    try:
        from redis import Redis
        from rq.job import Job
    except ModuleNotFoundError as exc:
        raise RuntimeError("queue dependencies not installed") from exc

    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    conn = Redis.from_url(redis_url)
    job = Job.fetch(job_id, connection=conn)

    payload: dict[str, Any] = {
        "job_id": job.id,
        "status": job.get_status(),
        "enqueued_at": str(job.enqueued_at) if job.enqueued_at else None,
        "ended_at": str(job.ended_at) if job.ended_at else None,
    }

    if job.result is not None:
        payload["result"] = job.result
    if job.exc_info:
        payload["error"] = job.exc_info.splitlines()[-1]

    return payload

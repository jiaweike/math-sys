# worker

Background worker for async jobs.

Current queues:

- `render`: handles trace render jobs (`tasks.render_trace_job`)
- `default`: reserved for future ingest/embedding jobs

## Notes

- MVP renderer stores trace JSON as artifact placeholder.
- V1 will replace placeholder with manim/ffmpeg pipeline.

# Docker

Deploy your dotflow pipeline with Docker and Docker Compose.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image with your pipeline |
| `docker-compose.yml` | Service definition for local or production use |

## Deploy

```bash
docker compose build
docker compose up
```

## Important

- Do not rename `workflow.py` or the `main()` function — the Dockerfile CMD depends on it

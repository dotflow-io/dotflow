# Docker

Deploy your dotflow pipeline with Docker and Docker Compose.

## Create project

```bash
dotflow init
# Select cloud: docker
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform docker
```

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

# GitHub Actions

Run your dotflow pipeline on a schedule or manually using GitHub Actions as the runtime.

## Create project

```bash
dotflow init
# Select cloud: github-actions
```

## Generated files

| File | Description |
|------|-------------|
| `.github/workflows/dotflow.yml` | Workflow with cron schedule and manual trigger |

## Deploy

Push to GitHub — the pipeline runs automatically on the configured schedule.

```bash
git init && git add . && git commit -m "initial"
gh repo create my_pipeline --push --source .
```

## View logs

Go to your repository > **Actions** tab > select the workflow run.

## Important

- Cron uses **UTC timezone**
- Minimum interval is 5 minutes
- `workflow_dispatch` allows manual trigger from the GitHub UI

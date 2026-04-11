# GitHub Actions

Run your dotflow pipeline on a schedule or manually using GitHub Actions as the runtime.

## Create project

```bash
dotflow init
# Select cloud: github-actions
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform github-actions
```

## Generated files

| File | Description |
|------|-------------|
| `.github/workflows/dotflow.yml` | Workflow with cron schedule and manual trigger |

## Prerequisites

- `pip install dotflow[deploy-github]`
- GitHub token: `export GITHUB_TOKEN=$(gh auth token)`

## Deploy

### Option 1: dotflow deploy

```bash
dotflow deploy --platform github-actions --project my_pipeline
```

Creates a private repo on GitHub, pushes all project files, and GitHub Actions runs automatically.

### Option 2: Manual

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
- No secrets or credentials needed unless your pipeline uses external services

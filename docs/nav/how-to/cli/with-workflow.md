# With Workflow

The `start` command supports two mutually exclusive entry points:

| Flag | When to use |
|------|-------------|
| `--step` / `-s` | Run a single `@action`-decorated function |
| `--workflow` / `-w` | Run a factory that returns a `DotFlow` instance |

## Single step

```bash
dotflow start --step docs_src.cli.cli_with_workflow.step_one
```

## Full workflow factory

The factory must be a plain callable (no `@action`) that returns a configured
`DotFlow` — the CLI is responsible for calling `.start()`.

```bash
dotflow start --workflow docs_src.cli.cli_with_workflow.pipeline
```

```bash
dotflow start --workflow docs_src.cli.cli_with_workflow.pipeline --mode parallel
```

{* ./docs_src/cli/cli_with_workflow.py *}

/// note
Passing both `--step` and `--workflow` at the same time is an error.
///

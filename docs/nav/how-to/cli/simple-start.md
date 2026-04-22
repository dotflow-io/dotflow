# Simple Start

Run a single step from the command line.

```bash
dotflow start --step docs_src.basic.simple_cli:simple_step
```

{* ./docs_src/basic/simple_cli.py *}

/// note
`--step` runs a single `@action` function. To run a full multi-step pipeline, use [`--workflow`](with-workflow.md) instead.
///

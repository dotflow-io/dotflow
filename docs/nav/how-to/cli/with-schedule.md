# With Schedule

```bash
dotflow schedule --step docs_src.cli.cli_schedule.extract --cron "*/5 * * * *"
```

```bash
dotflow schedule --step docs_src.cli.cli_schedule.extract --cron "0 6 * * *" --resume
```

```bash
dotflow schedule --step docs_src.cli.cli_schedule.extract --cron "*/5 * * * *" --overlap queue
```

```bash
dotflow schedule --step docs_src.cli.cli_schedule.extract --cron "0 * * * *" --mode parallel --overlap parallel
```

{* ./docs_src/cli/cli_schedule.py *}

from os import system

from dotflow import action


@action
def extract():
    return {"data": "fetched"}


@action
def load(previous_context):
    return {"saved": previous_context.storage}


def main():
    system(
        "dotflow schedule --step docs_src.cli.cli_schedule.extract --cron '*/5 * * * *'"
    )
    system(
        "dotflow schedule --step docs_src.cli.cli_schedule.extract --cron '0 6 * * *' --resume"
    )
    system(
        "dotflow schedule --step docs_src.cli.cli_schedule.extract --cron '*/5 * * * *' --overlap queue"
    )
    system(
        "dotflow schedule --step docs_src.cli.cli_schedule.extract "
        "--cron '0 * * * *' --mode parallel --overlap parallel"
    )


if __name__ == "__main__":
    main()

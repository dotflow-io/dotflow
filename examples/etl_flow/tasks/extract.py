from dotflow import action

from requests import get  # type: ignore


@action(retry=5)
def extract(initial_context):
    return get(initial_context.storage).text

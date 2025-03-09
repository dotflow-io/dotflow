from dotflow import action

from bs4 import BeautifulSoup  # type: ignore

from examples.etl_flow.book import Book


@action
class Transform:

    @action(retry=1)
    def text_html_parser(self, previous_context):
        soup = BeautifulSoup(
            previous_context.storage,
            features="html.parser"
        )

        return soup

    @action(retry=1)
    def transform_to_dict(self, previous_context):
        html = previous_context.storage
        new_dict = {
            "title": html.title.text,
            "author": html.find(id="author").text
        }

        return new_dict

    @action
    def transform_model(self, previous_context):
        return Book(**previous_context.storage).model_dump_json()

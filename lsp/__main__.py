import logging

from pygls.lsp.server import LanguageServer
from lsprotocol import types

logging.basicConfig(filename='pygls.log', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)

server = LanguageServer("example-server", "v0.1")

@server.feature(
    types.TEXT_DOCUMENT_DID_CHANGE
)
def did_change(params: types.DidChangeTextDocumentParams):
    logger.info(f"get did change {params}")
    logger.info(f"type did change {type(params)}")

@server.feature(
    types.TEXT_DOCUMENT_COMPLETION,
    types.CompletionOptions(trigger_characters=["."]),
)
def completions(params: types.CompletionParams):
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()

    if not current_line.endswith("hello."):
        return []

    return [
        types.CompletionItem(label="world"),
        types.CompletionItem(label="friends"),
    ]


if __name__ == "__main__":
    server.start_io()



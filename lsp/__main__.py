import logging

from lsprotocol import types
from pygls.lsp.server import LanguageServer

logging.basicConfig(filename="pygls.log", filemode="w", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting LSP 1")

server = LanguageServer("example-server", "v0.1")


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: types.DidChangeTextDocumentParams):
    logger.info(f"get did change {params}")
    logger.info(f"type did change {type(params)}")
    if params.content_changes:
        first_content_change = params.content_changes[0]
        if isinstance(first_content_change, types.TextDocumentContentChangePartial):
            diagnostics_end = first_content_change.range.start
        else:
            diagnostics_end = types.Position(line=0, character=3)

        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=params.text_document.uri,
                diagnostics=[
                    types.Diagnostic(
                        message="Testing Diag",
                        severity=types.DiagnosticSeverity.Error,
                        range=types.Range(
                            start=types.Position(line=0, character=0),
                            end=diagnostics_end,
                        ),
                    )
                ],
            )
        )


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
    logger.info("Starting LSP 2")
    server.start_io()

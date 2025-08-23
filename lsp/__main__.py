import logging

from tree_sitter import Range
from lsp.parser import parser
from typing import cast

from lsprotocol import types
from pygls.lsp.server import LanguageServer

from lsp.ctx import VALUE_OBJ, ChiContext, ChiError, ChiDataObject

logging.basicConfig(filename="pygls.log", filemode="w", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting LSP 1")

server = LanguageServer("example-server", "v0.1")

@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def document_did_open(ls: LanguageServer, params: types.DidChangeTextDocumentParams):
    logger.info(f"get did open {params.text_document.uri}")
    update(ls, params.text_document.uri)

@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: types.DidChangeTextDocumentParams):
    logger.info(f"get did change {params.text_document.uri}")
    update(ls, params.text_document.uri)

def update(ls: LanguageServer, uri: str):
    document = ls.workspace.get_text_document(uri)
    tree = parser.parse(document.source.encode())
    ctx = ChiContext(tree)
    obj = ctx.evualate_tree(tree.root_node)
    if obj.is_error():
        error = cast(ChiError, obj)
        diag = types.Diagnostic(
            message=error.message,
            severity=types.DiagnosticSeverity.Error,
            range=convert_range(error.range),
        )
    else:
        value = obj.chi_call(VALUE_OBJ)
        if value.is_error():
            diag = types.Diagnostic(
                message="Value has no value",
                severity=types.DiagnosticSeverity.Warning,
                range=convert_range(tree.root_node.range),
            )
        else:
            value = cast(ChiDataObject, value)
            diag = types.Diagnostic(
                message=f"Success !!!: {value.chi_data}",
                severity=types.DiagnosticSeverity.Hint,
                range=convert_range(tree.root_node.range),
            )
    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=document.uri,
            diagnostics=[diag],
        )
    )


def convert_range(_range: Range) -> types.Range:
    return types.Range(
        start=types.Position(
            line=_range.start_point.row, character=_range.start_point.column
        ),
        end=types.Position(
            line=_range.end_point.row, character=_range.end_point.column
        ),
    )


if __name__ == "__main__":
    logger.info("Starting LSP 2")
    server.start_io()

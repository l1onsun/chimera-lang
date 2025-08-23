
from typing import Any

from tree_sitter import Range
from lsp.object import ChiDataObject


def static_obj(value: Any):
    return ChiDataObject(Range((0, 0), (0, 0), 0, 0), value)

VALUE_KEY = "value"
VALUE_OBJ = static_obj(VALUE_KEY)
PLUS_KEY = b"+"
PLUS_OBJ = static_obj(PLUS_KEY)

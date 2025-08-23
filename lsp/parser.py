import enum

import tree_sitter_chimera as tschimera
from tree_sitter import Language, Parser

parser = Parser(Language(tschimera.language()))


class TreeSitterTypes(enum.StrEnum):
    source_file = "source_file"
    binnary_expression = "binnary_expression"
    const_value = "const_value"
    const_string = "const_string"
    const_number = "const_number"

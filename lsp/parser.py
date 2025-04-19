import tree_sitter_walktime as tswalk
from tree_sitter import Language, Parser

parser = Parser(Language(tswalk.language()))

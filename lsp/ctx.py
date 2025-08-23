import logging
from dataclasses import dataclass
from typing import cast

from tree_sitter import Node, Range, Tree

from lsp.object import ChiObject, ChiError, ChiDataObject
from lsp.object_helpers import PLUS_KEY, VALUE_KEY, VALUE_OBJ, static_obj
from lsp.parser import TreeSitterTypes

logger = logging.getLogger(__name__)



@dataclass
class ChiContext:
    ts_tree: Tree

    def evualate_tree(self, node: Node | None) -> ChiObject:
        if node is None:
            return ChiError(self.ts_tree.root_node.range, "Got None as tree")
        match node.type:
            case TreeSitterTypes.source_file | TreeSitterTypes.const_value:
                return self.evualate_tree(node.child(0))
            case TreeSitterTypes.binnary_expression:
                return self.binary_operator(node)
            case TreeSitterTypes.const_number:
                if not node.text:
                    return ChiError(node.range, "Invalid number -> no text")
                try:
                    value = int(node.text)
                except Exception as exc:
                    return ChiError(node.range, f"Can't parse number: {exc}")
                return create_number_object(node.range, value)
            case TreeSitterTypes.const_number:
                return ChiError(node.range, "Strings are not supported")
        return ChiError(node.range, "Not Implemented")

    def binary_operator(self, binary_exp: Node) -> ChiObject:
        logger.warning(f"bin opeRATION: {binary_exp.text}")
        left = binary_exp.child(0)
        operator = binary_exp.child(1)
        right = binary_exp.child(2)
        partial_operator = self.evualate_tree(left).chi_call(
            ChiDataObject(operator.range, operator.text)
            if operator
            else ChiError(binary_exp.range, "Not enough children")
        )
        if partial_operator.is_error():
            return partial_operator
        return partial_operator.chi_call(self.evualate_tree(right))


def create_number_object(range: Range, value: int) -> ChiObject:

    def plus(other: ChiObject) -> ChiObject:
        other_value_obj = other.chi_call(VALUE_OBJ)
        if other_value_obj.is_error():
            return other_value_obj
        other_value_obj = cast(ChiDataObject, other_value_obj)
        return create_number_object(range, cast(int, other_value_obj.chi_data) + value)

    return ChiDataObject(
        range,
        chi_data=lambda obj: {
            VALUE_KEY: static_obj(value),
            PLUS_KEY: static_obj(plus),
        }[obj.chi_data],
    )


# type BinaryOperatorRealization = Callable[[ChiContext, Node, Node], ChiBase]
# def binary_operator(name: str) -> Callable[[BinaryOperatorRealization], BinaryOperatorRealization]:
#     def decorator(func: BinaryOperatorRealization) -> BinaryOperatorRealization:
#         ...
#     return decorator

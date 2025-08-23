import logging
from dataclasses import dataclass
from typing import Any

from tree_sitter import Range

logger = logging.getLogger(__name__)


class ChiObject:
    def is_error(self) -> bool:
        raise NotImplementedError

    def chi_call(self, arg: "ChiObject") -> "ChiObject":
        raise NotImplementedError


@dataclass
class ChiDataObject(ChiObject):
    range: Range
    chi_data: Any

    def __post_init__(self):
        logger.warning(f"Created {self.chi_data}")

    def chi_call(self, arg: ChiObject) -> ChiObject:
        if not callable(self.chi_data):
            return ChiError(self.range, f"Object {self.chi_data} is not callable")
        try:
            res = self.chi_data(arg)
            if isinstance(res, ChiObject):
                return res
            else:
                return ChiError(
                    self.range,
                    f"Operation {self.chi_data} returned: {res} instead of ChiObject",
                )
        except Exception as exc:
            logger.exception("Got exception")
            return ChiError(self.range, f"Got exception: {type(exc)}: {exc}")

    def is_error(self) -> bool:
        return False

    def __hash__(self) -> int:
        return self.chi_data.__hash__()


@dataclass
class ChiError(ChiObject):
    range: Range
    message: str

    def is_error(self) -> bool:
        return True

    def chi_call(self, arg: ChiObject) -> ChiObject:
        return self

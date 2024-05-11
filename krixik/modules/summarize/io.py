from dataclasses import dataclass
from typing import Any, Literal, Optional


@dataclass
class InputStructure:
    format: Literal["text"] = "text"
    filename: str = "input_text.txt"
    process_key: None = None

    @property
    def data_example(self):
        return "sample text looks like this."

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None


@dataclass
class OutputStructure:
    format: Literal["text"] = "text"
    filename: str = "input_text.txt"
    process_key: None = None

    @property
    def data_example(self):
        return "sample text looks like this."

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

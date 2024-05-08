from dataclasses import dataclass, field
from typing import Literal
import numpy as np


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
    format: Literal["db"] = "db"
    filename: str = "output_index.db"
    process_key: None = None

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

    @property
    def data_example(self):
        return None

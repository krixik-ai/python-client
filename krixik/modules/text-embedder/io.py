from dataclasses import dataclass, field
from typing import Literal, Optional, Any, List
import numpy as np


@dataclass
class InputStructure:
    format: Literal["json"] = "json"
    filename: str = "filename_example.json"
    process_key: str = "snippet"
    snippet: str = "This is the main text."
    line_numbers: List[int] = field(default_factory=lambda: [1, 2, 3, 4])
    other: Optional[Any] = None

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

    @property
    def data_example(self):
        return {
            "snippet": self.snippet,
            "line_numbers": self.line_numbers,
            "other": self.other,
        }


@dataclass
class OutputStructure:
    format: Literal["npy"] = "npy"
    filename: str = "output_data.npy"
    process_key: str = "data"
    data: np.ndarray = field(default_factory=lambda: np.array([1, 2, 3]))

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

    @property
    def data_example(self):
        return self.data

from dataclasses import dataclass, field
from typing import Literal, List, Optional, Any


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

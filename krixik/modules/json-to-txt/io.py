from dataclasses import dataclass
from typing import Literal, Optional, Any


@dataclass
class InputStructure:
    format: Literal["json"] = "json"
    filename: str = "filename_example.json"
    process_key: str = "snippet"
    snippet: str = "This is the main text."
    other: Optional[Any] = None

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

    @property
    def data_example(self):
        return {
            "snippet": self.snippet,
            "other": self.other,
        }


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

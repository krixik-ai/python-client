from dataclasses import dataclass
from typing import Any, Literal, Optional


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

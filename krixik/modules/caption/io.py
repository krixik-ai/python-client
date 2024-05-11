from dataclasses import dataclass
from typing import Literal, Any, Optional


@dataclass
class InputStructure:
    format: Literal["image"] = "image"
    filename: str = "input_image.jpg"
    process_key: None = None

    @property
    def data_example(self):
        return None

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None


@dataclass
class OutputStructure:
    format: Literal["json"] = "json"
    filename: str = "filename_example.json"
    process_key: str = "caption"
    caption: str = "This is the caption text."
    other: Optional[Any] = None

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

    @property
    def data_example(self):
        return {
            "caption": self.caption,
            "other": self.other,
        }

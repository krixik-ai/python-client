from dataclasses import dataclass, field
from typing import Literal
import numpy as np


@dataclass
class InputStructure:
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


@dataclass
class OutputStructure:
    format: Literal["faiss"] = "faiss"
    filename: str = "output_index.faiss"
    process_key: None = None

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

    @property
    def data_example(self):
        return None

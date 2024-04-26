from typing import Dict, Any, Callable
from dataclasses import dataclass


@dataclass
class ModelSelection:
    model_selection: Dict[Dict[str, str], Dict[str, Any]]
    model_setup: Callable

    def __post_init__(self):
        self.setup_result = self.model_setup(self.model_selection)

    def get_setup_result(self):
        return self.setup_result

from krixik.modules.utilities.decorators import type_check_inputs
from krixik.__base__ import library_base_dir
from pathlib import Path
import pytest
import importlib

parser = importlib.import_module("krixik.modules.parser")
parser_module_config = parser.module_config
parser_default_model = parser_module_config["default_model"]
parser_default_params = parser_module_config["default_params"]

text_embedder = importlib.import_module("krixik.modules.text-embedder")
text_embedder_module_config = text_embedder.module_config
text_embedder_default_model = text_embedder_module_config["default_model"]
text_embedder_default_params = text_embedder_module_config["default_params"]

core_path = Path(library_base_dir)
parent_path = core_path.parent.absolute()


file_name = "tesFFt.txt"
symbolic_file_path = "/home/user/test.txt"
local_file_path = f"{parent_path}/tests/test_files/text/1984_short.txt"
pipeline_ordered_modules = ["parser", "text-embedder"]


class MyClass:
    def __init__(self, pipeline_ordered_modules):
        self.pipeline_ordered_modules = pipeline_ordered_modules

    @type_check_inputs
    def my_method(
        self,
        *,
        modules: dict,
        file_name: str,
        local_file_path: str,
        symbolic_file_path: str,
        verbose: bool = False,
    ):
        return modules


test_success_data = [
    {
        "parser": {"model": "sentence"},
        "text-embedder": {},
    },
    {"parser": {"model": "sentence"}},
    {
        "text-embedder": {
            "model": text_embedder_default_model,
        }
    },
    {},
]

true_hydrated_pipeline = {
    "module_1": {"model": parser_default_model, "params": parser_default_params},
    "module_2": {
        "model": text_embedder_default_model,
        "params": text_embedder_default_params,
    },
}


@pytest.mark.parametrize("test_modules", test_success_data)
def test_module_hydration_success(test_modules):
    """
    short test of module decorator - tests that
    - modules are properly hydrated under test conditions
    """
    instance = MyClass(pipeline_ordered_modules=pipeline_ordered_modules)
    
    print(f"test_modules {test_modules}")
    
    hydrated_modules = instance.my_method(
        modules=test_modules,
        file_name=file_name,
        local_file_path=local_file_path,
        symbolic_file_path=symbolic_file_path,
    )
    
    assert hydrated_modules == true_hydrated_pipeline


import os
from krixik.pipeline_examples.single_module.utilities import generate_examples
from krixik.modules import available_modules


def test_generate_examples():
    generate_examples.generate()
    for module_name in available_modules:
        assert os.path.exists(f"{generate_examples.save_directory}/{module_name}.yml") is True

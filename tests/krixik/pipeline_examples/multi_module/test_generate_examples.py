
import os
from krixik.pipeline_examples.multi_module.utilities import generate_examples
from krixik.pipeline_examples.multi_module.utilities import multi_module_pipeline_examples


def test_generate_examples():
    pipeline_names = [v["name"] for v in multi_module_pipeline_examples]
    generate_examples.generate()
    for pipeline_name in pipeline_names:
        assert os.path.exists(f"{generate_examples.save_directory}/{pipeline_name}.yml") is True

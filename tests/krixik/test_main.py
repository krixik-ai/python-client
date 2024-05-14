from krixik import krixik
from tests.krixik import pipeline_configs_path
from tests.krixik import text_files_path
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import BuildPipeline
import pytest

module_1 = Module(module_type="parser")
test_pipeline = BuildPipeline(name='temp-parser-pipeline',
                               module_chain=[module_1])
test_config = pipeline_configs_path + "parser.yml"

test_fail_data = [
    None,
    1,
    '/this/path/has/no/extension',
    '/this/path/has/invalid/extension.txt'
]


failure_tests = [
    (None, None), # both input cannot be None
    ('/this/path/has/no/extension', None), # invalid config
    (text_files_path + "1984_short.txt", None), # invalid config
    (None, 1),  # invalid BuildPipeline object
]


@pytest.mark.parametrize(("config_path", "pipeline"), failure_tests)
def test_1(config_path, pipeline):
    """load_pipeline failure tests for krixik main"""
    with pytest.raises((TypeError, ValueError, FileExistsError)):
        krixik.load_pipeline(config_path=config_path, pipeline=pipeline)

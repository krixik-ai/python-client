from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import BuildPipeline
from krixik.pipeline_builder.utilities.chain_checker import MAX_MODULES
from tests.krixik import text_files_path, audio_files_path
import os
import yaml
import pytest


test_failure_data = [
    ["vector-db", "text-embedder"],
    ["parser", "vector-db"],
]


@pytest.mark.parametrize("module_names", test_failure_data)
def test_1(module_names):
    """failure test for BuildPipeline class - invalid module chain"""
    module_chain = [Module(module_name) for module_name in module_names]
    with pytest.raises((Exception, ValueError)):
        BuildPipeline(module_chain=module_chain)


test_success_data = [
    ["parser", "text-embedder", "vector-db"],
    ["transcribe", "translate"],
]


@pytest.mark.parametrize("module_names", test_success_data)
def test_2(module_names):
    """success test for BuildPipeline class - valid module chain"""
    module_chain = [Module(module_name) for module_name in module_names]
    BuildPipeline(module_chain=module_chain)


test_failure_local_paths = [
    (
        ["parser", "text-embedder", "vector-db"],
        text_files_path + "not a real file.txt",
    ),
    (
        ["parser", "text-embedder", "vector-db"],
        audio_files_path + "Is AI Actually Useful short.mp3",
    ),
    (["transcribe", "translate"], text_files_path + "1984_short.txt"),
    (["transcribe", "translate"], []),
    (["transcribe", "translate"], 1),

]


@pytest.mark.parametrize("module_names, local_file_path", test_failure_local_paths)
def test_3(module_names, local_file_path):
    """failure test for BuildPipeline class - invalid test_input"""
    module_chain = [Module(module_name) for module_name in module_names]
    pipeline = BuildPipeline(module_chain=module_chain)
    with pytest.raises((TypeError, ValueError, FileNotFoundError, Exception)):
        pipeline.test_input(local_file_path=local_file_path)


test_success_local_paths = [
    (
        ["parser", "text-embedder", "vector-db"],
        text_files_path + "1984_short.txt",
    ),
    (
        ["transcribe", "translate"],
        audio_files_path + "valid_1.mp3",
    ),
]


@pytest.mark.parametrize("module_names, local_file_path", test_success_local_paths)
def test_4(module_names, local_file_path):
    """success test for BuildPipeline class - test_input"""
    module_chain = [Module(module_name) for module_name in module_names]
    pipeline = BuildPipeline(module_chain=module_chain)
    pipeline.test_input(local_file_path=local_file_path)


test_success_local_paths = [
    (
        ["parser", "text-embedder", "vector-db"],
        "vector-db-pipeline.yml",
    ),
]


@pytest.mark.parametrize("module_names, config_path", test_success_local_paths)
def test_5(module_names, config_path):
    """success test for BuildPipeline class - save, load pipeline and ensure data properties are same"""
    module_chain = [Module(module_name) for module_name in module_names]
    pipeline_v1 = BuildPipeline(module_chain=module_chain)

    with pytest.raises((ValueError)):  # no pipeline name given
        pipeline_v1.save(config_path=config_path)

    pipeline_v1.name = "test_pipeline"
    pipeline_v1.save(config_path=config_path)

    pipeline_v2 = BuildPipeline(config_path=config_path)

    assert pipeline_v1.module_chain == pipeline_v2.module_chain
    assert (
        pipeline_v1.module_chain_output_process_keys
        == pipeline_v2.module_chain_output_process_keys
    )
    assert pipeline_v1.name == pipeline_v2.name
    assert pipeline_v1.config == pipeline_v2.config

    os.remove(config_path)


def test_6():
    """ test that MAX_MODULES is obeyed"""
    module_names = ['parser'] * (MAX_MODULES + 1)
    module_chain = [Module(module_name) for module_name in module_names]
    with pytest.raises(ValueError):
        BuildPipeline(name="my_pipeline", module_chain=module_chain)
        

test_fail_data = [
    [],
    "",
    "a"*65,
    1
]

@pytest.mark.parametrize("name", test_fail_data)
def test_7(name):
    """fail test that pipeline input name obeys basic type checking"""
    with pytest.raises((TypeError, ValueError)):
        BuildPipeline(name=name)


test_fail_data = [
    {},
    [],
    [1],
    [True],
    1
]

@pytest.mark.parametrize("chain", test_fail_data)
def test_8(chain):
    """fail test that pipeline module_chain obeys basic type checking"""
    with pytest.raises((TypeError, ValueError)):
        BuildPipeline(module_chain=chain)


test_fail_data = [
    {},
    [],
    1,
    audio_files_path + "valid_1.mp3",
    text_files_path + "1984_short.txt"
]

@pytest.mark.parametrize("config", test_fail_data)
def test_9(config):
    """fail test that pipeline config obeys basic type checking"""
    with pytest.raises((TypeError, ValueError, yaml.YAMLError)):
        BuildPipeline(config_path=config)


test_fail_data = [
    {},
    [],
    1,
]

@pytest.mark.parametrize("fake_module", test_fail_data)
def test_10(fake_module):
    """try to add module that is not proper Module object"""
    with pytest.raises((TypeError)):
        pipeline = BuildPipeline()
        pipeline._add(fake_module)
        
        
test_fail_data = [
    None,
    1,
    '/this/path/has/no/extension',
    '/this/path/has/invalid/extension.txt'
]

@pytest.mark.parametrize("fake_module", test_fail_data)
def test_11(fake_module):
    """try to add module that is not proper Module object"""
    with pytest.raises((TypeError)):
        pipeline = BuildPipeline()
        pipeline._add(fake_module)
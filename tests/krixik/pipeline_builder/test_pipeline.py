from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline, MAX_MODULES
from tests.krixik import text_files_path, audio_files_path
import os
import pytest


test_failure_data = [
    ["vector-search", "text-embedder"],
    ["parser", "vector-search"],
]


@pytest.mark.parametrize("module_names", test_failure_data)
def test_1(module_names):
    """failure test for CreatePipeline class - invalid module chain"""
    module_chain = [Module(module_name) for module_name in module_names]
    with pytest.raises((Exception, ValueError)):
        CreatePipeline(module_chain=module_chain)


test_success_data = [
    ["parser", "text-embedder", "vector-search"],
    ["transcribe", "translate"],
]


@pytest.mark.parametrize("module_names", test_success_data)
def test_2(module_names):
    """success test for CreatePipeline class - valid module chain"""
    module_chain = [Module(module_name) for module_name in module_names]
    CreatePipeline(module_chain=module_chain)


test_failure_local_paths = [
    (
        ["parser", "text-embedder", "vector-search"],
        text_files_path + "not a real file.txt",
    ),
    (
        ["parser", "text-embedder", "vector-search"],
        audio_files_path + "Is AI Actually Useful short.mp3",
    ),
    (["transcribe", "translate"], text_files_path + "1984_short.txt"),
]


@pytest.mark.parametrize("module_names, local_file_path", test_failure_local_paths)
def test_3(module_names, local_file_path):
    """failure test for CreatePipeline class - invalid test_input"""
    module_chain = [Module(module_name) for module_name in module_names]
    pipeline = CreatePipeline(module_chain=module_chain)
    with pytest.raises((TypeError, ValueError, FileNotFoundError, Exception)):
        pipeline.test_input(local_file_path=local_file_path)


test_success_local_paths = [
    (
        ["parser", "text-embedder", "vector-search"],
        text_files_path + "1984_short.txt",
    ),
    (
        ["transcribe", "translate"],
        audio_files_path + "valid_1.mp3",
    ),
]


@pytest.mark.parametrize("module_names, local_file_path", test_success_local_paths)
def test_4(module_names, local_file_path):
    """success test for CreatePipeline class - test_input"""
    module_chain = [Module(module_name) for module_name in module_names]
    pipeline = CreatePipeline(module_chain=module_chain)
    pipeline.test_input(local_file_path=local_file_path)


test_success_local_paths = [
    (
        ["parser", "text-embedder", "vector-search"],
        "vector-search-pipeline.yml",
    ),
]


@pytest.mark.parametrize("module_names, config_path", test_success_local_paths)
def test_5(module_names, config_path):
    """success test for CreatePipeline class - save, load pipeline and ensure data properties are same"""
    module_chain = [Module(module_name) for module_name in module_names]
    pipeline_v1 = CreatePipeline(module_chain=module_chain)

    with pytest.raises((ValueError)):  # no pipeline name given
        pipeline_v1.save(config_path=config_path)

    pipeline_v1.name = "test_pipeline"
    pipeline_v1.save(config_path=config_path)

    pipeline_v2 = CreatePipeline(config_path=config_path)

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
        CreatePipeline(module_chain=module_chain)
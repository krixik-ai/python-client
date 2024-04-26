from krixik.modules.utilities.module_selections import (
    pipeline_selection_setup,
)
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


test_failuare_data = [
    {  # pipeline_ordered_modules is not a list
        "pipeline_ordered_modules": "not-a-module",
        "module_selections": {
            "not-a-module": {"model": "bert", "params": {"quantize": 1}}
        },
    },
    {  # module_selections is not a dictionary
        "pipeline_ordered_modules": ["text-embedder"],
        "module_selections": "not-a-dictionary",
    },
    {  # module_selections does not have the same number of keys as pipeline_ordered_modules
        "pipeline_ordered_modules": ["text-embedder"],
        "module_selections": {
            "not-a-module": {"model": "bert", "params": {"quantize": 1}}
        },
    },
    {  # module_selections has a key that is not in pipeline_ordered_modules
        "pipeline_ordered_modules": ["text-embedder"],
        "module_selections": {
            "not-a-module": {"model": "bert", "params": {"quantize": 1}}
        },
    },
    {  # module_selections has a key that is not in available_modules
        "pipeline_ordered_modules": ["text-embedder"],
        "module_selections": {
            "text-embedder": {"model": "bert", "params": {"quantize": 1}},
            "not-a-module": {"model": "bert", "params": {"quantize": 1}},
        },
    },
    {  # module_selections model is not in available_models
        "pipeline_ordered_modules": ["text-embedder"],
        "module_selections": {
            "text-embedder": {"model": "not-a-model", "params": {"quantize": 1}}
        },
    },
    {  # module_selections params is not in the required form
        "pipeline_ordered_modules": ["text-embedder"],
        "module_selections": {
            "text-embedder": {"model": "bert", "params": {"quantize": 1}}
        },
    },
]


@pytest.mark.parametrize("test_data", test_failuare_data)
def test_failure(test_data):
    with pytest.raises(ValueError):
        pipeline_selection_setup(
            test_data["pipeline_ordered_modules"], test_data["module_selections"]
        )


test_success_data = [
    [
        {
            "parser": {"model": "sentence"},
            "text-embedder": {},
        }
    ]
]

true_hydrated_pipeline = {
    "parser": {"model": parser_default_model, "params": parser_default_params},
    "text-embedder": {
        "model": text_embedder_default_model,
        "params": text_embedder_default_params,
    },
}


@pytest.mark.parametrize("test_data", test_success_data)
def test_success_1(test_data):
    hydrated_pipeline_selections = pipeline_selection_setup(
        list(test_data[0].keys()), test_data[0]
    )
    assert hydrated_pipeline_selections == true_hydrated_pipeline


test_success_data = [
    (
        ["parser", "text-embedder"],
        {"parser": {"model": "sentence"}},
    ),
    (
        ["parser", "text-embedder"],
        {},
    ),
]


@pytest.mark.parametrize("test_data", test_success_data)
def test_success_2(test_data):
    hydrated_pipeline_selections = pipeline_selection_setup(test_data[0], test_data[1])
    assert hydrated_pipeline_selections == true_hydrated_pipeline

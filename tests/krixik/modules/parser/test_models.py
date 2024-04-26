import importlib
import pytest
from krixik.modules.parser import module_config
from krixik.modules.parser.params import (
    CHUNK_SIZE_MIN,
    CHUNK_SIZE_MAX,
    OVERLAP_SIZE_MIN,
)
from krixik.modules.parser.models import model_selection_setup

test_data = importlib.import_module("tests.krixik.modules")
baseline_test_failue_data = test_data.baseline_failure_model_data
available_models = module_config["available_models"]
default_model = module_config["default_model"]
default_params = module_config["default_params"]


failure_test_data = baseline_test_failue_data + [
    {
        "model": "fixed",
        "params": {"chunk_size": CHUNK_SIZE_MIN - 1, "overlap_size": OVERLAP_SIZE_MIN},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": CHUNK_SIZE_MAX + 1, "overlap_size": OVERLAP_SIZE_MIN},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": CHUNK_SIZE_MIN, "overlap_size": OVERLAP_SIZE_MIN - 1},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": CHUNK_SIZE_MIN, "overlap_size": CHUNK_SIZE_MIN + 1},
    },
    {
        "model": "fixed",
        "params": {"bobs your uncle"},
    },
    {
        "model": "fixed",
        "params": {"bobs your uncle": 10, "overlap_size": 5},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": "10", "overlap_size": 5},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": [], "overlap_size": 5},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": CHUNK_SIZE_MAX + 1, "overlap_size": 5},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": 5, "overlap_size": 6},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": 5, "overlap_size": -1},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": 0, "overlap_size": 0},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": float(CHUNK_SIZE_MAX - 1), "overlap_size": 1},
    },
    {
        "model": "fixed",
        "params": {"chunk_size": CHUNK_SIZE_MAX + 1, "overlap_size": 1.0},
    },
    {
        "model": "fixed",
        "params": {
            "chunk_size": CHUNK_SIZE_MAX - 1,
            "overlap-size": 1,
            "overlap_size": 1,
        },
    },
    {
        "model": "fixed",
        "params": {"chunk_size": CHUNK_SIZE_MAX - 1},
    },
    {
        "model": "fixed",
        "params": "hi there",
    },
    {
        "model": "fixed",
        "params": 1.0,
    },
    {
        "model": "fixed",
        "params": 1,
    },
    {
        "model": "fixed",
        "params": {"chunk_size": 5, "overlap_size": 6},
    },
]


@pytest.mark.parametrize("test_data", failure_test_data)
def test_1(test_data):
    with pytest.raises((ValueError, TypeError)):
        model_selection_setup(test_data)


test_success_data = [
    {"model": "sentence", "params": {}},
    {"model": "fixed", "params": {"chunk_size": 10, "overlap_size": 2 }},
]


@pytest.mark.parametrize("test_data", test_success_data)
def test_2(test_data):
    instance = model_selection_setup(test_data)
    assert instance.get_setup_result() == test_data

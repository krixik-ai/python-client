
from tests.krixik.pipeline_examples.single_module.utilities.setup import prep_pipeline_and_data, run_test
import pytest

module_name = "json-to-txt"
all_setup_data = prep_pipeline_and_data(module_name)

@pytest.mark.parametrize("setup_data", all_setup_data)
def test_1(setup_data):
    """ test single module pipeline """
    pipeline, test_file, module_selection = setup_data
    run_test(module_name, module_selection, pipeline, test_file)

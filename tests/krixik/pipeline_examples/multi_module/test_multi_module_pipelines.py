from tests.krixik.pipeline_examples.multi_module.utilities.test_data import test_data
from tests.krixik.pipeline_examples.multi_module.utilities.setup import run_test
import pytest

pipeline_examples = list(test_data.keys())


@pytest.mark.parametrize("pipeline", pipeline_examples)
def test_pipeline(pipeline):
    """ test multi module pipeline """
    print("\n")
    print(f"Running test for {pipeline}")
    run_test(pipeline)

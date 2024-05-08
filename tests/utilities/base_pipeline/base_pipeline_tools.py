from tabnanny import check
from tests import USER_API_KEY_DEV
from tests import USER_API_URL_DEV
from tests.utilities.decorators import capture_printed_output
from tests.utilities.base_pipeline.base_pipeline_builder import (
    BasePipelineBuilder,
    build_pipeline,
)


class BasePipelineTools(BasePipelineBuilder):
    def __init__(self, pipeline: str):
        BasePipelineBuilder.__init__(self, pipeline)

    @capture_printed_output
    def bad_init(self):
        self.base_pipeline.init(
            api_key="c22a233c-3aee-499e-aacd-b5fae12e2f7e",
            api_url="https://12345.execute-api.us-west-2.amazonaws.com/dev",
        )

    @capture_printed_output
    def good_init(self):
        self.base_pipeline.init(
            api_key=USER_API_KEY_DEV, api_url=USER_API_URL_DEV
        )

    @capture_printed_output
    def good_search_init(self):
        self.search_pipeline.init(
            api_key=USER_API_KEY_DEV, api_url=USER_API_URL_DEV
        )

    def check_bad_init(self):
        result = self.bad_init()
        assert "FAILURE" in result["printed_output"]

    def check_good_init(self):
        result = self.good_init()
        assert "SUCCESS" in result["printed_output"]

    def check_good_search_init(self):
        result = self.good_search_init()
        assert "SUCCESS" in result["printed_output"]

    def list_all(self, verbose: bool = False):
        return self.base_pipeline.list(symbolic_directory_paths=["/*"], verbose=verbose)

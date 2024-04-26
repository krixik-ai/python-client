from tests.utilities.base_pipeline.base_pipeline_tools import BasePipelineTools


class BasePipelineSetup(BasePipelineTools):
    def __init__(self, pipeline: str):
        BasePipelineTools.__init__(self, pipeline)

    def test_1(self):
        """successfully initialize dummy account"""
        result = self.check_good_init()

    def test_2(self):
        """successfully list files in dummy account"""
        results = self.list_all()
        assert results["status_code"] == 200 or results["status_code"] == 400
        assert len(results["items"]) >= 0

    def test_3(self):
        """successfully delete all files in dummy account"""
        # list all of files in your account
        results = self.list_all()
        assert results["status_code"] == 200 or results["status_code"] == 400

        # get 'items' key from results
        warnings = results["warnings"]
        results = results["items"]

        # if there are results, collect all file_id's
        file_ids = []
        if len(results) > 0:
            for result in results:
                file_ids.append(result["file_id"])

        # collect any file_ids from warning messages
        if len(warnings) > 0:
            for warning in warnings:
                if "file_id" in list(warning.keys())[0]:
                    for entry in warning.values():
                        for file_id in entry:
                            file_ids.append(file_id)

        # delete all files in your account
        for file_id in file_ids:
            self.base_pipeline.delete(file_id=file_id)

        # list all of files in your account
        results = self.list_all()
        assert results["status_code"] == 200

        # get 'items' key from results
        results = results["items"]

        # assert that there are no files in your account
        assert len(results) == 0

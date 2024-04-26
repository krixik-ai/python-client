from krixik.utilities.validators.system import available_pipelines
from krixik.pipelines.base.krixik_base_pipeline import KrixikBasePipeline
from krixik.pipelines.base.krixik_search_pipeline import KrixikSearchPipeline


def build_pipeline(pipeline: str):
    if not isinstance(pipeline, str):
        raise TypeError("pipeline must be a string")
    if pipeline not in available_pipelines:
        raise ValueError(
            f"{pipeline} is not a valid pipeline - currently available apps are {available_pipelines}"
        )

    if pipeline == "transcribe":
        from krixik.pipelines.transcribe.modules_data_prep import modules_data_prep
    if pipeline == "translate":
        from krixik.pipelines.translate.modules_data_prep import modules_data_prep
    if pipeline == "sentiment":
        from krixik.pipelines.sentiment.modules_data_prep import modules_data_prep
    if pipeline == "caption":
        from krixik.pipelines.caption.modules_data_prep import modules_data_prep
    if pipeline == "ocr":
        from krixik.pipelines.ocr.modules_data_prep import modules_data_prep
    if pipeline == "summarization":
        from krixik.pipelines.summarization.modules_data_prep import modules_data_prep

    base_pipeline = KrixikBasePipeline(
        pipeline=pipeline, modules_data_prep=modules_data_prep
    )

    from krixik.pipelines.search.modules_data_prep import (
        modules_data_prep as search_modules_data_prep,
    )

    search_pipeline = KrixikSearchPipeline(
        pipeline="search", modules_data_prep=search_modules_data_prep
    )
    return base_pipeline, search_pipeline


def gather_test_data(pipeline: str):
    if not isinstance(pipeline, str):
        raise TypeError("pipeline must be a string")
    if pipeline not in available_pipelines:
        raise ValueError(
            f"{pipeline} is not a valid pipeline - currently available pipelines are {available_pipelines}"
        )

    if pipeline == "transcribe":
        test_data = [
            "/Users/jeremywatt/Desktop/krixik_cli/tests/test_files/transcribe/audio_files/valid_1_2.mp3",
            "/Users/jeremywatt/Desktop/krixik_cli/tests/test_files/transcribe/video_files/valid_1.mp4",
        ]
    if pipeline == "translate":
        pass
    if pipeline == "sentiment":
        pass
    return test_data


class BasePipelineBuilder:
    def __init__(self, pipeline: str):
        if not isinstance(pipeline, str):
            raise TypeError("pipeline must be a string")
        if pipeline not in available_pipelines:
            raise ValueError(
                f"{pipeline} is not a valid pipeline - currently available apps are {available_pipelines}"
            )
        self.pipeline = pipeline
        self.base_pipeline, self.search_pipeline = build_pipeline(pipeline)

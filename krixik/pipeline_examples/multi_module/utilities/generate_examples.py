import os
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline
from krixik.__base__ import library_base_dir
from krixik.pipeline_examples.multi_module.utilities import (
    multi_module_pipeline_examples,
)

save_directory = library_base_dir + "/pipeline_examples/multi_module"


def generate():
    try:
        for file in os.listdir(save_directory):
            if file.endswith(".yml"):
                os.remove(os.path.join(save_directory, file))

        pipeline = CreatePipeline()
        for element in multi_module_pipeline_examples:
            pipeline_name = element["name"]
            module_chain = element["module_chain"]
            pipeline = CreatePipeline(
                name=f"{pipeline_name}-pipeline",
                module_chain=[Module(module_name) for module_name in module_chain],
            )
            pipeline.save(f"{save_directory}/{pipeline_name}.yml")

    except Exception as e:
        raise e

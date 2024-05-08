import os
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline
from krixik.modules import available_modules
from krixik.__base__ import library_base_dir

save_directory = library_base_dir + "/pipeline_examples/single_module"


def generate():
    try:
        for file in os.listdir(save_directory):
            if file.endswith(".yml"):
                os.remove(os.path.join(save_directory, file))

        pipeline = CreatePipeline()
        for module_name in available_modules:
            module = Module(module_name)
            pipeline = CreatePipeline(name=f"{module_name}-pipeline", module_chain=[module])
            pipeline.save(config_path=f"{save_directory}/{module_name}.yml")

    except Exception as e:
        raise e

#!/bin/bash

python3.8 -m pytest tests/krixik/utilities/
python3.8 -m pytest tests/krixik/modules/ 
python3.8 -m pytest tests/krixik/pipeline_builder/
python3.8 -m pytest tests/krixik/system_builder/ --dist=loadfile
python3.8 -m pytest tests/krixik/pipeline_examples/single_module/test_generate_examples.py
python3.8 -m pytest tests/krixik/pipeline_examples/multi_module/test_generate_examples.py
python3.8 -m pytest tests/krixik/pipeline_examples/single_module/test_coverage.py
python3.8 -m pytest tests/krixik/pipeline_examples/single_module/modules/ -n auto
python3.8 -m pytest tests/krixik/pipeline_examples/multi_module/test_multi_module_pipelines.py -n auto

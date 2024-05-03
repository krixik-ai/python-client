#!/bin/bash

pytest tests/krixik/utilities/
pytest tests/krixik/modules/ 
pytest tests/krixik/pipeline_builder/
pytest tests/krixik/system_builder/ --dist=loadfile
pytest tests/krixik/pipeline_examples/single_module/test_generate_examples.py
pytest tests/krixik/pipeline_examples/single_module/test_coverage.py
pytest tests/krixik/pipeline_examples/single_module/modules/ -n auto
pytest tests/krixik/pipeline_examples/multi_module/test_generate_examples.py
pytest tests/krixik/pipeline_examples/multi_module/test_multi_module_pipelines.py -n auto

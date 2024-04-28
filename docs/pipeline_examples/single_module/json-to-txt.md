## the `json-to-txt` module

This document reviews the `json-to-txt` module - which takes as input a json of string snippets, joins them into a single string separated by double spaces, and returns a text file document.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).


```python
# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.



```python
# reset pipelines for demo
def reset_pipeline(pipeline):
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] != 500
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] != 500
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] != 500
    assert len(current_files["items"]) == 0
```

This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [using the `base` model](#using-the-base-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `json-to-txt` module. 


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="json-to-txt")

# create custom pipeline object
custom = CreatePipeline(name='json-to-txt-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

The `json-to-txt` module comes with a single model:

- `base`: (default) joins a json of text snippets into a single text separated by double spaces

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print the configuration of uor custom pipeline
json_print(custom.config)
```

    {
      "pipeline": {
        "name": "json-to-txt-pipeline-1",
        "modules": [
          {
            "name": "json-to-txt",
            "models": [
              {
                "name": "base"
              }
            ],
            "defaults": {
              "model": "base"
            },
            "input": {
              "type": "json",
              "permitted_extensions": [
                ".json"
              ]
            },
            "output": {
              "type": "text"
            }
          }
        ]
      }
    }


Here we can see the models and their associated parameters available for use.

## using the `base` model

We first define a path to a local input file.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.json"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
with open(test_file) as f:
    json_print(json.load(f))
```

    [
      {
        "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
        "line_numbers": [
          2,
          3,
          4,
          5
        ]
      }
    ]


Two sentences and their associated line numbers in the original text.

Now let's process it using our `base` model.  Because `base` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is text, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "json-to-txt-pipeline-1",
      "request_id": "cdfb3448-b7d8-454d-bd83-7becfb1b85ab",
      "file_id": "37d67bd1-08e8-484a-b7dc-8eaf7376bd93",
      "message": "SUCCESS - output fetched for file_id 37d67bd1-08e8-484a-b7dc-8eaf7376bd93.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./37d67bd1-08e8-484a-b7dc-8eaf7376bd93.txt"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    print(file.read())  
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


Here we see our two input sentences from the input have been concatenated successfully into a single text.

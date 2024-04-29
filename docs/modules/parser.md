## the parser module

This document reviews the `parser` module - which takes in input documents, cuts them up into pieces using different model logic, and returns the spliced input as json output. 

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


This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [using the `sentence` model](#using-the-sentence-model)
- [using the `fixed` model](#using-the-fixed-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `parser` module.  This parser takes in an input text file and splits into its constituent snippets.


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="parser")

# create custom pipeline object
custom = CreatePipeline(name='parser-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

The `parser` module comes with two models that determine how it cuts up an input text:

- `sentence`: (default) splits a text into its individual sentences
- `fixed`: splits a text into potentially overlapping chunks of consecutive words

The `fixed` model takes in two parameters to determine how it operates:

- `chunk_size` (recommended default 10) chunk size length in number of consecutive words
- `overlap_size`: (recommended default 2) length of overlap in words between consecutive chunks

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print the configuration of uor custom pipeline
json_print(custom.config)
```

    {
      "pipeline": {
        "name": "parser-pipeline-1",
        "modules": [
          {
            "name": "parser",
            "models": [
              {
                "name": "sentence"
              },
              {
                "name": "fixed",
                "params": {
                  "chunk_size": {
                    "type": "int"
                  },
                  "overlap_size": {
                    "type": "int"
                  }
                }
              }
            ],
            "defaults": {
              "model": "sentence"
            },
            "input": {
              "type": "text",
              "permitted_extensions": [
                ".txt",
                ".pdf",
                ".docx",
                ".pptx"
              ]
            },
            "output": {
              "type": "json"
            }
          }
        ]
      }
    }


Here we can see the models and their associated parameters available for use.

## using the `sentnece` model

We first define a path to a local input file.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
with open(test_file, "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


A paragraph of text consisting of two sentences.

Now let's process it using our `sentence` parser.  Because `sentence` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in the return response.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "e957e17f-ca3c-40bf-afd1-ebca1f27ba51",
      "file_id": "9d94d011-b445-41fa-ae9e-92322726be96",
      "message": "SUCCESS - output fetched for file_id 9d94d011-b445-41fa-ae9e-92322726be96.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
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
      ],
      "process_output_files": [
        "./9d94d011-b445-41fa-ae9e-92322726be96.json"
      ]
    }


Lets break down the output:

- `status_code`: provides the success / failure signal for the api
- `pipeline`: the name of the pipeline we ran `.process` on
- `request_id`: unique id associated with this execution of `.process`
- `file_id`: unique id for the processed file and its associated output
- `message`: message detailing success or failure of call
- `warnings`: message list indicating any warnings related to our call
- `process_output`: returned output (available when module-model output is json only)
- `process_output_files`: list of process output, local file names 

We can see from `process_output` that our two-sentence paragraph input has been separated correctly.  Each sentence also has its corresponding line number(s).

This process output is also stored in the file contained in `process_output_files`.  Lets load it in and confirm we have the same process output we see above.


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    process_output = json.load(file)
    json_print(process_output)
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


### using the `fixed` model

To use the `fixed` model we pass its name explicitly via the `modules` argument as follows.  This will implicitly pass the default parameter values for the `fixed` model.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  modules={"parser":{"model":"fixed",
                                                     "params":{
                                                         "chunk_size": 10,
                                                         "overlap_size": 2
                                                     }}})
```

Examining the output below we can see that our input document was not cut into complete sentences, but chunks of text.  Each chunk is 10 words in length, and the consecutive chunks overlap by two words.


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    process_output = json.load(file)
    json_print(process_output)
```

    [
      {
        "snippet": "It was a bright cold day in April, and the",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "and the clocks were striking thirteen. Winston Smith, his chin",
        "line_numbers": [
          1,
          2
        ]
      },
      {
        "snippet": "his chin nuzzled into his breast in an effort to",
        "line_numbers": [
          2
        ]
      },
      {
        "snippet": "effort to escape the vile wind, slipped quickly through the",
        "line_numbers": [
          2,
          3
        ]
      },
      {
        "snippet": "through the glass doors of Victory Mansions, though not quickly",
        "line_numbers": [
          3,
          4
        ]
      },
      {
        "snippet": "not quickly enough to prevent a swirl of gritty dust",
        "line_numbers": [
          4
        ]
      },
      {
        "snippet": "gritty dust from entering along with him.",
        "line_numbers": [
          4,
          5
        ]
      }
    ]

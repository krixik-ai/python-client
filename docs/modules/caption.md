## the `caption` module

This document reviews the `caption` module - which takes as input an image and returns a text description of the input image.  Output data is returned as a json.

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
- [using the vit-gpt2-image-captioning model](#using-the-vit-gpt2-image-captioning-model)
- [using the blip-image-captioning-base model](#using-the-blip-image-captioning-base-model)


## Pipeline setup

Below we setup a simple one module pipeline using the `caption` module. 


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="caption")

# create custom pipeline object
custom = CreatePipeline(name='caption-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

The `caption` module comes with a subset of popular caption models including the following:

- [vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning) (default)
- [git-base](https://huggingface.co/microsoft/git-base)
- [blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)
- [blip-image-captioning-large](https://huggingface.co/Salesforce/blip-image-captioning-large)

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print the configuration of uor custom pipeline
json_print(custom.config)
```

    {
      "pipeline": {
        "name": "caption-pipeline-1",
        "modules": [
          {
            "name": "caption",
            "models": [
              {
                "name": "vit-gpt2-image-captioning"
              },
              {
                "name": "git-base"
              },
              {
                "name": "blip-image-captioning-base"
              },
              {
                "name": "blip-image-captioning-large"
              }
            ],
            "defaults": {
              "model": "vit-gpt2-image-captioning"
            },
            "input": {
              "type": "image",
              "permitted_extensions": [
                ".jpg",
                ".jpeg",
                ".png"
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

## using the english to spanish translation model

We first define a path to a local input file.


```python
# define path to an input file
test_file = "../input_data/resturant.png"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
from IPython.display import Image
Image(filename=test_file) 
```




    
![png](caption_files/caption_14_0.png)
    



Now let's process it using the english to spanish model - `vit-gpt2-image-captioning`.  Because this is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file
test_file = "../input_data/resturant.png"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "caption-pipeline-1",
      "request_id": "21f0e335-c8cf-43fe-a6e6-7cf9b0a508d8",
      "file_id": "96c3ef30-e4a2-4daa-9765-b497fd12c6f4",
      "message": "SUCCESS - output fetched for file_id 96c3ef30-e4a2-4daa-9765-b497fd12c6f4.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "caption": "a large group of people are in a restaurant"
        }
      ],
      "process_output_files": [
        "./96c3ef30-e4a2-4daa-9765-b497fd12c6f4.json"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    print(file.read())  
```

    [{"caption": "a large group of people are in a restaurant"}]


### using the blip-image-captioning-base model

To use a non-default model like the spanish to english model `blip-image-captioning-base` we enter it explicitly as a `modules` selection when invoking `.process`.

We use it below to process the following input.


```python
# define path to an input file
test_file = "../input_data/valid_spanish.json"

# examine contents of input file
with open(test_file) as f:
    json_print(json.load(f))
```

    [
      {
        "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
      },
      {
        "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
      }
    ]



```python
# define path to an input file
test_file = "../input_data/resturant.png"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  modules={"caption":{"model":"blip-image-captioning-base"}})
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "caption-pipeline-1",
      "request_id": "bebae882-2c06-4e6c-8cf0-8e020af5451e",
      "file_id": "404f517e-f812-4535-9c8e-5f0e46093f99",
      "message": "SUCCESS - output fetched for file_id 404f517e-f812-4535-9c8e-5f0e46093f99.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "caption": "a group of people sitting around a bar"
        }
      ],
      "process_output_files": [
        "./404f517e-f812-4535-9c8e-5f0e46093f99.json"
      ]
    }


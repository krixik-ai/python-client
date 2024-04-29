# multilingual transcription pipeline

This document details a modular pipeline that takes in an audio/video file, transcribes it, and translates the transcription into a desired language.

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


This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)
- [saving the pipeline config for future use](#saving-the-pipeline-config-for-future-use)

## pipeline setup

Below we setup a multi module pipeline to serve our intended purpose, which is to build a pipeline that will transcribe any audio/video and make it semantically searchable in any language.

To do this we will use the following modules:

- [`transcribe`](modules/transcribe.md): takes in audio/video input, outputs json of content transcription
- [`translate`](modules/translate.md): takes in json of text snippets, outputs json of translated snippets



```python
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# select modules
module_1 = Module(module_type="transcribe")
module_2 = Module(module_type="translate")

# create custom pipeline object
custom = CreatePipeline(name='transcribe-translate-pipeline', 
                        module_chain=[module_1, module_2])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

With our `custom` pipeline built we now pass it, along with a test file, to our operator to process the file.

## processing a file

We first define a path to a local input file.


```python
# define path to an input file
test_file = "../input_data/Interesting Facts About Colombia.mp4"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
from IPython.display import Video
Video(test_file)
```


<video src="../input_data/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>


The input video content language content is English.  We will use the `opus-mt-en-es` model of the [`translate`](modules/translate.md) to translate the transcript of this video into Spanish.

For this run we will use the default models for the remainder of the modules.



```python
# test file
test_file = "../input_data/Interesting Facts About Colombia.mp4"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*5,
                                  modules={"translate": {"model": "opus-mt-en-es"}})
```

    INFO: Checking that file size falls within acceptable parameters...
    INFO:...success!
    converted ../input_data/Interesting Facts About Colombia.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmp5xuokbb_/krixik_converted_version_Interesting Facts About Colombia.mp3
    INFO: hydrated input modules: {'transcribe': {'model': 'whisper-tiny', 'params': {}}, 'translate': {'model': 'opus-mt-en-es', 'params': {}}, 'json-to-txt': {'model': 'base', 'params': {}}, 'parser': {'model': 'sentence', 'params': {}}, 'text-embedder': {'model': 'multi-qa-MiniLM-L6-cos-v1', 'params': {'quantize': True}}, 'vector-db': {'model': 'faiss', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_vtwcehmsxh.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 300 seconds, at Mon Apr 29 12:25:45 2024 UTC
    INFO: transcribe-translate-semantic-pipeline file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: 91147d41-0b25-651c-6f85-6727d909e68c
    INFO: File process and processing status:
    SUCCESS: module 1 (of 6) - transcribe processing complete.
    SUCCESS: module 2 (of 6) - translate processing complete.
    SUCCESS: module 3 (of 6) - json-to-txt processing complete.
    SUCCESS: module 4 (of 6) - parser processing complete.
    SUCCESS: module 5 (of 6) - text-embedder processing complete.
    SUCCESS: module 6 (of 6) - vector-db processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below.  Because the output of this particular pipeline is a json file, the process output is shown as well.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "transcribe-translate-semantic-pipeline",
      "request_id": "4ed11ce5-63de-4d99-8f3c-46d7d0db1448",
      "file_id": "4e291196-62c3-48f8-8b69-3a0aac85a99f",
      "message": "SUCCESS - output fetched for file_id 4e291196-62c3-48f8-8b69-3a0aac85a99f.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik-cli/docs/examples/4e291196-62c3-48f8-8b69-3a0aac85a99f.faiss"
      ]
    }


## saving the pipeline config for future use

You can save the configuration of this pipeline using the `custom` object, and use it later direclty without building it again in python.


```python
# save your config for later use (that way you don't need to re-build in python)
custom.save(config_path='transcribe-translate-semantic-pipeline.yml')
```

See more about [saving and loading pipeline configuration files](LINNK GOES HERE).

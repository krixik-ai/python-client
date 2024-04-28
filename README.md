# Krixik python cli

Easily consume modular AI pipelines from a secure API, in python.

## Contents
 
- [Introduction to krixik](#introduction-to-krixik)
- [Two popular modular AI pipelines](#two-popular-ai-pipelines)
    - [Vector search pipeline](#vector-db-pipeline)
    - [Transcription pipeline](#transcription-pipeline)
- [Introduction to the krixik cli](#introduction-to-the-krixik-cli)
- [Register an account](#register-an-account)
- [Installation](#installation)
- [Initialize your `krixik` cli](#initialize-your-krixik-cli)
- [Quick start example](#quick-start-example)
    - [Setting up a search pipeline](#setting-up-a-search-pipeline)
    - [Process a file but do not wait for the results](#process-a-file-but-do-not-wait-for-the-results)
    - [Using modules manually](#using-modules-manually)
    - [Setting the expire time](#setting-the-expire-time)
- [Pipeline index](#pipeline-index)
    - [Examples](#examples)



## Introduction to krixik

Sometimes you want to consume an AI model convinently as an API.  

But typically you need more than just a model to make AI useful: often a single AI model is only one (important) step of a larger pipeline.

An AI pipeline consists of self-contained, modular components - from the AI model(s) themselves, to pre/post processing steps, data augmentation, encoding/decoding,  data storage and retrieval, etc.,  

Building, testing, deploying, and maintaining these components -  as well as wiring them together to function as a single secure API - can be a complex, expensive, and time-consuming process.
 
Thats why we built krixik.  

With krixik we make it easy build, test, deploy, and maintain modular AI pipelines that you can serve and consume convinently as a secure API endpoint.


## Two popular modular AI pipelines

Sometimes an AI pipeline can consist of a single AI model.  More often than not, they consist of several self contained processing steps or modules

**Vector search** and **transcription** and are two such popular AI pipelines, each consisting of a number of modular components.

### Vector search pipeline

Suppose you have a document that would like to make searchable.

A standard vector search pipeline consists of at least three modular components that need to performed on an input document in sequence to make it searchable.  These are

 - **Parser**: a parser transforms input text into "chunks" of text that are suitable for searching.  For example, a parser might split a document into sentences, or slice it into overlpipelineing windows of consecutive words / tokens.

 - **Embedder**: an embedder transforms the chunks of text into a suitable numerical representation - a vector - that make the chunk mathematically comparable to other chunks.  For example, an embedder might transform a chunk of text into a 512-dimensional vector.  This makes the chunk comparable to other chunks using standard vector similarity measures (e.g., cosine similarity).

 - **Vector database**: a vector database takes the vectors and stores and indexes them in a way that makes them easily searchable.  For example, a vector database might store the vectors in a way that makes them easily searchable using a nearest neighbor search algorithm.

 Each of these components are modular - there are many different parsers, embedders, and indexers to choose from.  


### Transcription pipeline

A standard transcription pipeline consists of at least two components to extract transcription from a raw audio file.  These are:

- **Voice Activity Detection**: a voice activity detector (VAD) is an AI model trained to identify the parts of an audio file that contain speech.  These segments can then be passed on to a transcription model to perform transcription.  VAD is an important pre-processing step, as transcription models can hallucinate transcriptions in areas of an input audio file that contain no speech.

- **Transcription model**: a transcription model takes in an audio file - or a segment of an audio file - and outputs a transcript.  

These components are modular - there are many different VAD and transcription models to choose from.


## Introduction to the krixik cli

The krixik python client allows you to consume modular AI pipelines as a secuire API.   Processing is managed on a serverless infrastructure, meaning no local setup is required to use any api beyond the installation of the krixik cli.


## Register an account

krixik is currently in closed beta.  Access to the krixik cli is by request only.

To request access please complete our short survey form (LINK TO GOOGLE INTAKE FORM GOES HERE).  


## Introduction

The krixik client consists of a set of a universal apis for a diverse range of AI models and general data pipelines. 


## Installation

To install the krixik python cli, run the following command:

```pip
pip install krixik-cli
```

Note: python version 3.8 or higher is required.


## Initialize your `krixik` cli

Initialize your `krixik` cli using your unique secrets `api_key` and `api_url` as shown below.


```python
from krixik import krixik
krixik.init(api_key=MY_API_KEY, 
            api_url=MY_API_URL)
```

where  `MY_API_KEY` and `MY_API_URL` are your account secrets.


## Quick start example

### setting up a search pipeline

After initializing your `krixik` cli, you can get started using any pipeline.  For example, to use the `search` pipeline, first create an pipeline object using the `select_pipeline` method as shown below.

```python
from krixik import krixik
search = krixik.select_pipeline(pipeline='search')
```

Now you can then use the search pipeline to make any `.txt`, `.pdf`, `.docx`, or `.pptx` searchable via both vector and keyword search.  You can upload a file as shown below for processing.

```python
# process a file and wait for the results
output_data = search.process(/local/path/to/text/file)
```

By default you will wait for the process to complete and then download the confirmation that your input text has been successfully processed for vector/keyword search.

### process a file but do not wait for the results

By default execution of the `process` method will block until the process is complete.  You can set `wait_for_process` to `False` to return your current thread once your audio has completed uploading.  Set `verbose` to `False` to suppress all information printed to the console as well.

```python
# process a file but do not wait for the results
output_data = search.process(local_file_path=/local/path/to/text/file, 
                             wait_for_process=False,
                             verbose=False)
```

Check the process status using the `process_status` method.  Feed in the `process_id` from the `output_data` received above.  This will return the status of the associated process.


```python
# check the status of the process
search.process_status(process_id=output_data['process_id'])
```

Once the process is complete, you can query your file using vector and keyword search.  To perform vector search use the `.semantic_search` method as shown below.
 
```python
# vector search
search.semantic_search(file_ids=[output_data['file_id']], 
                     query='my search query goes here')
```

To perform keyword search use the `.keyword_search` method as shown below.

```python
# keyword search
search.keyword_search(file_ids=[output_data['file_id']], 
                      query='my search query goes here')
```

You can perform either search over multiple files by passing a list of file_ids to the `file_ids` parameter.  

If you would like additional manual metadata associated with your file, you can assign a custom `file_name`, `symbolic_directory_path`, and `file_tags` to the file as described in the [krixik file system](#krixik-file-system) documentation.

Doing so allows you to perform both keyword and vector search over the metadata you have assigned to your file.  For example, provided a file tag `{"deadline": "urgent"}`when processing your file, you can use the `.keyword_search` method as shown below.

```python
# keyword search
search.keyword_search(file_tags={"deadline": "urgent"}, 
                      query='my search query goes here')
```

to perform keyword search on this file as well as any other file with the tag `{"deadline": "urgent"}` you have previously processed.


### Using modules manually

To see the current list of modules available for search, use the `.available_modules` method as shown below.

```python
# see the available modules for search
search.available_modules()
```

To use a specific module for search, set the `modules` parameter to a dictionary particular  modules you would like to use.  The first module listed in each sub-dictionary is the default module used for search.

For search your `modules` dictionary should have the following format:

```python
modules = {
    'parser': 'parser_module_option',
    'embedder': 'embedder_module_option',
    'vector_db': 'vector_db_module_option',
}
```

For example, to use the `search` module `search_module_option` you would set `modules` as shown below.

```python
# process a file with manually selected modules
output_data = search.process(local_file_path=/local/path/to/text/file, 
                             modules={'parser': 'parser_module_option',
                                      'embedder': 'embedder_module_option',
                                      'vector_db': 'vector_db_module_option'})
```

### Setting the expire time

By default we keep output associated with a successfully run `search` process for 30 minutes.  

You can change this by setting `expire_time` to the number of seconds you would like to keep the output alive on our servers for.  The minimum time you can set is 60 seconds, and maximum is 7 days (604800 seconds).  

Below we illustrate setting the `expire_time` to 7 days hour (604800 seconds).

```python
# process a file but do not wait for the results - set expire time to 7 days
output_data = search.process(local_file_path=/local/path/to/text/file,
                             wait_for_process=False,
                             verbose=False,
                             expire_time=604800)
```

If you would like to keep the output of this process organized you can use the `.list`, `.update`, and `.delete` methods as described in the [krixik file system](#krixik-file-system) documentation.


## pipeline index

The following modular AI pipelines are available for immediate use with the krixik python cli:

- `search`: make your text both vector and keyword searchable using top embedding models from hugging face and the faiss vector database

- `transcribe`: transcribe audio to text using a variety of whisper models

- `sentiment`: analyze the sentiment of text using popular sentiment analysis models from huggingface

- `translate`: translate text between languages (e.g., English to French) using popular translation models from huggingface

- `caption`: generate captions for images using high quality image caption models from huggingface

- `ocr`: extract text from images using popular OCR models pytessearct and easyocr

- `summarize`: summarize text using popular summarization models from huggingface


### Examples

Examples of each pipeline are provided in the [docs](#docs) directory of this repository.

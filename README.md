# Welcome to Krixik!

Sequentially assembling multiple AI models into a single pipeline can be a painful and expensive. Consuming even a single model can often be draining.

That's why we're here. **Welcome to Krixik**, where you can easily assemble and serverlessly consume modular AI pipelines through secure Python APIs.

## Table of Contents

- [What can you do with Krixik?](#what-can-you-do-with-krixik)
- [Core concepts](#core-concepts)
- [Quickstart guide](#quickstart-guide)
- [Further detail](#further-detail)

## What can you do with Krixik?

With Krixik, you can...

- ...run semantic search on 540 focus group transcripts and perform sentiment analysis on each result.
  - Pipeline: [Parse → Embed → Vector Search → Sentiment Analysis]
- ...transcribe a year's worth of Peruvian political speeches, translate them to English, and summarize each one.
  - Pipeline: [Transcribe → Translate → Summarize]
- ...easily and serverlessly consume your open-source OCR model of choice.
  - Pipeline: [OCR]

## Core concepts

### Components of a krixik pipeline

Krixik **pipelines** are comprised of one or more sequentially connected **modules**. These modules are containers for a range of (possibly) **parameterized** AI **models** or support functions.

Let's examine each of the above-highlighted terms.

A **pipeline** is a self-contained sequence of one or more modules that is consumed via a serverless API.  

A **module** is a processing step with a unique input/output data footprint. Each model contains a parameterizable AI model or support function.

A **model** is a bespoke processing function contained within a module. Many of these are AI models, but some are simple "support functions" for inter-pipeline data preparation or transformation.

**Parameters** can be set for each module when a pipeline is run and allow for further customization. Each has a default value, so setting them is optional. For instance, one parameterizable item is which specific AI model you want active within a given module.

--

New modules and models will constantly be added to the Krixik library. To see all available modules at any given time, run the following:

```python
krixik.available_modules
```

## Quickstart guide

### Account registration

Krixik is currently in beta, so access to the Krixik CLI is by request only.

If you'd like to participate as a beta tester, please complete [this brief Google form](https://docs.google.com/forms/d/e/1FAIpQLSfieELvcpumTwzKZnDj9AVUpX8FgJzHEca80Css4WNSdlbKQA/viewform?usp=sf_link) and we'll get back to you soon.

### Install Krixik

Run the following command to install the Krixik Python CLI:

```pip
pip install krixik
```

Note: Python version 3.8 or higher is required.


### Initialize your session

To initialize your Krixik CLI session you will need your unique `api_key` and `api_url` secrets.  Beta testers will receive their secrets from Krixik admin.

Once you have your secrets, initialize your session as follows:


```python
from krixik import krixik
krixik.init(api_key=MY_API_KEY, 
            api_url=MY_API_URL)
```

...where  `MY_API_KEY` and `MY_API_URL` are your account secrets.

If you've misplaced your secrets, please reach out to us directly.


### Building your first pipeline

Let's build a simple transcription pipeline consisting of a single `transcribe` module.

Import the required Krixik module and pipeline tooling required to instantiate modules and create custom pipelines: the `Module` and `CreatePipeline` class objects. Then create your module and your pipeline.

```python
# import custom pipeline builder tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(name="transcribe")

# create custom pipeline object with above module
custom_pipeline_1 = CreatePipeline(name='my-transcribe-pipeline-1', 
                                   module_chain=[module_1])
```

With your custom pipeline defined you can load it for use with the `load_pipeline` method.

```python
my_pipeline_1 = krixik.load_pipeline(pipeline=custom_pipeline_1)
```

The pipeline is ready! Now you can process audio and video files through it to generate transcripts of them.

```python
my_pipeline_1.process(local_file_path='./path/to/my/mp3/or/mp4')
```

The outputs of this pipeline will be a timestamped transcript of your input audio/video file, a `file_id` for the processed file, and a `process_id` for the process itself.


### Extending your pipeline

Suppose you wanted to make the output of the `transcribe` module immediately vector searchable.

You would need to do the following after transcription:

1.  *Transform* the transcript into a text file
2.  *Parse* the text using a sliding window, chunking it into (possibly overlapping) snippets
3.  *Embed* each snippet using an appropriate text embedder
4.  *Store* the resulting vectors in a vector database
5.  *Index* said database

Locally creating and testing this sequence of steps would be time consuming—orchestrating them in a secure production service even more so. And that's without trying to make it all serverless.

With **Krixik**, however, you can rapidly add this functionality to your original pipeline by just adding a few modules. Syntax remains as above:

```python
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate modules
module_a = Module(name="transcribe")
module_b = Module(name="json-to-txt")
module_c = Module(name="parser")
module_d = Module(name="text-embedder")
module_e = Module(name="vector-search")

# create custom pipeline object with the above modules in sequence
custom_pipeline_2 = CreatePipeline(name='my-transcribe-pipeline-2', 
                        module_chain=[module_a, module_b, module_c, module_d, module_e])

# pass the custom object to the krixik operator
my_pipeline_2 = krixik.load_pipeline(pipeline=custom_pipeline_2)
```

Let's process a file through your new pipeline.

```python
my_pipeline_2.process(local_file_path='./path/to/my/mp3/or/mp4')
```

Now that there is at least one file in the pipeline, you can use the file's `file_id`—which was returned at the end of the above process—to perform semantic search on the associated transcript with `.vector_search`:

```python
my_pipeline_2.vector_search(query="The text you wish to semantically search for goes here",
                            file_ids=['file_id_from_above'])
```

That's it! You have now transcribed a file, processed the transcript, performed vector search on it, and can reuse the pipeline for as many files and queries as you like... all of it in a couple of minutes and with a few lines of code.

## Further detail

The above is just a peek at the power of Krixik. In addition to all possible parameterization (which we didn't even touch on), the Krixik toolbox is an ever-growing collection of modules and models for you to build with.

If you'd like to learn more, please visit: [[FOUR BULLETS BELOW ARE LINKS]]

- An in-depth look at pipeline assembly and parameterization
- Using the Krixik file system
- The Krixik module library
- Krixik pipeline examples

## Krixik launch date and newsletter

Excited about Krixik graduating from beta? So are we! We're confident that this product is going to kick a monumental amount of ass, and we'd love to have you on board when it does.

If you wish to be in the loop about launch and other matters (we promise not to spam), please subscribe to occasional correspondence from us [[HERE]].

Thanks for reading, and welcome to Krixik!

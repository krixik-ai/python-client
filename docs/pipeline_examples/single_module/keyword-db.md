## the `keyword-db` module

This document reviews the `keyword-db` module - which takes as input a document, parses the documents for non-trivial keywords and their lemmatized stems, and returns a database with this content.

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
- [using the `keyword_search` method](#using-the-keyword-search-method)
- [querying output databases locally](#querying-output-databases-locally)

## Pipeline setup

Below we setup a simple one module pipeline using the `keyword-search` module. 


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="keyword-db")

# create custom pipeline object
custom = CreatePipeline(name='keyword-db-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

The `keyword-search` module comes with a single model:

- `base`: (default) parses input document for non-trivial keywords

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print the configuration of uor custom pipeline
json_print(custom.config)
```

    {
      "pipeline": {
        "name": "keyword-db-pipeline-1",
        "modules": [
          {
            "name": "keyword-db",
            "models": [
              {
                "name": "sqlite"
              }
            ],
            "defaults": {
              "model": "sqlite"
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
              "type": "db"
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


Two sentences and their associated line numbers in the original text.

Now let's process it using our `base` model.  Because `base` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*3,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is a sqlite database, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "keyword-search-pipeline-1",
      "request_id": "9871ccde-80c7-4b17-9d05-fc07903ed1de",
      "file_id": "b57921e2-306c-4d43-9150-7649b4b5aaf6",
      "message": "SUCCESS - output fetched for file_id b57921e2-306c-4d43-9150-7649b4b5aaf6.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./b57921e2-306c-4d43-9150-7649b4b5aaf6.db"
      ]
    }


### using the `keyword_search` method

Any pipeline containing a `keyword-search` module automatically inherits access to the [`keyword_search` method](keyword_search_method.md).  This provides convenient sophisticated query access to the newly created keyword database in krixik.

The `keyword_search` method takes in an input `query` containing desired keywords separated by spaces, and searches through your database(s) for these keywords as well as their lemmatized stems.

An example use if given below.


```python
# perform keyword_search over the input file
keyword_output = pipeline.keyword_search(query="it was cold night",
                                         file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(keyword_output)
```

    {
      "status_code": 200,
      "request_id": "27cd17f5-ac73-4771-aecb-8852aadb1bf0",
      "message": "Successfully queried 1 user file.",
      "warnings": [
        {
          "WARNING: the following words in the query are in the stop_words list and thus no results will be returned for them": [
            "it",
            "was"
          ]
        }
      ],
      "items": [
        {
          "file_id": "b57921e2-306c-4d43-9150-7649b4b5aaf6",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_tcrgnmbhcz.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 5,
            "created_at": "2024-04-28 21:05:32",
            "last_updated": "2024-04-28 21:05:32"
          },
          "search_results": [
            {
              "keyword": "cold",
              "line_number": 1,
              "keyword_number": 5
            }
          ]
        }
      ]
    }


### querying output databases locally

We can now perform queries on the pulled keyword database whose location is given in `process_output_files`.

Below is a simple function for performing single keyword queries on this database locally.


```python
import sqlite3

def query_db(query_keyword: str,
             keyword_db_local_file_name: str) -> list:
    # load keyword_db
    keyword_db = sqlite3.connect(keyword_db_local_file_name)
    keyword_cursor = keyword_db.cursor()
    
    # create query pattern
    query_pattern = f"""
    SELECT
        original_keyword,
        line_number,
        keyword_number
    FROM
        keyword_search
    where original_keyword="{query_keyword}"
    GROUP BY
        original_keyword,
        line_number,
        keyword_number
    ORDER BY
        line_number,
        keyword_number
    """
    
    # excute query
    keyword_cursor.execute(query_pattern)

    # Fetch and process the results
    rows = keyword_cursor.fetchall()
    return rows
```

Below we query our small database using a single keyword query.


```python
# query database
query = "cold"
query_db(query,
         process_output['process_output_files'][0])
```




    [('cold', 1, 5)]



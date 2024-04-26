# Demo examples

Three notebooks in the main of this directory illustrate three compelling use cases of the current system.  

They center on our strongest modules in terms of quality: `sentiment`, `search`, `translate`, and `transcribe`.

I've started each one with a single module - building up to something more complex as we go along.  Done this for the sake of an audience not us - will of course be more compelling to build up to an approximate magic moment starting from humble beginnings.

My personal ordering of the three:

1.  `transcribe-examples.ipynb`: 

"transcribe any audio/video and make it searchable in any language"

this starts with a very familiar (in the yc space) item, whisper, and goes a long way down the yellow brick road

2.  `sentiment-examples.ipynb` - 

"analyze the sentiment of any product reviews, tweets, etc., in any language"

pretty business-y, a shorter demo.


3.  `text-search-examples.ipynb` -

"make your documents searchable in any language"

good but missing the sentence parser (which i put a dummy version of in code) so demo not as compelling



The `wip` directory contains more - but of inferior interest imo.


They aren't the only examples we have worked up.

Examine the directories in your krixik cli:

- `krixik/pipeline_examples/single_module`
- `krixik/pipeline_examples/multi_module`

The examples in these directories are tested as a part of v1.1.13 test suite.

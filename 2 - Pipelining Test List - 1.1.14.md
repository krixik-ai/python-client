# PIPELINING TEST LIST - 1.1.14

### TABLE OF CONTENTS

P1 - Module tests
P2 - Pipeline tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## P1 - Module tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

P1.1 - AVAILABLE_MODULES TESTS
1 - Confirm `.available_modules` is working well
2 - Attempt without .init
3 - Attempt without internet connection

P1.2 - MODULE INSTANTIATION LABEL VALIDITY AND TYPE CHECK TESTS
 - Module label is too long
 - Module label is one character
 - Module label has all spaces
 - Module label has odd characters
 - Module label is integer
 - Module label is boolean
 - Module label is list
 - Module label is string

P1.3 - MODULE DUPLICATION TESTS
 - Module name duplication in same code execution (cell)
 - Module name duplication in different code execution (cell)
 - Module type duplication in same code execution (cell)
 - Module type duplicaiton in different code excution (cell)

P1.4 - MODULE FUNCTION ARGUMENT TESTS
 - Null all arguments
 - Inexistent argument
 - Inexistent argument and `module_type`

P1.5 - RENAMED MODULE_TYPE ARGUMENT TESTS
 - `name` argument by itself
 - `name` argument with `module_type`

P1.6 - MODULE_TYPE TYPE CHECK AND VALIDITY TESTS
 - As integer
 - As list
 - As boolean
 - As dictionary
 - As random string
 - As empty string

P1.7 - MODULE INSTANTIATION WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P1.8 - .CONFIG PROPERTY ON INEXISTENT MODULE TESTS
 - Attempt on an inexistent module

P1.9 - .CONFIG PROPERTY ON REPLACED MODULE TESTS
 - Attempt on a module that's been duplicated

P1.10 - .CONFIG PROPERTY ON FAILED MODULE TESTS
 - Attempt on a module whose creation failed

P1.11 - .CONFIG PROPERTY ON CURRENT MODULES TESTS
 - On Caption
 - On JSON-to-TXT
 - On Keyword search
 - On OCR
 - On Parser
 - On Sentiment
 - On Summarize
 - On Text embedder
 - On Transcribe
 - On Translate
 - On Vector search

 P1.12 - .CONFIG PROPERTY ON MODULE WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P1.13 - .CLICK_DATA PROPERTY ON INEXISTENT MODULE TESTS
 - Attempt on an inexistent module

P1.14 - .CLICK_DATA PROPERTY ON REPLACED MODULE TESTS
 - Attempt on a module that's been duplicated

P1.15 - .CLICK_DATA PROPERTY ON FAILED MODULE TESTS
 - Attempt on a module whose creation failed

P1.16 - .CLICK_DATA PROPERTY ON CURRENT MODULES TESTS
 - On Caption
 - On JSON-to-TXT
 - On Keyword search
 - On OCR
 - On Parser
 - On Sentiment
 - On Summarize
 - On Text embedder
 - On Transcribe
 - On Translate
 - On Vector search

P1.17 - .CLICK_DATA PROPERTY WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P1.18 - .OUTPUT_EXAMPLE PROPERTY ON INEXISTENT MODULE TESTS
 - Attempt on an inexistent module

P1.19 - .OUTPUT_EXAMPLE PROPERTY ON REPLACED MODULE TESTS
 - Attempt on a module that's been duplicated

P1.20 - .OUTPUT_EXAMPLE PROPERTY ON FAILED MODULE TESTS
 - Attempt on a module whose creation failed

P1.21 - .OUTPUT_EXAMPLE PROPERTY ON CURRENT MODULES TESTS
 - On Caption
 - On JSON-to-TXT
 - On Keyword search
 - On OCR
 - On Parser
 - On Sentiment
 - On Summarize
 - On Text embedder
 - On Transcribe
 - On Translate
 - On Vector search

P1.22 - .OUTPUT_EXAMPLE PROPERTY WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection


[[FOR LATER, FEATURE REQUEST: ALLOW USERS TO LIST ALL INSTANTIATED MODULES AND PIPELINES]]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## P2 - Pipeline tests [OccasionallyTestSuccessfullyCreatedPipelineWithFile]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

P2.1 - PIPELINE INSTANTIATION LABEL VALIDITY AND TYPE CHECK TESTS
 - Pipeline label is too long
 - Pipeline label is one character
 - Pipeline label has odd characters
 - Pipeline label has all spaces
 - Pipeline label is integer
 - Pipeline label is boolean
 - Pipeline label is list
 - Pipeline label is string

P2.2 - CREATEPIPELINE NULL ARGUMENTS TESTS
 0 - Call help to see all arguments
 - All arguments null
 - [Null each argument and, if few enough, by MECE sets] [[If there are more than module_chain, name, config_path, and the load one, must make moar tests]]

P2.3 - CREATEPIPELINE NAME ARGUMENT TYPE CHECK AND VALIDITY TESTS
 - As integer
 - As list
 - As boolean
 - As dictionary
 - As string, one character
 - As string, empty
 - As string, just spaces
 - As string, much too long
 - As string, includes Chinese and accented characters

P2.4 - PIPELINE NAME DUPLICATION TESTS
 - In same code cell execution
 - In separate code cell execution

P2.5 - MODULE_CHAIN TYPE CHECK TESTS
 - As integer
 - As string
 - As boolean
 - As dictionary

P2.6 - MODULE_CHAIN COMPONENT TESTS [Test with known good matches]
 - One, as a string
 - One, as a list
 - One, as an integer
 - One, as a boolean
 - One, as a dictionary
 - One, as an inexistent module
 - One, as a replaced module
 - One, as a creation-failed module
 - One, as a too-long name module
 - One, as a one-character name module
 - Two, including a string
 - Two, including a list
 - Two, including an integer
 - Two, including a boolean
 - Two, including a dictionary
 - Two, including an inexistent module
 - Two, including a replaced module
 - Two, including a creation-failed module
 - Two, including a too-long name module
 - Two, including a one-character name module
 [3x] - Three, combination of the above

P2.7 - MODULE_CHAIN VALIDITY TESTS [Test with known good matches]
 - List is empty
 - List is much too long
 - List repeats same module many times (within cap)
 - List repeats same module type but different instances
 - List includes a module with no name, just two consecutive commas

P2.8 - CREATEPIPELINE CONFIG_PATH TYPE CHECK TESTS
- As integer
- As dictionary
- As boolean
- As dictionary

P2.9 - CREATEPIPELINE CONFIG_PATH ARGUMENT VALIDITY TESTS [RANDOMIZE BETWEEN KEYWORD AND POSITIONAL]
- Random string
- Empty string
- Valid, but does not start with period
- Valid, but does not start with period or slash
- Valid, but starts with period and no slash
- Only directory, does not end in slash
- Only directory, ends in slash
- Only full file name
- File, no extension
- File, period but no extension
- Complete file, but file isn't there
- Complete file, file exists but isn't yaml
- File is fine, but name is a single character
- File is fine, but name includes Chinese and accented Latin Characters
- File is fine, but name is impossibly long

P2.10 - CREATEPIPELINE CONFIG_PATH YAML VALIDITY TESTS [RANDOMIZE BETWEEN .YML AND .YAML]
- Yaml is re-extensioned from other sort of file
- Yaml is blank
- Yaml has random content in it
- Yaml is incredibly long and enormous and has random stuff in it
- Yaml has properly formatted single pipeline in it (Krixik generated)
- Yaml has properly formatted single pipeline in it (manually generated)
- Yaml has properly formatted multiple pipelines in it
- Yaml has multiple properly formatted pipelines in it, but also some random crap
- Yaml has properly formatted pipelines in it, but a trillion of them
[2x, or as many as need be] - Yaml has pipeline in it, but it's not quite properly formatted
[2x, or as many as need be] - Yaml has pipeline in it, but it's not all there. Some parts are missing
[2x, or as many as need be] - Yaml has had a single random character thrown in there

P2.11 - PIPELINE INSTANTIATION WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.12 - .ADD METHOD ON INEXISTENT PIPELINE TESTS
  - Try on an inexistent pipeline

P2.13 - .ADD METHOD ON REPLACED PIPELINE TESTS
  - Try on an replaced pipeline

P2.14 - .ADD METHOD ON FAILED PIPELINE TESTS
 - Attempt on a pipeline whose creation failed

P2.15 - .ADD METHOD ON DIFFERENT PIPELINES TESTS
 - On preexistent single-module pipeline
 - On preexistent multi-module pipeline
 - On same-cell single-module pipeline
 - On same-cell multi-module pipeline
 - On pipeline that is just at its module cap

[[FEATURE REQUEST FOR LATER: SHOULD ONE BE ABLE TO "SUBTRACT" A MODULE, JUST AS ONE ADDS ONE? POP OFF THE TOP ONE?]]

P2.16 - .ADD METHOD NULL ARGUMENT TESTS
0 - Call help to see all arguments
 - Null all arguments
 - [Null each argument and, if few enough, by MECE sets]

P2.17 - .ADD METHOD ARGUMENT TYPE CHECK TESTS
1 - String
2 - List
3 - Integer
4 - Boolean
5 - Dictionary
6 - Undeclared variable

P2.18 - .ADD METHOD ARGUMENT VALIDITY TESTS
1 - Replaced module
2 - Module already in pipeline but not adjacent
3 - Module in pipeline and adjacent
4 - Creation-failed module
5 - Same type of module already in pipeline but not same instance

P2.19 - .ADD METHOD WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.20 - .SAVE METHOD NULL ARGUMENT TESTS
0 - Call help to see all arguments
 - Null all arguments
 - [Null each argument and, if few enough, by MECE sets]

P2.21 - .SAVE CONFIG_PATH TYPE CHECK TESTS [MAY HAVE TO DO OTHER SUBSETS OF THERE ARE OTHER ARGUMENTS, BUT I THINK NOT]
- As integer
- As dictionary
- As boolean
- As dictionary

P2.22 - .SAVE CONFIG_PATH VALIDITY TESTS [RANDOMIZE BETWEEN KEYWORD AND POSITIONAL]
- Random string
- Empty string
- Valid, but does not start with period
- Valid, but does not start with period or slash
- Valid, but starts with period and no slash
- Only directory, does not end in slash
- Only directory, ends in slash
- Only full file name
- File, no extension
- File, period but no extension
- Complete file, but file isn't there
- Complete file, file exists but isn't yaml
- File is fine, but name is a single character
- File is fine, but name includes Chinese and accented Latin Characters
- File is fine, but name is impossibly long

P2.23 - .SAVE CONFIG_PATH YAML VALIDITY TESTS [RANDOMIZE BETWEEN .YML AND .YAML]
- Yaml is re-extensioned from other sort of file
- Yaml is blank
- Yaml has random content in it
- Yaml is incredibly long and enormous and has random stuff in it
- Yaml already has properly formatted single pipeline in it (Krixik generated)
- Yaml already has properly formatted single pipeline in it (manually generated)
- Yaml already has properly formatted multiple pipelines in it
- Yaml has multiple properly formatted pipelines in it, but also some random crap
- Yaml has properly formatted pipelines in it, but a trillion of them

P2.24 - .SAVE METHOD WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.25 - .LOAD_PIPELINE NULL AND DOUBLED ARGUMENTS TESTS
 0 - Call help to see all arguments
 - All arguments null
 - [Null each argument and, if few enough, by MECE sets]
 - Include both 'pipeline' and 'config_path' [tbd if there are other arguments]

P2.26 - .LOAD_PIPELINE PIPELINE ARGUMENT TYPE CHECK TESTS
- As integer
- As boolean
- As string
- As dictionary
- As list
- As undefined variable

P2.27 - .LOAD_PIPELINE PIPELINE ARGUMENT VALIDITY TESTS
- Replaced pipeline
- Creation-failed pipeline
- Successfully made but tricky pipeline, like multiple same module

P2.28 - .LOAD_PIPELINE CONFIG_PATH ARGUMENT TYPE CHECK TESTS
- As integer
- As dictionary
- As boolean
- As dictionary

P2.29 - .LOAD_PIPELINE CONFIG_PATH ARGUMENT VALIDITY TESTS [RANDOMIZE BETWEEN KEYWORD AND POSITIONAL]
- Random string
- Empty string
- Valid, but does not start with period
- Valid, but does not start with period or slash
- Valid, but starts with period and no slash
- Only directory, does not end in slash
- Only directory, ends in slash
- Only full file name
- File, no extension
- File, period but no extension
- Complete file, but file isn't there
- Complete file, file exists but isn't yaml
- File is fine, but name is a single character
- File is fine, but name includes Chinese and accented Latin Characters
- File is fine, but name is impossibly long

P2.30 - .LOAD_PIPELINE CONFIG_PATH YAML VALIDITY TESTS [RANDOMIZE BETWEEN .YML AND .YAML]
- Yaml is re-extensioned from other sort of file
- Yaml is blank
- Yaml has random content in it
- Yaml is incredibly long and enormous and has random stuff in it
- Yaml has properly formatted single pipeline in it (Krixik generated)
- Yaml has properly formatted single pipeline in it (manually generated)
- Yaml has properly formatted multiple pipelines in it
- Yaml has multiple properly formatted pipelines in it, but also some random crap
- Yaml has properly formatted pipelines in it, but a trillion of them
[2x, or as many as need be] - Yaml has pipeline in it, but it's not quite properly formatted
[2x, or as many as need be] - Yaml has pipeline in it, but it's not all there. Some parts are missing
[2x, or as many as need be] - Yaml has had a single random character thrown in there

P2.31 - .LOAD_PIPELINE METHOD WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.32 - ALL TWO-MODULE PIPELINE CREATION COMBINATION TESTS - [RANDOMIZE BETWEEN MODULE_CHAIN AND .ADD, OCCASIONALLY LOAD SOME OF THEM]
- [ATTEMPT EVERY PERMUTATION OF EVERY SINGLE TWO-MODULE COMBINATION, INCLUDING DOUBLE-UPS; CONFIRM THAT WHAT SHOULD CLICK CLICKS AND WHAT SHOULDN'T DOESN'T]

P2.33 - EXISTING PIPELINE AUGMENTATION INTO 3+ MODULES WITH .ADD
[15x] - Random two module pipeline, random module .added, duplication allowed
[10x] - Random 3+ module pipeline, random module .added, duplication allowed

P2.34 - NEW 3+ MODULE CREATION WITH MODULE_CHAIN
[30x] - RNG from 3 to cap, all modules randomly selected, duplication allowed

P2.35 - .CONFIG PROPERTY ON INEXISTENT PIPELINE TESTS
 - Attempt on an inexistent module

P2.36 - .CONFIG PROPERTY ON REPLACED PIPELINE TESTS
 - Attempt on a module that's been duplicated

P2.37 - .CONFIG PROPERTY ON FAILED PIPELINE TESTS
 - Attempt on a module whose creation failed

P2.38 - .CONFIG PROPERTY ON PIPELINES LOADED VS NOT LOADED INTO OPERATOR
 - .config on a pipeline not yet loaded
 - .config on same pipeline now loaded

P2.39 - .CONFIG PROPERTY ON SEARCH PIPELINES WITH VS WITHOUT FILES IN THEM
 - .config on semantic search pipeline without file in it
 - .config on same semantic search pipeline with a file in it
 - .config on same semantic search pipeline with multiple files in it
 - .config on keyword search pipeline without file in it
 - .config on same keyword search pipeline with a file in it
 - .config on same keyword search pipeline with multiple files in it

P2.40 - .CONFIG PROPERTY ON CURRENT PIPELINE TESTS
[10x] - Run .config on existing pipelines; make sure all modules are covered at least once

P2.41 - .CONFIG PROPERTY ON PIPELINE WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.42 - .TEST_INPUT ON INVALID PIPELINE TESTS
- .test_input on inexistent pipeline
- .test_input on replaced pipeline
- .test_input on failed pipeline

P2.43 - TEST_._INPUT ON DIFFERENT TYPES OF PIPELINES TESTS [Randomize how many modules in pipeline, from 1 to cap]
 - Start with Caption (off-type input)
 - Start with Caption (on-type input)
 - Start with JSON-to-TXT (off-type input)
 - Start with JSON-to-TXT (on-type input)
 - Start with JSON-to-TXT (misextensioned)
 - Start with Keyword search (off-type input)
 - Start with Keyword search (on-type input)
 - Start with OCR (off-type input)
 - Start with OCR (on-type input)
 - Start with Parser (off-type input)
 - Start with Parser (on-type input)
 - Start with Sentiment (off-type input)
 - Start with Sentiment (on-type input)
 - Start with Sentiment (misextensioned)
 - Start with Summarize (off-type input)
 - Start with Summarize (on-type input)
 - Start with Text embedder (off-type input)
 - Start with Text embedder (on-type input)
 - Start with Transcribe (off-type input)
 - Start with Transcribe (on-type input)
 - Start with Transcribe (misextensioned)
 - Start with Translate (off-type input)
 - Start with Translate (on-type input)
 - Start with Vector search (off-type input)
 - Start with Vector search (on-type input)

P2.44 - .TEST_INPUT METHOD NULL ARGUMENT TESTS
0 - Call help to see all arguments [If there are more, set of subsets must be expanded]
 - Null all arguments
 - [Null each argument and, if few enough, by MECE sets]

P2.45 - .TEST_INPUT LOCAL_FILE_PATH TYPE CHECK TESTS
- As integer
- As boolean
- As list
- As dictionary

P2.46 - .TEST_INPUT LOCAL_FILE_PATH VALIDITY TESTS
- Random string
- Empty string
- Valid, but does not start with period
- Valid, but does not start with period or slash
- Valid, but starts with period and no slash
- Only directory, does not end in slash
- Only directory, ends in slash
- Only full file name
- File, no extension
- File, period but no extension
- Complete file, but file isn't there
- Complete file, file exists but isn't yaml
- File is fine, but name is a single character
- File is fine, but name includes Chinese and accented Latin Characters
- File is fine, but name is impossibly long

P2.47 - .TEST_INPUT WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.48 - .INPUTSTRUCTURE AND .OUTPUTSTRUCTURE FOR EACH MODULE TESTS [Use code cell from the end of 1.5 in Intro-Modular-Pipelines]
0 - Call help on this to see if there's anything other than .data_example [If yes, expand as necessary]
 - For Caption
 - For JSON-to-TXT
 - For Keyword search
 - For OCR
 - For Parser
 - For Sentiment
 - For Summarize
 - For Text embedder
 - For Transcribe
 - For Translate
 - For Vector search

P2.49 - .INPUTSTRUCTURE AND .OUTPUTSTRUCTURE WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.50 - .MODULE_CHAIN PROPERTY ON INEXISTENT PIPELINE TESTS
 - Attempt on an inexistent module

P2.51 - .MODULE_CHAIN PROPERTY ON REPLACED PIPELINE TESTS
 - Attempt on a module that's been duplicated

P2.52 - .MODULE_CHAIN PROPERTY ON FAILED PIPELINE TESTS
 - Attempt on a module whose creation failed

P2.53 - .MODULE_CHAIN PROPERTY ON PIPELINES LOADED VS NOT LOADED INTO OPERATOR
 - .module_chain on a pipeline not yet loaded
 - .module_chain on same pipeline now loaded

P2.54 - .MODULE_CHAIN PROPERTY ON SEARCH PIPELINES WITH VS WITHOUT FILES IN THEM
 - .module_chain on semantic search pipeline without file in it
 - .module_chain on same semantic search pipeline with a file in it
 - .module_chain on same semantic search pipeline with multiple files in it
 - .module_chain on keyword search pipeline without file in it
 - .module_chain on same keyword search pipeline with a file in it
 - .module_chain on same keyword search pipeline with multiple files in it

P2.55 - .MODULE_CHAIN PROPERTY ON CURRENT PIPELINE TESTS
[10x] - Run .module_chain on existing pipelines; make sure all modules are covered at least once

P2.56 - .MODULE_CHAIN PROPERTY ON PIPELINE WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection

P2.57 - .LOAD METHOD ON INEXISTENT PIPELINE TESTS
  - Try on an inexistent pipeline

P2.58 - .LOAD METHOD ON REPLACED PIPELINE TESTS
  - Try on an replaced pipeline

P2.59 - .LOAD METHOD ON FAILED PIPELINE TESTS
 - Attempt on a pipeline whose creation failed

P2.60 - .LOAD METHOD ON DIFFERENT PIPELINES TESTS
 - On preexistent single-module pipeline
 - On preexistent multi-module pipeline
 - On preexistent-then-loaded-into single-module pipeline
 - On preexistent-then-loaded-into multi-module pipeline
 - On same-cell single-module pipeline
 - On same-cell multi-module pipeline

P2.61 - .LOAD METHOD NULL ARGUMENT TESTS
0 - Call help to see all arguments
 - Null all arguments
 - [Null each argument and, if few enough, by MECE sets]

P2.62 - .LOAD METHOD ARGUMENT TYPE CHECK TESTS
 - List
 - Integer
 - Boolean
 - Dictionary

P2.63 - .LOAD METHOD CONFIG_PATH ARGUMENT VALIDITY TESTS [RANDOMIZE BETWEEN KEYWORD AND POSITIONAL]
- Random string
- Empty string
- Valid, but does not start with period
- Valid, but does not start with period or slash
- Valid, but starts with period and no slash
- Only directory, does not end in slash
- Only directory, ends in slash
- Only full file name
- File, no extension
- File, period but no extension
- Complete file, but file isn't there
- Complete file, file exists but isn't yaml
- File is fine, but name is a single character
- File is fine, but name includes Chinese and accented Latin Characters
- File is fine, but name is impossibly long

P2.64 - .LOAD METHOD CONFIG_PATH YAML VALIDITY TESTS [RANDOMIZE BETWEEN .YML AND .YAML]
- Yaml is re-extensioned from other sort of file
- Yaml is blank
- Yaml has random content in it
- Yaml is incredibly long and enormous and has random stuff in it
- Yaml has properly formatted single pipeline in it (Krixik generated)
- Yaml has properly formatted single pipeline in it (manually generated)
- Yaml has properly formatted multiple pipelines in it
- Yaml has multiple properly formatted pipelines in it, but also some random crap
- Yaml has properly formatted pipelines in it, but a trillion of them
[2x, or as many as need be] - Yaml has pipeline in it, but it's not quite properly formatted
[2x, or as many as need be] - Yaml has pipeline in it, but it's not all there. Some parts are missing
[2x, or as many as need be] - Yaml has had a single random character thrown in there

P2.65 - .ADD METHOD WITHOUT .INIT OR INTERNET CONNECTION TESTS
 - Attempt without .init
 - Attempt without internet connection
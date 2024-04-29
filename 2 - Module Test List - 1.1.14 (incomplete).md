# MODULE TEST LIST - 1.1.14

### TABLE OF CONTENTS

M1 - .vector_search tests
M2 - .keyword_search tests
M3 - Transcription tests
M4 - OCR tests
M5 - Caption tests
M6 - Sentiment tests
M7 - Summarize tests
M8 - Translate tests
M9 - JSON-to-TXT
M10 - Parser
M11 - Text embedder

[EYYYYYYISHOULDDOFOREACHMODULEAHELPTOSEEWHATARGUMENTSITSHOWS]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M1 - .vector_search tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M1.1 [LEGACY S1.1, LEGACY 2.23] - CLEANING PROCESS TESTS
9r4 - If character-to-string replacement works, upload makes big file bigger than upload limit [Testing that it now short circuits after becoming too big] [[Had many fails here, re-run .1 and .3 and .4. In .1, check that the error message no longer references KrixikSearchPipeline. In .3, make sure that it gives priority to clean_options over default_clean_options when both have same key in kv pair. Similar in .4.]]

M1.2 [LEGACY S1.2, LEGACY 2.44] - PRIOR EMBEDDING TEST REDUX - HALL OF FAME - ALL MODELS
6r2 - [Prev 2.6.11] Dense documents with many words; no spaces or punctuation [[REDO NOW THAT THERE IS LONGER TIMEOUT]] [[Redo .1 and .5, there was an embedding fail issue that looked like a timeout but wasn't. ]]
7r2 - [Prev 2.6.12] Only numbers with spacing [[REDO .1 NOW THAT THERE IS LONGER TIMEOUT]] [[There was an unexplained embedding error before, try again.]]

M1.3 [LEGACY S1.3, LEGACY 2.48] - ASYNC_UPLOAD FUNCTIONALITY TESTS  (try .upload_status after each) [[REDO NOW THAT UPLOAD_STATUS FIXED]]
5r - One file, failed in embedding (compare output with non-async) [[Try calling .process_status with request_id instead of process_id, but only if we've seen it in the text. Also check if original embedding process fails (previous one after ~31 seconds. )]]
6r - One file, failed in parsing/chunking (compare output with non-async) [[Try in the same order as before; first .process, then .process_status, then .process with same sfp, then .list a couple of times]]
8r - Multiple files, one cell, some successful, some failed (compare output with non-async) [[Call .process_status a lot after running this. Maybe try the test a couple of times]]

M1.4 [LEGACY S1.4, LEGACY 2.49] - ASYNC_UPLOAD FOLLOWED BY ANOTHER API
3r - .vector_search while doing async upload [Replicate prior issues of Error 500 when async upload, but after other upload, works / also no files should now go missing]
4r - .vector_search on that same file (its directory) while doing its async upload (result at beginning of file) [Repeat it all, there were many issues]
5r - .vector_search on that same file (its directory) while doing its async upload (result at end of file) [Repeat it, there were a couple of issues]
7r - .delete on that same file while doing its async upload (is this even possible? will there be a file_id in time?) [Repeat it, there were a couple of issues]
9r - .update on that same file while doing its async upload (is this even possible? will there be a file_id in time?) [Repeat it, there were a couple of issues]
13r - .show_tree while doing async upload [Confirm that it no longer shows wrong max_files message at top of output]
14r - .show_tree on that same file (its directory) while doing its async upload [Repeat several times during upload to see if output changes]

M1.5 [LEGACY S1.6, LEGACY 2.56] - DELETE_LATERAL_OUTPUT WITH LOCAL FILE MODIFICATION AND REMOVAL
3.2r2 - Local cleaned file is deleted during .upload [Check that it no longer continues to generate the file if the first one is deleted] [[Repeat, Jeremy tweaked. Check Windows directory error message]]
4.3r2 - Local converted file is deleted during .upload [Check that it no longer continues to generate the file if the first one is deleted] [[Repeat, see if is still continuing from halfway]]

M1.6 [LEGACY S1.8, LEGACY 4.20] - DUPLICATE VALIDITY TESTS
1r - Duplicate file_ids [Should work now that duplicate file_ids error was resolved] [[Try to replicate Error 500 from last time]]

M1.7 [LEGACY S1.9, LEGACY 4.22] - SORT_ORDER FUNCTIONALITY TESTS
1r - Test default: descending? [There was no default sort_order, confirm there is now] [Try to reproduce "It used to tell you that X, Y, and Z files weren't processed for `.vector_search` and give you the result for the rest, and now it fails if but a single file wasn't processed for vector search."]

M1.8 [LEGACY S1.10, LEGACY 4.25] - FILE_NAME STUBS/SUBSTRINGS
8r2 - Substring is within prefix [Replicate error from last time: "Inexplicably failed with 'FAILURE: Error querying user files'"]

M1.9 [LEGACY S1.11, LEGACY 4.26] - MAX_FILES VALIDITY TESTS
1r2 - 5 (low number, exact) [Repeat, there were multiple failures]

M1.10 [LEGACY S1.13, LEGACY 4.28] - KEY STUMP IN FILE_TAGS FUNCTIONALITY TESTS
2r - Multiple matches for single key stump [Check that it now queries all files]
3r - Multiple key stumps, some have matches [Check that it now queries all files]
4r - Multiple key stumps, all have matches [Check that crazy listing inconsistency is gone]
5r - Key is there twice, once with stump, one without, both valid [Replicate that it lists all files]
7r - Key stump works when new file tag is added into key stump [Should not ignore file just uploaded]
9r - Mixed with file_name in same .list [Check that strange error is no more]

M1.11 [LEGACY S1.16, LEGACY 4.37] - ATTEMPT .VECTOR_SEARCH BY PROCESS_ID (all should fail)
3r - Vector_search by .show_tree process_id [Check that type check fail no longer fails: "It should tell me that sdps should not be lists, but should only be strings. Period. Not comment on the formatting of my list."]

M1.12 [LEGACY 10.5] - .PROCESS_STATUS SCENARIO TESTS [Run .process_status on each of these]
[-][][][] - Properly uploaded file, not processed for vector search
 - .upload failed during upload, embedding
 - .upload failed during upload, parsing/chunking
 - .upload failed before upload

M1.13 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M1.14 - KEYWORD SEARCH ON NON-KEYWORD-SEARCH PIPELINE TESTS
- Run .keyword_search on one of these pipelines

[[FOR LATER, BENCHMARKING]] 2.43 - QUANTIZED VS UNQUANTIZED COMPARISON TESTS (2X FILES, SAME SFP)
[[FOR LATER, BENCHMARKING]] - Need space/size comparison, when available [[All others were done in Macrobatch 5]]

[[FOR LATER, BENCHMARKING]] - [2.29-2] - PDF UPLOAD - CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - PDF with vertical text
[[FOR LATER, BENCHMARKING]] - PDF with upside-down text
[[FOR LATER, BENCHMARKING]] - PDF with enormous spaces
[[FOR LATER, BENCHMARKING]] - Non-machine-generated pdf (scan)
[[FOR LATER, BENCHMARKING]] - PDF with all images
[[FOR LATER, BENCHMARKING]] - PDF with text in images
[[FOR LATER, BENCHMARKING]] - PDF with strange font
[[FOR LATER, BENCHMARKING]] - PDF with default_clean_options-addressable characters
[[FOR LATER, BENCHMARKING]] - PDF with Cyrillic characters
[[FOR LATER, BENCHMARKING]] - PDF with Mandarin characters
[[FOR LATER, BENCHMARKING]] - PDF with footnotes
[[FOR LATER, BENCHMARKING]] - PDF with comments

[[FOR LATER, BENCHMARKING]] - [prev(?) 2.31] - DOCX UPLOAD - CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - Txt to docx to txt - query comparison
[[FOR LATER, BENCHMARKING]] - Txt to docx to txt - line comparison
[[FOR LATER, BENCHMARKING]] - Pdf to docx to txt - query comparison
[[FOR LATER, BENCHMARKING]] - Pdf to docx to txt - line comparison
[[FOR LATER, BENCHMARKING]] - Oddly formatted docx - Structure match
[[FOR LATER, BENCHMARKING]] - Docx with annoying format with several headers and such
[[FOR LATER, BENCHMARKING]] - Docx with long narrow columns
[[FOR LATER, BENCHMARKING]] - Docx with vertical text
[[FOR LATER, BENCHMARKING]] - Docx with upside-down text
[[FOR LATER, BENCHMARKING]] - Docx with enormous spaces
[[FOR LATER, BENCHMARKING]] - Non-machine-generated Docx (scan)
[[FOR LATER, BENCHMARKING]] - Docx with all images
[[FOR LATER, BENCHMARKING]] - Docx with text in images
[[FOR LATER, BENCHMARKING]] - Docx with strange font
[[FOR LATER, BENCHMARKING]] - Docx with default_clean_options-addressable characters
[[FOR LATER, BENCHMARKING]] - Docx with Cyrillic characters
[[FOR LATER, BENCHMARKING]] - Docx with Mandarin characters
[[FOR LATER, BENCHMARKING]] - Docx with footnotes
[[FOR LATER, BENCHMARKING]] - Docx with comments

[[FOR LATER, BENCHMARKING]] - [prev(?) 2.33] - PPTX UPLOAD - CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - Oddly formatted pptx - Structure match
[[FOR LATER, BENCHMARKING]] - Pptx with annoying format with several headers and such
[[FOR LATER, BENCHMARKING]] - Pptx with long narrow columns
[[FOR LATER, BENCHMARKING]] - Pptx with vertical text
[[FOR LATER, BENCHMARKING]] - Pptx with upside-down text
[[FOR LATER, BENCHMARKING]] - Pptx with enormous spaces [several blank slides]
[[FOR LATER, BENCHMARKING]] - Non-machine-generated Pptx (scan)
[[FOR LATER, BENCHMARKING]] - Pptx with all images
[[FOR LATER, BENCHMARKING]] - Pptx with text in images
[[FOR LATER, BENCHMARKING]] - Pptx with default_clean_options-addressable characters
[[FOR LATER, BENCHMARKING]] - Pptx with Cyrillic characters
[[FOR LATER, BENCHMARKING]] - Pptx with Mandarin characters
[[FOR LATER, BENCHMARKING]] - PDF with notes at bottom
[[FOR LATER, BENCHMARKING]] - PDF with comments

[[FOR LATER, BENCHMARKING]] - [prev(?) 2.34] - MULTI-PATH CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - Docx-pdf-txt vs docx-txt
[[FOR LATER, BENCHMARKING]] - Pptx-pdf-txt vs pptx-txt
[[FOR LATER, BENCHMARKING]] - Pdf-docx-txt vs pdf-txt

[[FOR LATER, BENCHMARKING]] - ASSORTED TXT FORMATS
[[FOR LATER, BENCHMARKING]] - Longform prose
[[FOR LATER, BENCHMARKING]] - Poetry
[[FOR LATER, BENCHMARKING]] - Manual
[[FOR LATER, BENCHMARKING]] - Prose in Spanish
[[FOR LATER, BENCHMARKING]] - Prose in Mandarin
[[FOR LATER, BENCHMARKING]] - Invoices
[[FOR LATER, BENCHMARKING]] - Chat history
[[FOR LATER, BENCHMARKING]] - Emails
[[FOR LATER, BENCHMARKING]] - A bunch of numbers w/ spaces
[[FOR LATER, BENCHMARKING]] - A bunch of numbers without spaces
[[FOR LATER, BENCHMARKING]] - Unicode characters
[[FOR LATER, BENCHMARKING]] - Very short text file (1-2 sentences)
[[FOR LATER, BENCHMARKING]] - 10,000 rows with one '1'
[[FOR LATER, BENCHMARKING]] - Same line 10,000 times
[[FOR LATER, BENCHMARKING]] - Blank text file
[[FOR LATER, BENCHMARKING]] - Dense document with many words separated by spaces. No periods or newlines
[[FOR LATER, BENCHMARKING]] - Dense documents with many words; no spaces or punctuation
[[FOR LATER, BENCHMARKING]][[[[[[See the A Great Many Words, missing]]]]]]

[[FOR LATER, BENCHMARKING]] - QUANTIZED VS UNQUANTIZED SPEED COMPARISON TESTS [Files from 2.43?]
[[FOR LATER, BENCHMARKING]] - Model 1 - Speed comparison, quantized vs unquantized, after warm-up
[[FOR LATER, BENCHMARKING]] - Model 2 - Speed comparison, quantized vs unquantized, after warm-up
[[FOR LATER, BENCHMARKING]] - Model 3 - Speed comparison, quantized vs unquantized, after warm-up
[[FOR LATER, BENCHMARKING]] - Model 4 - Speed comparison, quantized vs unquantized, after warm-up
[[FOR LATER, BENCHMARKING]] - Model 5 - Speed comparison, quantized vs unquantized, after warm-up

[[FOR LATER, BENCHMARKING]] - INTER-EMBEDDING-MODEL SPEED COMPARISON TESTS [Files from 2.43?]
[[FOR LATER, BENCHMARKING]] - Inter-model speed ranking

[[FOR LATER, BENCHMARKING]] - EMBEDDING MODEL ACCURACY COMPARISON TEST (all 10 models) [[THIS IS THE CORE OF THE EMBEDDING ACCURACY BENCHMARKING TEST SET]]
## Jeremy comment: ### WE ALSO NEED BASELINE TESTS - INPUT AND EXPECTED OUTPUT - CAN YOU COOK UP 5 OF EACH VECTOR AND KEYWORD SEARCH? ###
[[FOR LATER, BENCHMARKING]] - File with just ~10 similar sentences; result "ranking" test (no chunk overlap) 2x
[[FOR LATER, BENCHMARKING]] - Full novel, normal sentence 2x
[[FOR LATER, BENCHMARKING]] - Full novel, seeded sentences 2x

[[FOR LATER, BENCHMARKING]] - PRIOR DISTANCE TESTS - HALL OF FAME - ALL MODELS [Does this add value? Comparing distances of different results] [BENCHMARK!]
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.1] - Same file (same sentence twice)
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.2] - Same file (same sentence every time)
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.3] - Same file (punctuation in one instance of same sentence, not in another)
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.4] - Same file - Caps all off in one instance, not in another
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.5] - Same file - spacing all off in one instance, not in another
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.6] - Same file - different gibberishpunctuation "word" in the middle in both
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.7] - Synonyms in same file
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.8] - String reduction - Same string 10 words vs 8 vs 6 vs 4 vs 2
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.9] - Identical files, different positions
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.10] - Different file (same sentence)
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.11] - Different file (full file to one-liner)
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.12] - File of similar sentences, to see low numbers in sentences (below 0.3)
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.13] - File of very different sentences, to see high numbers in sentences (above 0.7)
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.14] - File of only numbers - sentence
[[FOR LATER, BENCHMARKING]] - [Prev 4.19.15] - File of gibberish sentences

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M2 - .keyword_search tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M2.1 [LEGACY S2.4, LEGACY 7.23] - KEYWORD SEARCH FUNCTIONALITY TESTS - STOP WORDS
3r3 - Query is largely stop words, and document is entirely stop words [Had multiple fails last time, re-run]

M2.2 [LEGACY S2.5, LEGACY 7.28] - PROCESS_ID REFLECTION TESTS
1r2 - Confirm process_id when .keyword_search fails (err 500) [Check that process_id is reflected now and this error message is gone: "{'status_code': 504, 'message': 'Endpoint request timed out'}"]

M2.3 [LEGACY S2.6, LEGACY 7.32] - TOKEN_NUMBER ACCURACY TESTS
1r - Normal word, once in file [Check that in results it calls it 'word' and not 'keyword']

M2.4 [LEGACY S2.8, LEGACY 10.5] - .UPLOAD_STATUS SCENARIO TESTS
2r - .upload failed during upload [Check that process_id deletion gremlin doesn't strike this time]

M2.5 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M2.6 - VECTOR SEARCH ON NON-VECTOR-SEARCH PIPELINE TESTS
- Run .vector_search on one of these pipelines

[[FOR LATER, BENCHMARKING]] - [2.29-2] - PDF UPLOAD - CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - PDF with vertical text
[[FOR LATER, BENCHMARKING]] - PDF with upside-down text
[[FOR LATER, BENCHMARKING]] - PDF with enormous spaces
[[FOR LATER, BENCHMARKING]] - Non-machine-generated pdf (scan)
[[FOR LATER, BENCHMARKING]] - PDF with all images
[[FOR LATER, BENCHMARKING]] - PDF with text in images
[[FOR LATER, BENCHMARKING]] - PDF with strange font
[[FOR LATER, BENCHMARKING]] - PDF with default_clean_options-addressable characters
[[FOR LATER, BENCHMARKING]] - PDF with Cyrillic characters
[[FOR LATER, BENCHMARKING]] - PDF with Mandarin characters
[[FOR LATER, BENCHMARKING]] - PDF with footnotes
[[FOR LATER, BENCHMARKING]] - PDF with comments

[[FOR LATER, BENCHMARKING]] - [prev(?) 2.31] - DOCX UPLOAD - CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - Txt to docx to txt - query comparison
[[FOR LATER, BENCHMARKING]] - Txt to docx to txt - line comparison
[[FOR LATER, BENCHMARKING]] - Pdf to docx to txt - query comparison
[[FOR LATER, BENCHMARKING]] - Pdf to docx to txt - line comparison
[[FOR LATER, BENCHMARKING]] - Oddly formatted docx - Structure match
[[FOR LATER, BENCHMARKING]] - Docx with annoying format with several headers and such
[[FOR LATER, BENCHMARKING]] - Docx with long narrow columns
[[FOR LATER, BENCHMARKING]] - Docx with vertical text
[[FOR LATER, BENCHMARKING]] - Docx with upside-down text
[[FOR LATER, BENCHMARKING]] - Docx with enormous spaces
[[FOR LATER, BENCHMARKING]] - Non-machine-generated Docx (scan)
[[FOR LATER, BENCHMARKING]] - Docx with all images
[[FOR LATER, BENCHMARKING]] - Docx with text in images
[[FOR LATER, BENCHMARKING]] - Docx with strange font
[[FOR LATER, BENCHMARKING]] - Docx with default_clean_options-addressable characters
[[FOR LATER, BENCHMARKING]] - Docx with Cyrillic characters
[[FOR LATER, BENCHMARKING]] - Docx with Mandarin characters
[[FOR LATER, BENCHMARKING]] - Docx with footnotes
[[FOR LATER, BENCHMARKING]] - Docx with comments

[[FOR LATER, BENCHMARKING]] - [prev(?) 2.33] - PPTX UPLOAD - CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - Oddly formatted pptx - Structure match
[[FOR LATER, BENCHMARKING]] - Pptx with annoying format with several headers and such
[[FOR LATER, BENCHMARKING]] - Pptx with long narrow columns
[[FOR LATER, BENCHMARKING]] - Pptx with vertical text
[[FOR LATER, BENCHMARKING]] - Pptx with upside-down text
[[FOR LATER, BENCHMARKING]] - Pptx with enormous spaces [several blank slides]
[[FOR LATER, BENCHMARKING]] - Non-machine-generated Pptx (scan)
[[FOR LATER, BENCHMARKING]] - Pptx with all images
[[FOR LATER, BENCHMARKING]] - Pptx with text in images
[[FOR LATER, BENCHMARKING]] - Pptx with default_clean_options-addressable characters
[[FOR LATER, BENCHMARKING]] - Pptx with Cyrillic characters
[[FOR LATER, BENCHMARKING]] - Pptx with Mandarin characters
[[FOR LATER, BENCHMARKING]] - PDF with notes at bottom
[[FOR LATER, BENCHMARKING]] - PDF with comments

[[FOR LATER, BENCHMARKING]] - [prev(?) 2.34] - MULTI-PATH CONVERSION TESTS
[[FOR LATER, BENCHMARKING]] - Docx-pdf-txt vs docx-txt
[[FOR LATER, BENCHMARKING]] - Pptx-pdf-txt vs pptx-txt
[[FOR LATER, BENCHMARKING]] - Pdf-docx-txt vs pdf-txt

[[FOR LATER, BENCHMARKING]] - ASSORTED TXT FORMATS
[[FOR LATER, BENCHMARKING]] - Longform prose
[[FOR LATER, BENCHMARKING]] - Poetry
[[FOR LATER, BENCHMARKING]] - Manual
[[FOR LATER, BENCHMARKING]] - Prose in Spanish
[[FOR LATER, BENCHMARKING]] - Prose in Mandarin
[[FOR LATER, BENCHMARKING]] - Invoices
[[FOR LATER, BENCHMARKING]] - Chat history
[[FOR LATER, BENCHMARKING]] - Emails
[[FOR LATER, BENCHMARKING]] - A bunch of numbers w/ spaces
[[FOR LATER, BENCHMARKING]] - A bunch of numbers without spaces
[[FOR LATER, BENCHMARKING]] - Unicode characters
[[FOR LATER, BENCHMARKING]] - Very short text file (1-2 sentences)
[[FOR LATER, BENCHMARKING]] - 10,000 rows with one '1'
[[FOR LATER, BENCHMARKING]] - Same line 10,000 times
[[FOR LATER, BENCHMARKING]] - Blank text file
[[FOR LATER, BENCHMARKING]] - Dense document with many words separated by spaces. No periods or newlines
[[FOR LATER, BENCHMARKING]] - Dense documents with many words; no spaces or punctuation
[[FOR LATER, BENCHMARKING]][[[[[[See the A Great Many Words, missing]]]]]]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M3 - Transcription tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M3.1 [LEGACY S3.1, LEGACY 2.56] - DELETE_LATERAL_OUTPUT WITH LOCAL FILE MODIFICATION AND REMOVAL
4.3r2 - Local converted file is deleted during .upload [Failed in several ways, re-run]

M3.2 [LEGACY S3.3, LEGACY BS2.1] - FILE ITSELF
6r2 - MP3 too big [Re-run it all, failed in a couple of ways]
9r2 - MP4 too long (but within size cap) (check what size cap is now; 180 secs is too short for production) [Check if length cap issue is still issue]

M3.3 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M3.4 - KEYWORD SEARCH ON NON-KEYWORD-SEARCH PIPELINE TESTS
- Run .keyword_search on one of these pipelines

M3.5 - VECTOR SEARCH ON NON-VECTOR-SEARCH PIPELINE TESTS
- Run .vector_search on one of these pipelines

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M4 - OCR tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M4.1 [LEGACY S4.1, LEGACY BS7.1] - FILE ITSELF
+++***8r2 - JPG too small [Confirm that error message is now correct, not about "not representing a valid image"]

M4.2 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M4.3 - KEYWORD SEARCH ON NON-KEYWORD-SEARCH PIPELINE TESTS
- Run .keyword_search on one of these pipelines

M4.4 - VECTOR SEARCH ON NON-VECTOR-SEARCH PIPELINE TESTS
- Run .vector_search on one of these pipelines

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M5 - Caption tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M5.1 [LEGACY S5.1, LEGACY BS6.1] - FILE ITSELF
14r2 - JPG too small [Confirm that error message is now correct, not about "not representing a valid image"]

M5.2 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M5.3 - KEYWORD SEARCH ON NON-KEYWORD-SEARCH PIPELINE TESTS
- Run .keyword_search on one of these pipelines

M5.4 - VECTOR SEARCH ON NON-VECTOR-SEARCH PIPELINE TESTS
- Run .vector_search on one of these pipelines

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M6 - Sentiment tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M6.1 [LEGACY S6.3, LEGACY BS3.3] - KEY TESTS
5r2 - Key is excessively long [Two fails before: first, error message had a stroke and was just redtext opener, 2nd error message in disorder]

M6.2 [LEGACY S6.4, LEGACY BS3.4] - VALUE CONTENT TESTS
1r2 - Value is integer [Check that error message post-type checking is now more clear]
2r2 - Value is boolean [Check that error message post-type checking is now more clear]
3r2 - Value is list [Check that error message post-type checking is now more clear]

M6.3 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M6.4 - KEYWORD SEARCH ON NON-KEYWORD-SEARCH PIPELINE TESTS
- Run .keyword_search on one of these pipelines

M6.5 - VECTOR SEARCH ON NON-VECTOR-SEARCH PIPELINE TESTS
- Run .vector_search on one of these pipelines

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M7 - Summarize tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M7.1 [LEGACY S7.3, LEGACY BS5.3] - KEY TESTS
1r2 - Single - key is empty string [confirm that minimum length for keys has been added]
5r2 - Key is excessively long [confirm length cap for keys has been added]

M7.2 [LEGACY S7.4, LEGACY BS5.4] - VALUE CONTENT TESTS
1r2 - Value is integer [Confirm type checking error is good now, not about 'split' attribute]
2r2 - Value is boolean [Confirm type checking error is good now, not about 'split' attribute]
3r2 - Value is list [Confirm type checking error is good now, not about 'split' attribute]
7r3 - Value is same word a great many times [confirm set time cap to 10 minutes]
19r2 - Value is long list of words/names [confirm set time cap to 10 minutes]

M7.3 [LEGACY S7.5, LEGACY BS5.5] - ESTABLISHED TEXT TESTS
1r2 - Try established texts: Cat in the Hat [Check if timeout is now indeed 10min]
2r2 - Try established texts: Wikipedia for United States [Check if timeout is now indeed 10min]
3r2 - Try established texts: The Lottery [Check if timeout is now indeed 10min]
[[FOR LATER, DEFAULT MODEL SUCKS]] - Try established texts: Reddit Ts&Cs
[[FOR LATER, DEFAULT MODEL SUCKS]] - Try established texts: Famous letter
[[FOR LATER, DEFAULT MODEL SUCKS]] - Other texts: Invoice
[[FOR LATER, DEFAULT MODEL SUCKS]] - Other texts: A chat log

M7.4 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M7.5 - KEYWORD SEARCH ON NON-KEYWORD-SEARCH PIPELINE TESTS
- Run .keyword_search on one of these pipelines

M7.6 - VECTOR SEARCH ON NON-VECTOR-SEARCH PIPELINE TESTS
- Run .vector_search on one of these pipelines

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M8 - Translate tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

M8.1 [LEGACY S8.3, LEGACY BS4.3] - KEY TESTS
5r2 - Key is excessively long [Two fails before: first, error message had a stroke and was just redtext opener, 2nd error message in disorder]

M8.2 [LEGACY S8.4, LEGACY BS4.4] - VALUE CONTENT TESTS
1r2 - Value is integer [Check that type check error is better/clearer]
2r2 - Value is boolean [Check that type check error is better/clearer]

M8.3 - HELP TO SEE ALL ARGUMENTS TESTS
- Run help on module to see if there are any arguments we're not aware of. [If so, more tests will have to be added]

M8.4 - KEYWORD SEARCH ON NON-KEYWORD-SEARCH PIPELINE TESTS
- Run .keyword_search on one of these pipelines

M8.5 - VECTOR SEARCH ON NON-VECTOR-SEARCH PIPELINE TESTS
- Run .vector_search on one of these pipelines

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## M9 - JSON-to-TXT tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
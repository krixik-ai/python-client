# SYSTEM TEST LIST - 1.1.14

Note: 1.1.13 technically existed but no tests were run on it, it was skipped

ALL TESTS HERE MUST BE RANDOMIZED BETWEEN PIPELINES
ALL TESTS HERE MUST BE RANDOMIZED BETWEEN PIPELINES
ALL TESTS HERE MUST BE RANDOMIZED BETWEEN PIPELINES
ALL TESTS HERE MUST BE RANDOMIZED BETWEEN PIPELINES

### TABLE OF CONTENTS

S0 - Test pipeline setup
S1 - .process tests
S2 - .list tests
S3 - .delete tests
S4 - .update tests
S5 - .show_tree tests
S6 - .upload_status tests
S7 - .fetch_output test
S8 - Inter-app wall tests
S9 - Other tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S0 - Test pipeline setup

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

S0.1 - SET UP SINGLE-MODULE PIPELINES FOR TESTS
1 - Caption
2 - OCR
3 - Keyword search
4 - Vector search
5 - Sentiment analysis
6 - Summarize
7 - Translate
8 - Transcribe
9 - Text embedder
10 - Parser
11 - Json-to-txt

S0.2 - SET UP MULTI-MODULE PIPELINES FOR TESTS
1 - Translate → Sentiment Analysis
2 - Transcribe → Vector Search
3 - OCR → Summarize → Translate

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S1 - .process tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

S1.1 [LEGACY G1.1null, LEGACY 2.48] - ASYNC_UPLOAD FUNCTIONALITY TESTS (try .upload_status after each) [[REDOING NOW THAT WAIT_FOR_PROCESS ISSUES ARE RESOLVED]]
3r2 - One file, enormous but feasible [[Repeat, as rest of batch was skipped]]
 - One file, just too big
 - Multiple files, one cell, all successful, same pipeline
 - Multiple files, one cell, all successful, similar pipeline
 - Multiple files, one cell, all successful, different pipeline
 - Multiple files, one cell, some successful, some failed, same pipeline (compare output with non-async)
 - Multiple files, one cell, some successful, some failed, similar pipeline (compare output with non-async)
 - Multiple files, one cell, some successful, some failed, different pipeline (compare output with non-async)
 - [Multiple, as necessary to check sufficient models] - Multiple files, one cell, all failed differently (compare output with non-async)
 - [Multiple, as necessary to check sufficient models] - Multiple simultaneous async uploads, different cells (compare output with non-async)

S1.2 [LEGACY G1.2null, LEGACY 2.49] - ASYNC_UPLOAD FOLLOWED BY ANOTHER API
[2x] - .list while doing async upload
[2x] - .list on that same file (its directory) while doing its async upload
[2x] - .delete while doing async upload
[2x] - .delete on that same file while doing its async upload (is this even possible? will there be a file_id in time?)
[2x] - .update while doing async upload
[2x] - .update on that same file while doing its async upload (is this even possible? will there be a file_id in time?)
[2x] - .show_tree while doing async upload
[2x] - .show_tree on that same file (its directory) while doing its async upload
[2x] - .upload_status while doing async upload
[2x] - .upload_status on that same file while doing its async upload
[2x] - overload; try to have as many files as possible async uploading (they'll all have to be enormous). Use a For loop

S1.3 [LEGACY G1.3null, LEGACY 2.50] - ASYNC_UPLOAD COMPARISONS [[REDOING NOW THAT WAIT_FOR_PROCESS ISSUES ARE RESOLVED]]
[2x] - Compare async_upload with Verbose on 'True' vs on 'False'
[3x] - Compare non-async warm .process API speed while vs while not async uploading
[3x] - Compare warm .list API speed while vs while not async uploading
[3x] - Compare warm .update API speed while vs while not async uploading

S1.4 [LEGACY G1.4null, LEGACY 2.51] - ASYNC_UPLOAD DUPLICATE GENERATION [[REDOING NOW THAT WAIT_FOR_PROCESS ISSUES ARE RESOLVED]]
[2x] - Same sfp, duplicate upload starts after first async upload starts and finishes after first async upload ends 
[2x] - Same sfp, duplicate upload starts after first async upload starts and finishes before first async upload ends
[2x] - Update into same sfp happens while async upload is happening (may do test 2-3 times, varying the timing)

S1.5 [LEGACY G1.1, LEGACY BS1.3]- NULL ARGUMENT TESTS
18r2 - Check that it now tells you that no timestamp windows were specified [Transcribe] [[Could not replicate, try again]]

S1.6 [LEGACY G1.3, LEGACY BS1.14] - DUPLICATE FILES, DIFFERENT API [[REDOING NOW THAT FILES AREN'T BEING 'DELETED']] [[No repeats, and the two XXXXXs must be different]]
0r - First confirm that duplicates are still being addressed as used to be.
1r2 - Caption upload, OCR .upload creates duplicate (rerun all the code cells; this was the mess that revealed how bad the non-inter-API wall issue was)
 - XXXXX upload, XXXXX .update creates duplicate
 - XXXXX upload, XXXXX .upload creates duplicate
 - XXXXX upload, XXXXX .update creates duplicate
 - XXXXX upload, XXXXX .upload creates duplicate
 - XXXXX upload, XXXXX .update creates duplicate
 - XXXXX upload, XXXXX .upload creates duplicate
 - XXXXX upload, XXXXX .update creates duplicate
 - XXXXX upload, XXXXX .upload creates duplicate
 - XXXXX upload, XXXXX .update creates duplicate
 - XXXXX upload, XXXXX .upload creates duplicate
 - XXXXX upload, XXXXX .update creates duplicate

S1.7 [LEGACY BS1.16] - ASYNC_UPLOAD TESTS [[REDOING NOW THAT WAIT_FOR_PROCESS ISSUES ARE RESOLVED]]
5r2 - Sentiment_analysis, then summarize (the issue here was that I called upload_status on both files "too quickly" and it told me that processing hadn't begun. must reproduce)
7r - Test for this: When .upload is run with async_upload set to 'True', it gives upload_process_id in the verbose text, but process_id in the returned json, and they're the same. We have to be consistent with the labeling here. The verbose text says "INFO: This file's upload process_id is: ce543c40-7a3b-488f-fb66-72a205673e10 and will be returned to you as process_id." to address this, but that just makes it more confusing.

S1.8 [LEGACY G1.4] - PROCESS REPLACING UPLOAD TESTS
1r - Attempt .upload, then .process for same file (just attempt `.upload` first) [OCR] [[Check if 'KrixikBase/SearchPipeline error still arises]]
2r - Attempt .upload, then .process for same file (just attempt `.upload` first) [Caption] [[Check if 'KrixikBase/SearchPipeline error still arises]]
3r - Attempt .upload_status, then .process_status for same file (just attempt `.upload_status` first) [Sentiment] [[Check if 'KrixikBase/SearchPipeline error still arises]]
4r - Attempt .upload_status, then .process_status for same file (just attempt `.upload_status` first) [Vector] [[Check if 'KrixikBase/SearchPipeline error still arises]]
7r - Attempt to feed .process_status a process_id, then a request_id (ex-.process) [Caption] [[Check process_/request_id labels now]]
8r - Attempt to feed .process_status a process_id, then a request_id (ex-.process) [Transcribe] [[Confirms inter-pipeline wall for `.process_status`]]
9r - Confirm upload_process_id now process_id in .process output [Summarize] [[Check process_/request_id labels now]]

S1.9 [LEGACY G1.5] - FILE_NAME NOW OPTIONAL TESTS
4r - Multiple file_names null (10 in one cell, same pipeline, not all null) (confirm with list) [[Check if error message still off]]

S1.10 [LEGACY G1.6] - SERVER-SIDE TIMEOUT DELETION TESTS [[HOW ABOUT SOME IDEAS THIS TIME?]]
 - Exceed 15-second limit on presigned_url (server or client? determine)
[3x] - Exceed 30sec upload limit
 - Attempt .list on all time-exceeded uploads from test above

S1.11 [LEGACY G1.7] - EXPIRE_TIME DEFAULT TESTS [[Repeat both, was saying that would automatically delete file in timestamp-in-past]]
1r - Valid expire_time [Summarize]
2r - Default expire_time [Sentiment]

S1.12 [LEGACY G1.8] - EXPIRE_TIME TYPE_CHECK TESTS
3r - As boolean [Keyword] [[See if now gives proper type check error]]

S1.13 [LEGACY G1.9] - EXPIRE_TIME VALIDITY TESTS [[WE HAD ISSUES WITH THE WORDING OF THE ERROR MESSAGES]]
1r - Negative [Summarize]
3r - Zero [Search]
4r - Low positive integer [Search]
5r - Very high integer [Search]

S1.14 [LEGACY G1.10] - EXPIRE_TIME .LIST CONFIRMATION TESTS [[CHECK THAT TIMEZONE ISSUE IS NOW FIXED]]
1r - Test processed through .list

S1.15 [LEGACY G1.12] - EXPIRE_TIME BUMPUP TESTS [[Check how much bumpup is now, was showing as ~5hrs]]
1 - Heavy file with 1min expire_time (doable) [Search]

S1.16 [LEGACY G1.13] - POST-EXPIRY CONFIRMATION TESTS
2r - .update [Check if it's type-checking, or argument-checking, or what]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S2 - .list tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

S2.1 [LEGACY G2.2, LEGACY 3.24] - UPDATED AND CREATED TIMESTAMP TYPE CHECK TESTS [All four tested within each test]
1r3 - String (normal, date only) [Confirm that now files outside timestamp window are at end of output, not beginning/middle]

S2.2 [LEGACY G2.4, LEGACY 3.34] - HIGH VOLUME LIST TESTS
1r - Listing over 100 files would've generated a DynamoDB error, Error 500. Should be fixed now [[Formal test for >100 listing and file deletion issue]]

S2.3 [LEGACY G2.5, LEGACY BS1.8] - .LIST ARGUMENT TESTS
[[FOR WHEN .LIST INTER-PPLN WALL IS UP]]8r - File_ids, three equal, others there as well (Before I popped a Summarize file_id in there and it was listed. Try that again)
54r.1 - Symbolic_file_paths, three equal, others there as well (Now you can use the /[file_name] symbolic_file_path, in theory) [[Test was all fucked]]

S2.4 [LEGACY G2.7, LEGACY BS1.19] - MAX_FILES TESTS
1r - Transcribe, .list, max_files hit (confirm that files are no longer random selection but default to descending with max_files hit) [[Same check]]
3r - Image_caption, .list, max_files hit (confirm that files are no longer random selection but default to descending with max_files hit) [[Same check]]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S3 - .delete tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

S3.1 [LEGACY G3.1] - VERBOSE TYPE CHECK TESTS
2r - Boolean [Check that (a) verbose now applies for .delete and (b) that, if it doesn't, it's not type checking the thing]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S4 - .update tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

S4.1 [LEGACY G4.1] - EXPIRE_TIME TYPE_CHECK TESTS
3r - As boolean [Caption] (check that we're now getting proper type check error and that it's not taking boolean as an int)

S4.2 [LEGACY G4.2] - EXPIRE_TIME VALIDITY TESTS [[Check that error message is better now, was that ugly one about XX seconds into the future]]
1 - Negative [Search]
3 - Zero [Summarize]
4 - Low positive integer [Caption]
5 - Very high integer [Caption]

S4.3 [LEGACY G4.3] - EXPIRE_TIME .LIST CONFIRMATION TESTS
1r - Test processed through .list [[Check that time zones are working properly now]]

S4.4 [LEGACY G4.4] - EXPIRE_TIME EXACT TRIGGER TIME TESTS [[Check that time zone issue is no longer plaguing this]]
1 - Test with default seconds (confirm exact system time first) [Sentiment]
2 - Test with 3600 seconds (confirm exact system time first) [Summarize]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S5 - .show_tree tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

S5.1 [LEGACY G5.2, LEGACY 9.5] - ROOT TESTS
2r2 - Specific root '/', file in root [Test now that we've decided to allow root uploads] [[Must redo, "file delete" bug made this one impossible]]
4r2 - Specific root '/', some structure beneath and file in root [Check if output is better] [[Must redo, "file delete" bug made this one impossible, also oddly slow]]
5r - Root stump '/*', file in root [Test now that we've decided to allow root uploads] [[Check if root for this and above are exact same, and if "treetest file is missing"]]
6r2 - Root stump '/*', some structure beneath and file in root [Check if json is now consistent with showing directories yes/no, confirm that Verbose is False] [[Check if JSON shows directories (it shouldn't), and if verbose is true (should be by default)]]

S5.2 [LEGACY 9.7] - SPECIFIC DIRECTORY TESTS - ANALOG [[For when we can go over 100 files]]
3 - Thousands of files (under max_files) [Wasn't able to perform before] [[For when we can go over 100 files]]
4 - Thousands of files (over max_files) [Wasn't able to perform before] [[For when we can go over 100 files]]

S5.3 [LEGACY 9.9] - STUMP TESTS - ANALOG [[For when we can go over 100 files]]
7 - Thousands of files (under max_files), in a few levels above [Wasn't able to perform before] [[For when we can go over 100 files]]
8 - Thousands of files (over max_files), in a few levels above [Wasn't able to perform before] [[For when we can go over 100 files]]
9 - Thousands of levels (under max_files) [Wasn't able to perform before] [[For when we can go over 100 files]]
10 - Thousands of levels (over max_files) [Wasn't able to perform before] [[For when we can go over 100 files]]

S5.4 [LEGACY G5.6, LEGACY BS1.19] - MAX_FILES TESTS
4r2 - Summarize, .show_tree, max_files hit [[Should now outright reject sdps, as it's not an argument for show_tree]]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S6 - .upload_status tests

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

S6.1 [LEGACY G6.2, LEGACY 10.2] - NULL ARGUMENT TESTS
2r - Null verbose [Translate] [[Do again, got weird error message last time]]
3r - Null upload_process_id [Sentiment] [[Check if verbose is now activated for .upload_status]]

S6.2 [LEGACY G6.3, LEGACY 10.3] - UPLOAD_PROCESS_ID TYPE CHECK TESTS [[Confirm that request_id vs process_id label issue has been sorted out for both]]
1r - Boolean [Translate]
2r - Integer [Caption]

S6.3 [LEGACY 10.6] - VERBOSE TYPE CHECK TESTS [[First check if verbose is even active for .upload_status]]
- List
- Unformatted string

S6.4 [LEGACY G6.6, LEGACY 10.7] - .UPLOAD_STATUS WITHOUT INTERNET CONNECTION
1 - Attempt without having an internet connection [OCR] [[Check if error message is still weird]]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S7 - .fetch_output

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

No tests this batch.

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S8 - Other

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

No tests this batch

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

## S9 - Inter-app wall [FIRST DETERMINE WHAT THE UNITS ARE BEFORE I ADJUST THIS (E.G. ADD KEYWORD? TRANSCRIBE VS TRANSCRIPTION?); TEST SET REMAINS FROM BS LIST] [[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]]

----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------

[[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]] G8.1 [LEGACY BS8.1] - SEARCH UPLOADS
1 - .list with transcribe (file_id)
2 - .show_tree with sentiment_analysis (sdp)
3 - .delete with translate (file_id)
4 - .fetch_output with image_caption (file_id)
5 - .update with OCR (file_id)
6 - .upload_status with summarize (upload_process_id)

[[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]] G8.2 [LEGACY BS8.2] - TRANSCRIBE UPLOADS
1 - .list with image_caption (file_id)
2 - .show_tree with OCR (sdp)
3 - .delete with search (file_id)
4 - .fetch_output with summarize (file_id)
5 - .update with transcribe (file_id)
6 - .upload_status with sentiment analysis (upload_process_id)

[[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]] G8.3 [LEGACY BS8.3] - SENTIMENT_ANALYSIS UPLOADS
1 - .list with OCR (file_id)
2 - .show_tree with transcribe (sdp)
3 - .delete with image_caption (file_id)
4 - .fetch_output with summarize (file_id)
5 - .update with translate (file_id)
6 - .upload_status with search (upload_process_id)

[[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]] G8.4 [LEGACY BS8.4] - TRANSLATE UPLOADS
1 - .list with summarize (file_id)
2 - .show_tree with search (sdp)
3 - .delete with OCR (file_id)
4 - .fetch_output with translate (file_id)
5 - .update with transcribe (file_id)
6 - .upload_status with sentiment analysis (upload_process_id)

[[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]] G8.5 [LEGACY BS8.5] - IMAGE_CAPTION UPLOADS
1 - .list with sentiment analysis (file_id)
2 - .show_tree with transcribe (sdp)
3 - .delete with translate (file_id)
4 - .fetch_output with summarize (file_id)
5 - .update with OCR (file_id)
6 - .upload_status with search (upload_process_id)

[[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]] G8.6 [LEGACY BS8.6] - OCR UPLOADS
1 - .list with search (file_id)
2 - .show_tree with sentiment analysis (sdp)
3 - .delete with image_caption (file_id)
4 - .fetch_output with summarize (file_id)
5 - .update with translate (file_id)
6 - .upload_status with transcribe (upload_process_id)

[[WILL NOT EXECUTE UNTIL THIS BATCH'S INTER-APP WALL IDENTIFIED ISSUE FIXED]] G8.7 [LEGACY BS8.7] - SUMMARIZE UPLOADS
1 - .list with OCR (file_id)
2 - .show_tree with transcribe (sdp)
3 - .delete with search (file_id)
4 - .fetch_output with sentiment_analysis (file_id)
5 - .update with image_caption (file_id)
6 - .upload_status with translate (upload_process_id)
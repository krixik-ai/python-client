from tests.krixik import text_files_path, audio_files_path, json_files_path, image_files_path, npy_files_path


test_data = {
    "json-to-txt": [ 
        {"local_file_path": f"{json_files_path}valid_1.json"},
        {"local_file_path": f"{json_files_path}valid_2.json"},
    ]
}

test_data_multi = {
    "standard-vector-search": [
        {"local_file_path": f"{text_files_path}1984_short.txt"}
    ],
    "transcribe-translate-vector-search": [
        {"local_file_path": f"{audio_files_path}valid_1.mp3"}
    ],
}

test_failure_data = {
    "standard-vector-search": [
        {"local_file_path": f"{text_files_path}random_chars.txt"}
    ],
}
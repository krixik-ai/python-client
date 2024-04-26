from tests.krixik import text_files_path, audio_files_path, json_files_path, image_files_path, npy_files_path


test_data = {
    "keyword-search": [ 
        {"local_file_path": f"{text_files_path}1984_short.txt"},
        {"local_file_path": f"{text_files_path}war_of_the_worlds_short.txt"},
    ]
}


wait_for_test_data = {
    "keyword-search": [
        {"local_file_path": f"{text_files_path}1984_full.txt"},
    ]
}

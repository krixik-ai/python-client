from tests.krixik import text_files_path, audio_files_path, json_files_path, image_files_path, npy_files_path

module_test_data = {
    "caption": [ 
        {"local_file_path": f"{image_files_path}restaurant.png"},
        ],
    "json-to-txt": [
        {"local_file_path": f"{json_files_path}valid_1.json"}
    ],
    "keyword-db": [
        {"local_file_path": f"{text_files_path}1984_short.txt"}
    ],
    "ocr": [
        {"local_file_path": f"{image_files_path}seal.png"}
    ],
    "parser": [
        {"local_file_path": f"{text_files_path}1984_short.txt"}
    ],
    "sentiment": [
        {"local_file_path": f"{json_files_path}valid_1.json"}
    ],
    "summarize": [
        {"local_file_path": f"{text_files_path}sample_article.txt"}
    ],
    "text-embedder": [
        {"local_file_path": f"{json_files_path}valid_1.json"}
    ],
    "transcribe": [
        {"local_file_path": f"{audio_files_path}valid_1.mp3"}
    ],
    "translate": [
        {"local_file_path": f"{json_files_path}valid_1.json"}
    ],
    "vector-db": [
        {"local_file_path": f"{npy_files_path}valid_1.npy"}
    ],
}

from krixik.modules import available_modules

assert available_modules == list(module_test_data.keys())
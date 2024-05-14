import os
from pathlib import Path

text_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/text/"
)
json_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/json/"
)
audio_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/audio/"
)
image_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/images/"
)
video_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/video/"
)
npy_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/npy/"
)
faiss_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/faiss/"
)
pipeline_configs_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/pipeline_configs/"
)
output_files_path = (
    Path(os.path.abspath(__file__)).parent.parent.__str__() + "/test_files/output_data"
)
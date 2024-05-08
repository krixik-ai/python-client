import pytest
from krixik.utilities.validators.data import available_data_types
from krixik.utilities.validators.data.utilities.read_config import get_allowable_data_types


# as of 2024-04-01
current_data_types = ["docx", "pdf", "text", "audio", "json", "video", "image", "pptx", "npy"]


def test_available_data_types():
    print(f"available_data_types {available_data_types}")
    
    assert available_data_types == current_data_types


test_data = [
    ("image", [".jpg", ".jpeg", ".png"]),
    ("audio", [".mp3", ".mp4"]),
    ("json", [".json"]),
    ("text", [".txt", ".pdf", ".pptx", ".docx"]),
]


@pytest.mark.parametrize("data_type, extensions", test_data)
def test_get_allowable_data_types(data_type, extensions):
    assert set(get_allowable_data_types(data_type)) == set(extensions)

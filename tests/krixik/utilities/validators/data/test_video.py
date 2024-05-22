# from krixik.utilities.validators.data.video import is_valid
# from krixik.utilities.validators.data.video import is_size
# from tests.krixik import video_files_path
# import pytest

# # first - check is_valid
# test_failure_data = [
#     video_files_path + "invalid_1.mp3",
# ]


# @pytest.mark.parametrize("local_file_path", test_failure_data)
# def test_1(local_file_path):
#     with pytest.raises((ValueError, TypeError, FileNotFoundError)):
#         is_valid(local_file_path=local_file_path)


# test_success_data = [
#     video_files_path + "valid_1.mp4",
# ]


# @pytest.mark.parametrize("local_file_path", test_success_data)
# def test_2(local_file_path):
#     assert is_valid(local_file_path=local_file_path) is None


# # second - check is_size
# test_failure_data = [
#     video_files_path + "/" + "Empty McFile.mp4",  # 0 bytes
# ]


# @pytest.mark.parametrize("local_file_path", test_failure_data)
# def test_3(local_file_path):
#     with pytest.raises((ValueError, TypeError, IOError, FileNotFoundError)):
#         is_size(
#             local_file_path=local_file_path,
#             minimum_seconds=3,
#             maximum_seconds=180,
#             minimum_file_size=0.000001,
#             maximum_file_size=100.0,
#         )


# test_success_data = [
#     video_files_path + "valid_1.mp4",
# ]


# @pytest.mark.parametrize("local_file_path", test_success_data)
# def test_4(local_file_path):
#     assert (
#         is_size(
#             local_file_path=local_file_path,
#             minimum_seconds=3,
#             maximum_seconds=180,
#             minimum_file_size=0.000001,
#             maximum_file_size=100.0,
#         )
#         is None
#     )

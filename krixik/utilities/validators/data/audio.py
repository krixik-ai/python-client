import os
from typing import Optional
from krixik.utilities.validators.data import file_size_check

# from pydub import AudioSegment
# from moviepy.editor import AudioFileClip
# from pydub.exceptions import PydubException


# def is_valid(local_file_path: str | None) -> None:
#     if local_file_path is None:
#         raise ValueError("input file is None")

#     # check that local_file_path represents audio file
#     try:
#         duration = 100
#         AudioSegment.from_file(local_file_path, format="mp3", duration=duration)
#     except PydubException as e:
#         raise ValueError(f"input file is not a valid audio file - {local_file_path} - see exception {e}")
#     except FileNotFoundError:
#         raise FileNotFoundError(f"The file '{local_file_path}' does not exist.")
#     except Exception as e:
#         raise ValueError(f"Error reading audio: {e}")


def is_valid(local_file_path: Optional[str]) -> None:
    if local_file_path is None:
        raise ValueError("input local_file_path is None")
    if not isinstance(local_file_path, str):
        raise ValueError(f"input local_file_path is not a string: '{local_file_path}'")
    if not local_file_path.endswith("mp3"):
        raise ValueError(f"input local_file_path does not end with required extension 'mp3' {local_file_path}")


def is_size(
    *,
    local_file_path: str,
    minimum_seconds: int = 1,
    maximum_seconds: int = 180,
    minimum_file_size: float = 0.00001,
    maximum_file_size: float = 3.000001,
) -> None:
    # proper size
    def compute_size(file_path: str):
        try:
            # Get the size of the file in bytes
            file_size_bytes = os.path.getsize(file_path)

            # Convert the size to megabytes (MB)
            file_size_mb = file_size_bytes / (1024 * 1024)
            return file_size_mb
        except Exception as e:
            raise ValueError(f"audio extraction failed with exception {e}")

    # def compute_duration(file_path: str) -> float:
    #     try:
    #         audio_clip = AudioFileClip(file_path)
    #         duration_in_seconds = round(audio_clip.duration, 1)
    #         audio_clip.close()
    #         return duration_in_seconds
    #     except Exception as e:
    #         raise ValueError(f"audio duration calculation failed with exception {e}")

    try:
        # check that local_file_path is valid
        is_valid(local_file_path)

        # compute file size
        file_size = compute_size(local_file_path)

        # check that file size in megabytes is greater than minimum_file_size and less than maximum_file_size
        file_size_check(local_file_path, file_size, minimum_file_size, maximum_file_size)

        # # compute length of audio file in seconds
        # audio_duration = compute_duration(local_file_path)

        # # check that audio file is  greater than minimum_seconds and less than maximum_seconds
        # if audio_duration < minimum_seconds or audio_duration > maximum_seconds:
        #     raise ValueError(
        #         f"audio file is {round(audio_duration,2)} seconds - this is either less than {minimum_seconds} seconds (current minimum size allowable) or greater than {maximum_seconds} seconds (current maximum size allowable)"
        #     )
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"audio extraction failed with exception {e}")

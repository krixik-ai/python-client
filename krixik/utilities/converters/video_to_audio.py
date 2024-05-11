import os
from moviepy.editor import VideoFileClip
from krixik.utilities.validators.system.base.utilities.decorators import (
    file_converters_input_check,
)
from krixik.utilities.validators.data.video import is_size as is_video_size
from krixik.utilities.validators.data.audio import is_size as is_audio_size
from krixik.utilities.utilities import vprint


def delete_file(*, file_path: str, exception: str) -> None:
    if file_path is not None:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise ValueError(f"audio extraction failed with exception: {str(exception)}")


@file_converters_input_check
def extract_audio(*, local_file_path: str, audio_filepath: str) -> None:
    try:
        video = VideoFileClip(local_file_path)
        audio = video.audio
        if audio is not None:
            audio.write_audiofile(audio_filepath, verbose=False, logger=None)
    except Exception as e:
        raise ValueError(f"error extracting audio from video {local_file_path}, exception: {e}")


@file_converters_input_check
def convert(
    *,
    local_file_path: str | None,
    local_save_directory: str | None,
    verbose: bool = True,
) -> str:
    """video to audio converter - strips audio mp3 from video file using moviepy library

    Parameters
    ----------
    local_file_path : str | None
        path to local file to convert
    local_save_directory : str | None
        local directory to save converted file
    verbose : bool, optional
        by default True

    Returns
    -------
    str | None
        if conversion successful returns path to converted file
    """

    if local_file_path is not None and local_save_directory is not None:
        audio_filepath = None
        try:
            # get file_name video_file_path
            file_name = "krixik_converted_version_" + os.path.splitext(os.path.basename(local_file_path))[0]

            # format audio file path
            extension = ".mp3"
            audio_filepath = os.path.join(local_save_directory, file_name + extension)

            # remove file if it already exists
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)

            # check input file is mp4
            is_video_size(local_file_path=local_file_path, minimum_file_size=0.1)

            # extract audio from video
            extract_audio(local_file_path=local_file_path, audio_filepath=audio_filepath)

            # report size check
            vprint(
                "INFO: Checking that file size falls within acceptable parameters...",
                verbose=verbose,
            )
            is_audio_size(local_file_path=audio_filepath, minimum_file_size=0.05)
            vprint("INFO:...success!", verbose=verbose)

            return audio_filepath
        except ValueError as ve:
            vprint(
                "INFO:...failure!  The converted (audio) file does not fall within acceptable size parameters.",
                verbose=verbose,
            )
            if audio_filepath is not None:
                delete_file(file_path=audio_filepath, exception=str(ve))
            raise
        except AttributeError as ae:
            if audio_filepath is not None:
                delete_file(file_path=audio_filepath, exception=str(ae))
            raise ValueError(f"video contains no visual content, cannot convert to audio - {local_file_path}")
        except Exception as e:
            if audio_filepath is not None:
                delete_file(file_path=audio_filepath, exception=str(e))
            raise
    else:
        raise ValueError("the input local_file_path and/or local_save_directory is null")

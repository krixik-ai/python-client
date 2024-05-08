from krixik.utilities.validators.data.audio import is_size as is_audio_size
from krixik.utilities.validators.data.video import is_size as is_video_size
from krixik.utilities.validators.data.text import is_size as is_text_size
from krixik.utilities.validators.data.pdf import is_size as is_pdf_size
from krixik.utilities.validators.data.json import is_size as is_json_size
from krixik.utilities.validators.data.image import is_size as is_image_size
from krixik.utilities.validators.data.docx import is_size as is_docx_size
from krixik.utilities.validators.data.pptx import is_size as is_pptx_size
from krixik.utilities.validators.data.npy import is_size as is_npy_size

from krixik.utilities.validators.data.utilities.read_config import get_all_allowable_extensions


def datatype_validator(func):
    def wrapper(*args, **kwargs):
        try:
            if "local_file_path" in list(kwargs.keys()):
                local_file_path = kwargs["local_file_path"]
                extension = local_file_path.split(".")[-1]
                allowable_extensions = get_all_allowable_extensions()
                if "." + extension not in allowable_extensions:
                    raise ValueError(f"invalid file extension: {extension} - currently only {get_all_allowable_extensions} are allowed.")

                if extension == "txt":
                    is_text_size(local_file_path=local_file_path)
                elif extension == "pdf":
                    is_pdf_size(local_file_path=local_file_path)
                elif extension == "json":
                    is_json_size(local_file_path=local_file_path)
                elif extension == "jpg" or extension == "jpeg" or extension == "png":
                    is_image_size(local_file_path=local_file_path)
                elif extension == "docx":
                    is_docx_size(local_file_path=local_file_path)
                elif extension == "pptx":
                    is_pptx_size(local_file_path=local_file_path)
                elif extension == "mp3":
                    is_audio_size(local_file_path=local_file_path)
                elif extension == "mp4":
                    is_video_size(local_file_path=local_file_path)
                elif extension == "npy":
                    is_npy_size(local_file_path=local_file_path)
                else:
                    raise ValueError(f"invalid file extension: {extension}")
            return func(*args, **kwargs)
        except ValueError as e:
            raise ValueError(e)
        except Exception as e:
            raise Exception(e)

    return wrapper

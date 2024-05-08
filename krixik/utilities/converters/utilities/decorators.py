import copy
import inspect
import tempfile
from krixik.utilities.converters.read_config import convert_extension
from krixik.utilities.converters.unclean_to_clean_txt import (
    convert as convert_unclean_text,
)
from krixik.utilities.converters.docx_to_txt import convert as convert_docx
from krixik.utilities.converters.pdf_to_txt import convert as convert_pdf
from krixik.utilities.converters.pptx_to_txt import convert as convert_pptx
from krixik.utilities.converters.video_to_audio import convert as convert_video
from krixik.utilities.utilities import vprint, get_input


def datatype_converter_wrapper(func):
    def converter_wrapper(*args, **kwargs):
        try:
            signature = inspect.signature(func)
            verbose = get_input("verbose", signature, kwargs, default_value=True)
            local_file_path = get_input("local_file_path", signature, kwargs, default_value=True)

            if local_file_path is not None:
                extension = local_file_path.split(".")[-1]
                conversion = convert_extension(extension)
                if conversion is not None:
                    with tempfile.TemporaryDirectory() as conversion_save_directory:
                        og_local_file_path = copy.deepcopy(local_file_path)
                        if extension == "mp4":
                            local_file_path = convert_video(
                                local_file_path=local_file_path,
                                local_save_directory=conversion_save_directory,
                                verbose=verbose,
                            )
                        elif extension == "pdf":
                            local_file_path = convert_pdf(
                                local_file_path=local_file_path,
                                local_save_directory=conversion_save_directory,
                                verbose=verbose,
                            )
                        elif extension == "docx":
                            local_file_path = convert_docx(
                                local_file_path=local_file_path,
                                local_save_directory=conversion_save_directory,
                                verbose=verbose,
                            )
                        elif extension == "pptx":
                            local_file_path = convert_pptx(
                                local_file_path=local_file_path,
                                local_save_directory=conversion_save_directory,
                                verbose=verbose,
                            )
                        if local_file_path is not None:
                            if local_file_path.split(".")[-1] != conversion:
                                raise ValueError(f"conversion failed, expected {conversion} got {local_file_path.split('.')[-1]}")

                            vprint(
                                f"converted {og_local_file_path} to: {local_file_path}",
                                verbose=verbose,
                            )
                            # if local_file_path.split(".") == "txt":
                            #     clean_options = None
                            #     if "clean_options" in list(kwargs.keys()):
                            #         if kwargs["clean_options"] is not None:
                            #             clean_options = kwargs["clean_options"]
                            #     use_default_clean_options = False
                            #     if "use_default_clean_options" in list(kwargs.keys()):
                            #         if kwargs["use_default_clean_options"] is not None:
                            #             use_default_clean_options = kwargs[
                            #                 "use_default_clean_options"
                            #             ]
                            #     local_file_path = convert_unclean_text(
                            #         local_file_path=local_file_path,
                            #         local_save_directory=local_save_directory,
                            #         clean_options=clean_options,
                            #         use_default_clean_options=use_default_clean_options,
                            #         verbose=verbose,
                            #     )
                        kwargs["local_file_path"] = local_file_path
                        kwargs["og_local_file_path"] = og_local_file_path
                        return func(*args, **kwargs)
            return func(*args, **kwargs)
        except ValueError as e:
            raise ValueError(e)
        except TypeError as e:
            raise TypeError(e)
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        except PermissionError as e:
            raise PermissionError(e)
        except Exception as e:
            raise Exception(e)

    return converter_wrapper

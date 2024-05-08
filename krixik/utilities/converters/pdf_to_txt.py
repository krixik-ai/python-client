import os
from pypdf import PdfReader
from krixik.utilities.validators.system.base.utilities.decorators import (
    file_converters_input_check,
)
from krixik.utilities.validators.data.pdf import is_size as is_size_pdf
from krixik.utilities.validators.data.text import is_size as is_size_text
from krixik.utilities.utilities import vprint


def delete_file(*, file_path: str, exception: str) -> None:
    if file_path is not None:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise ValueError(
            f"there seems to be a problem with your pdf - file conversion failed with exception {str(exception)} - please check your pdf file of the converter documentation - pypdf - for further information: https://pypdf.readthedocs.io/en/stable/"
        )


@file_converters_input_check
def extract(
    *,
    local_file_path: str,
    local_save_directory: str | None = None,
    verbose: bool = True,
) -> str | None:
    if local_file_path is not None and local_save_directory is not None:
        convert_save_path = ""
        try:
            file_name = "krixik_converted_version_" + os.path.splitext(os.path.basename(local_file_path))[0]
            extension = ".txt"
            convert_save_path = os.path.join(local_save_directory, file_name + extension)

            # remove file if it already exists
            if os.path.exists(convert_save_path):
                os.remove(convert_save_path)

            # creating a pdf reader object
            reader = PdfReader(local_file_path)

            # loop over pages and write to txt
            num = 0
            for page in reader.pages:
                # extract page
                line = page.extract_text()

                if num == 0:
                    with open(convert_save_path, "a", encoding="utf-8") as new_file:
                        new_file.write(line)

                if num > 0:
                    if os.path.exists(convert_save_path):
                        with open(convert_save_path, "a", encoding="utf-8") as new_file:
                            new_file.write(line)
                    else:
                        raise FileNotFoundError(f"file {convert_save_path} does not exist")
                num += 1

            vprint(
                f"SUCCESS: File conversion complete with pydf, result saved to: {convert_save_path}",
                verbose=verbose,
            )

            # report size check
            vprint(
                "INFO: Checking that file size falls within acceptable parameters...",
                verbose=verbose,
            )
            is_size_text(local_file_path=convert_save_path)
            vprint("INFO:...success!", verbose=verbose)

            return convert_save_path
        except ValueError as ve:
            vprint(
                "INFO:...failure!  The converted (text) file does not fall within acceptable size parameters.",
                verbose=verbose,
            )
            delete_file(file_path=convert_save_path, exception=str(ve))
        except Exception as e:
            delete_file(file_path=convert_save_path, exception=str(e))
    else:
        raise ValueError("the input local_file_path and/or local_save_directory is null")


@file_converters_input_check
def convert(
    *,
    local_file_path: str | None,
    local_save_directory: str | None,
    verbose: bool = True,
) -> str:
    """pdf converter - converts pdf file to txt using the pypdf library

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

    if local_file_path is None:
        raise ValueError("local_file_path cannot be None")

    # check if local_file_path is a pdf and convert to text if so
    new_local_file_path = ""
    if "." + local_file_path.split(".")[-1] == ".pdf":
        if local_save_directory is None:
            raise ValueError("local_save_directory cannot be None")

        vprint("INFO: Converting pdf to text...", verbose=verbose)

        # check size and validity of input pdf
        is_size_pdf(local_file_path=local_file_path)

        # convert pdf to text
        new_local_file_path = extract(
            local_file_path=local_file_path,
            local_save_directory=local_save_directory,
            verbose=verbose,
        )

        return new_local_file_path
    return local_file_path

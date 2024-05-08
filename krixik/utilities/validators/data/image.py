import os
import imghdr
from PIL import Image


def is_valid(local_file_path: str) -> bool | None:
    try:
        with open(local_file_path, "rb") as f:
            # Read the first 10 bytes to determine the image type
            header = f.read(10)
            f.seek(0)  # Reset the file pointer to the beginning

            # Use imghdr to determine the image type
            image_type = imghdr.what(None, header)

            # Check if the image type is JPEG or PNG
            if image_type in ["jpg", "jpeg", "png"]:
                return True
            else:
                raise ValueError(f"The file '{local_file_path}' does not represent a valid image.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{local_file_path}' does not exist.")
    except Exception as e:
        raise ValueError(f"Error reading image: {e}")


def is_proportionally_acceptable(local_file_path: str) -> None:
    try:
        # Check if the image is valid
        is_valid(local_file_path)

        # Open the image file
        with Image.open(local_file_path) as img:
            width, height = img.size
            if width == 0 or height == 0:
                raise ValueError("image width or height is 0")

            if width / height < 0.05 or height / width < 0.05:
                raise ValueError("image proportion is less than 0.2: width/height or height/width")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"invalid local_file_path: {e}")


def is_size(
    *,
    local_file_path: str,
    minimum_file_size: float = 0.001,
    maximum_file_size: float = 5.000001,
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
            raise ValueError(f"file size calculation failed with exception {e}")

    try:
        # check that local_file_path represents a valid json file
        is_valid(local_file_path)

        # check size of input json file
        file_size = compute_size(local_file_path)
        if file_size < minimum_file_size or file_size > maximum_file_size:
            raise ValueError(
                f"input file size is {file_size} megabytes: either less than {minimum_file_size} megabytes (current minimum size allowable) or greater than {maximum_file_size} megabytes (current maximum size allowable) - {local_file_path}"
            )
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"invalid local_file_path: {e}")

    # check proportion of input image file
    is_proportionally_acceptable(local_file_path)

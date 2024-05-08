from setuptools import setup
from setuptools import find_packages

setup(
    name="meme_checkr",
    version="1.0.1",
    description="a hello world example",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jeremy Watt",
    email="jermwattml@gmail.com",
    url="https://github.com/jermwatt/meme_checkr",
    packages=find_packages(include=["meme_checkr*"]),
    python_requires=">=3.8",
    entry_points={"console_scripts": ["hello-world-cli = meme_checkr.main:main"]},
    install_requires=[
        "boto3",
        "ffmpeg-python",
        "moviepy",
        "nltk",
        "numpy",
        "pillow",
        "pyaml",
        "pydub",
        "pypdf",
        "pytest",
        "pytest-subtests",
        "python-docx",
        "python-dotenv",
        "python-pptx",
        "requests",
    ],
    extras_require={
        "linting": [
            "pylint",
            "mypy",
            "typing-extensions",
            "ruff",
        ],
        "testing": [
            "pytest",
            "pytest-xdist",
        ],
    },
)

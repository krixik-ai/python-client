from tests.utilities.decorators import capture_printed_output
from tests import TEST_DUMMY_API_KEY_DEV
from tests import TEST_DUMMY_API_URL_DEV
from functools import wraps
from krixik import krixik

krixik_transcribe = krixik.select_pipeline(pipeline="transcribe")


@capture_printed_output
def bad_init():
    krixik.init(
        api_key="c22a233c-3aee-499e-aacd-b5fae12e2f7e",
        api_url="https://12345.execute-api.us-west-2.amazonaws.com/dev",
    )


@capture_printed_output
def good_init():
    krixik.init(api_key=TEST_DUMMY_API_KEY_DEV, api_url=TEST_DUMMY_API_URL_DEV)


def transcribe_bad_init(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = bad_init()
        assert "FAILURE" in result["printed_output"]  # noqa
        return func(*args, **kwargs)

    return wrapper


def transcribe_good_init(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = good_init()
        assert "FAILURE" not in result["printed_output"]  # noqa
        return func(*args, **kwargs)

    return wrapper


def list_all():
    krixik_transcribe = krixik.select_pipeline(pipeline="transcribe")
    return krixik_transcribe.list(symbolic_directory_paths=["/*"])


def confirm_app(items: list):
    apps = [v["pipeline"] for v in items]
    assert all([v == "transcribe" for v in apps])

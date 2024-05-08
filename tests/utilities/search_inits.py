from tests.utilities.decorators import capture_printed_output
from tests import USER_API_KEY_DEV, USER_API_URL_DEV
from functools import wraps
from krixik import krixik

krixik_search = krixik.select_pipeline(pipeline="search")


@capture_printed_output
def bad_init():
    krixik.init(
        api_key="c22a233c-3aee-499e-aacd-b5fae12e2f7e",
        api_url="https://12345.execute-api.us-west-2.amazonaws.com/dev",
    )


@capture_printed_output
def good_init():
    krixik.init(api_key=USER_API_KEY_DEV, api_url=USER_API_URL_DEV)


def search_bad_init(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("\n")
        print("INFO: before bad_init called")
        result = bad_init()
        assert "FAILURE" in result["printed_output"]  # noqa

        print("INFO: after bad_init called")
        return func(*args, **kwargs)

    return wrapper


def search_good_init(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = good_init()
        assert "FAILURE" not in result["printed_output"]  # noqa
        return func(*args, **kwargs)

    return wrapper


@search_good_init
def list_all():
    krixik_search = krixik.select_pipeline(pipeline="search")
    return krixik_search.list(symbolic_directory_paths=["/*"])


def confirm_app(items: list):
    apps = [v["pipeline"] for v in items]
    assert all([v == "search" for v in apps])

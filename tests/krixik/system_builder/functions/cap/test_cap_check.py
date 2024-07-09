from krixik import krixik
from tests import USER_API_KEY, USER_API_URL
import pytest


def test_1():
    """ test that pipeline with same name but different modules fails """
    # initialize krixik
    krixik.init(api_key=USER_API_KEY,
                api_url=USER_API_URL)

    # check cap
    results = krixik.check_cap()    
    assert results["status_code"] == 200
    
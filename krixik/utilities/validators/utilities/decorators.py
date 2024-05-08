from functools import wraps
from krixik.utilities.validators.system.base.utilities.decorators import (
    type_check_inputs as system_base_type_check_inputs,
)
from krixik.utilities.validators.system.data.utilities.decorators import (
    type_check_inputs as system_data_type_check_inputs,
)
from krixik.utilities.validators.system.base.lower_case import lower_case_decorator
from krixik.utilities.validators.data.utilities.decorators import datatype_validator


def type_check_inputs(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = system_base_type_check_inputs(system_data_type_check_inputs(datatype_validator(lower_case_decorator(func))))(
                self, *args, **kwargs
            )

            return result

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

    return wrapper

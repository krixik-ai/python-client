from krixik.utilities.validators.system import EXPIRE_TIME_MIN
from krixik.utilities.validators.system import EXPIRE_TIME_MAX


def expire_time_checker(expire_time: str) -> None:
    # check if expire_time is a int and not bool
    if isinstance(expire_time, bool):
        raise ValueError(f"input expire_time must be an int - INFO: input expire_time type: {type(expire_time)}")

    if not isinstance(expire_time, int):
        raise ValueError(f"input expire_time must be an int - INFO: input expire_time type: {type(expire_time)}")

    # check that expire_time falls with in EXPIRE_TIME_MIN and EXPIRE_TIME_MAX
    if expire_time < EXPIRE_TIME_MIN:
        raise ValueError(f"expire_time {expire_time} must be at least {EXPIRE_TIME_MIN} seconds in the future")
    if expire_time > EXPIRE_TIME_MAX:
        raise ValueError(f"expire_time {expire_time} must be at most {EXPIRE_TIME_MAX} seconds in the future")

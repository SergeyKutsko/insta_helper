from instagrapi import Client
from app.models import Limit

delay_min = Limit.get_limit('MIN_DELAY', 1)
delay_max = Limit.get_limit('MAX_DELAY', 4)


def delay(cl: Client, min_d: int = delay_min, max_d: int = delay_max) -> None:
    """
        Delay for requests

        Parameters
        ----------
        cl: Client object
            Instagram client object
        min_d: int, optional
            Min value delay for requests
        max_d: int, optional
            Max value delay for requests

        Returns
        -------
        None
    """
    return cl.random_delay([min_d, max_d])
from instagrapi import Client
from instagrapi.types import DirectMessage
from typing import List


def send_message(cl: Client,
                 text: str,
                 user_ids: List[int] = [],
                 thread_ids: List[int] = [],
                 ) -> DirectMessage:
    """
        Send a direct message to list of users or threads

        Parameters
        ----------
        cl: Client object
            Instagram client object

        text: str
            String to be posted on the thread

        user_ids: List[int]
            List of unique identifier of Users id

        thread_ids: List[int]
            List of unique identifier of Direct Message thread id

        Returns
        -------
        DirectMessage
            An object of DirectMessage
    """

    cl.direct_send(text, user_ids, thread_ids)
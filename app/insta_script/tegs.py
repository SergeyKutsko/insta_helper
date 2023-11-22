from instagrapi import Client
from app.insta_script.variables import delay
from typing import List


def get_user_pk_by_tag(cl: Client, tag: str, amount: int = 9) -> List[int]:
    """
        Get recent medias for a hashtag

        Parameters
        ----------
        cl: Client object
            Instagram client object

        tag: str
            tag name for search

        amount: int, optional
            Maximum number of media to return, default is 9 -

        Returns
        -------
        List[int]
    """

    medias = cl.hashtag_medias_top(tag, amount)
    delay(cl)
    users_pk = []
    for media in medias:
        media = media.dict()
        users_pk.append(media['user']['pk'])
        delay(cl)
    return users_pk

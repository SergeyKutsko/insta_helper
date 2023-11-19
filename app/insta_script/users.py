from insagrapi import Client
from .variables import delay_min, delay_max


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


def following_to_user_by_followers(cl: Client, user_id: str, amount: int = 0) -> None:
    """
        Follow a user by followers

        Parameters
        ----------
        cl: Client object
            Instagram client object
        user_id: str
            Username for an Instagram account(ID)
        amount: int, optional
            Maximum number of media to return, default is 0 -
            amount=0 - fetch all

        Returns
        -------
        None
    """

    followers = cl.user_followers(user_id=user_id, amount=amount)
    delay(cl)
    for user_id in followers.keys():
        cl.user_follow(user_id)
        delay(cl)


def unfollowing_to_user_by_followers(cl: Client, user_id: str, amount: int = 0) -> None:
    """
        Unfollow a user by followers

        Parameters
        ----------
        cl: Client object
            Instagram client object
        user_id: str
            Username for an Instagram account(ID)
        amount: int, optional
            Maximum number of media to return, default is 0 -
            amount=0 - fetch all

        Returns
        -------
        None
    """
    followers = cl.user_followers(user_id=user_id, amount=amount)
    delay(cl)
    for user_id in followers.keys():
        cl.user_unfollow(user_id)
        delay(cl)


def following_to_user_by_following(cl: Client, user_id: str, amount: int = 0) -> None:
    """
        Follow a user by following

        Parameters
        ----------
        cl: Client object
            Instagram client object
        user_id: str
            Username for an Instagram account(ID)
        amount: int, optional
            Maximum number of media to return, default is 0 -
            amount=0 - fetch all

        Returns
        -------
        None
    """
    followings = cl.user_following(user_id=user_id, amount=amount)
    delay(cl)
    for user_id in followings.keys():
        cl.user_follow(user_id)
        delay(cl)


def unfollowing_to_user_by_following(cl: Client, user_id: str, amount: int = 0) -> None:
    """
        Follow a user by following

        Parameters
        ----------
        cl: Client object
            Instagram client object
        user_id: str
            Username for an Instagram account(ID)
        amount: int, optional
            Maximum number of media to return, default is 0 -
            amount=0 - fetch all

        Returns
        -------
        None
    """
    followings = cl.user_following(user_id=user_id, amount=amount)
    delay(cl)
    for user_id in followings.keys():
        cl.user_unfollow(user_id)
        delay(cl)


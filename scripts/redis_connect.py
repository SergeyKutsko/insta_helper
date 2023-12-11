import os
import redis


def redis_instance():
    return redis.Redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
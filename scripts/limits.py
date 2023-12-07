from app.models import Limit

# Normal limits for one account
limits = {
    'LIMIT_IP': 10,             # use of 10 accounts per IP address (count)
    'MIN_PUBLIC_POST': 4,       # min number publishing of post for account (count)
    'MAX_PUBLIC_POST': 16,      # max number publishing of post for account (count)
    'MIN_PUBLIC_HISTORY': 24,   # min number publishing of history for account (count)
    "MAX_PUBLIC_HISTORY": 48,   # max number publishing of history for account (count)
    "MIN_DELAY": 1,             # min delay after each request (sec)
    "MAX_DELAY": 4,             # max delay after each request (sec)
    "MIN_DIRECT": 7,            # min delay after send message (minutes)
    "MAX_DIRECT": 10,           # max delay after send message (minutes)
}


def run():
    for name, limit in limits.items():
        Limit.objects.create(name=name, limit=limit)

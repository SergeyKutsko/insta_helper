from app.models import Limit

# Normal limits for one account
limits = {
    'LIMIT_IP': 10,             # use of 10 accounts per IP address
    'MIN_PUBLIC_POST': 4,       # min number publishing of post for account
    'MAX_PUBLIC_POST': 16,      # max number publishing of post for account
    'MIN_PUBLIC_HISTORY': 24,   # min number publishing of history for account
    "MAX_PUBLIC_HISTORY": 48,   # max number publishing of history for account
    "MIN_DELAY": 1,             # min delay after each request
    "MAX_DELAY": 4              # max delay after each request
}


def run():
    for name, limit in limits.items():
        Limit.objects.create(name=name, limit=limit)

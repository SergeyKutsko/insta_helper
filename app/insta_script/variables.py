from .app.models import Limit

delay_min = Limit.get_limit('MIN_DELAY', 1)
delay_max = Limit.get_limit('MAX_DELAY', 4)
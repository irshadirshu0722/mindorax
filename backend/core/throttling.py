from django.core.cache import cache
from time import time

class RateLimiter:
  def __init__(self,key,limit,window):
    self.key = key
    self.limit = limit
    self.window = window


  def is_allowed(self):
    current_time = int(time())
    window_key = f"{self.key}:{current_time // self.window}"
    count = cache.get(window_key, 0)
    if count > self.limit:
      return False
    cache.incr(window_key)
    cache.expire(window_key,self.window)
    return True
  
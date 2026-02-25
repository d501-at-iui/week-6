# your code here ...

from apputil import Genius

# Exercise 1
genius = Genius(access_token = "access_token")
"""
Python class Genius initialize object, saves access token as an attribute.
"""

class Genius:
    def __init__ (self, access_token):
        self.access_token = access_token
# Comment
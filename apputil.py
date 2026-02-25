# your code here ...

from apputil import Genius
import json

# Exercise 1
genius = Genius(access_token = "access_token")
"""
Python class Genius initialize object, saves access token as an attribute.
"""

class Genius:
    def __init__ (self, access_token):
        self.access_token = access_token
#Exercise 2
    search_term = 'Audioslave'
    genius.get_artist(search_term)
    """Extract most likely 'Primary' Artist_ID from the first 'hit'
        of the search
     Use API path under 'Artists' for this Artist_ID to pull info. about artist
    """
    genius_search_url = f"http://api.genius.com/search?=
                        {search_term}&access_token={ACCESS_TOKEN}"
    response = requests.get(genius_search_url)
    json_data = response.json()
    



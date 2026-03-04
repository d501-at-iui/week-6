# your code here ...

import os
import requests
import json

# Exercise 1
"""
Python class Genius initialize object, saves access token as an attribute.
"""
class Genius:
    def __init__ (self, access_token):
        self.access_token = access_token
#Exercise 2
    """Extract most likely 'Primary' Artist_ID from the first 'hit'
    of the search
    Use API path under 'Artists' for this Artist_ID to pull info. about artist
"""
    def get_artist(self, search_term):
        search_url = f"https://api.genius.com/search?q={search_term}"
        headers = {"Authorization": "Bearer " + self.access_token}
        #send search request
        response = requests.get(search_url, headers=headers)
        data = response.json() #reads returned keys
        #extract artist ID
        artist_id = data["response"]["hits"][0]["result"]["primary_artist"]["id"]
        #artist lookup
        artist_url = f"https://api.genius.com/artists/{artist_id}"
        response = requests.get(artist_url, headers=headers)
        artist_data = response.json()
        return artist_data
       
genius = Genius(access_token = os.getenv("ACCESS_TOKEN"))

print(genius.get_artist("Drake"))

""" Create another method .get_artists(search_terms)
    which takes a list, returns a df containing a row for each
    search term, and the columns search_term, artist_name, artist_id and followings_count
"""
#example: genius_get.artists(['Rihanna, 'Tycho', 'Seal', 'U2'])


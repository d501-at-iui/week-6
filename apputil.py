# your code here ...

import os
import requests
import json
import pandas as pd

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
    def get_artists(self, search_terms):
    #similar to previous exercise
        headers = {"Authorization": "Bearer " + self.access_token}
        rows = []
        for term in search_terms:
            search_url = f"https://api.genius.com/search?q={term}"
            response = requests.get(search_url, headers=headers)
            data = response.json()
            hits = data["response"]["hits"]

        # was runnin into issue creating dataframe 
        #prevents IndexError: out of range, gives None if there are errors and tels you where
            if len(hits) == 0:
                rows.append({
                "search_term": term,
                "artist_name": None,
                "artist_id": None,
                "followers_count": None
            })
                continue


    #extract primary artist id 
            artist_id = data["response"]["hits"][0]["result"]["primary_artist"]["id"]
    #lookup
            artist_url = f"https://api.genius.com/artists/{artist_id}"
            response = requests.get(artist_url, headers=headers)
            artist_data = response.json()
    #extract primary artist object
            artist = artist_data["response"]["artist"]
    #build dict
            rows.append({
                "search_term": term,
                "artist_name": artist["name"],
                "artist_id": artist["id"],
                "followers_count": artist["followers_count"]
            })
        return pd.DataFrame(rows)

genius = Genius(access_token = os.getenv("ACCESS_TOKEN"))
df = genius.get_artists(['Rihanna', 'Tycho', 'Seal', 'U2'])
print(df)
#print(genius.get_artist("Drake"))

""" Create another method .get_artists(search_terms)
    which takes a list, returns a df containing a row for each
    search term, and the columns search_term, artist_name, artist_id and followings_count"""

    

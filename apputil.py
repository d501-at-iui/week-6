# your code here ...
from __future__ import annotations
from typing import TYPE_CHECKING
from lyricsgenius import Genius as GeniusAPIClient
import pandas as pd
import os
from time import sleep
import time
from numpy.random import uniform
from tqdm import tqdm
import requests

## Exercise 1

# Create a Python class named `Genius` such that the following code initializes the object,
# and "saves" the access token as an attribute of the object. You'll need to use this 
# attribute for Exercises 2 and 3.
#
# ```python
# from apputil import Genius

# genius = Genius(access_token="access_token")
# ```


class Genius:
    BASE_URL = "https://api.genius.com"
    
    def __init__(self, access_token: str, *, timeout: int = 10):
        """Initialize Genius API client."""
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "User-Agent": "GeniusAPIClient/1.0"
            })
        # self.client = GeniusAPIClient(access_token=access_token)
        # You can add more initialization code here if needed
        
        # helpers
        def request(self, endpoint: str, params: dict = None) -> dict:
            """Make a GET request to the Genius API."""
            url = f"{self.BASE_URL}/{endpoint}"
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                return {}
    def search(self, query: str, per_page: int = 15) -> list:
        """Search for songs, artists, or albums."""
        params = {
            "q": query,
            "per_page": per_page
        }
        data = self.request("search", params=params)
        return data.get("response", {}).get("hits", [])
   

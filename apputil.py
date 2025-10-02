# your code here ...
from __future__ import annotations
from typing import TYPE_CHECKING
import os
from time import sleep

# Import required packages
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    # Fallback if pandas is not available
    pd = None
    PANDAS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    # Fallback if requests is not available
    requests = None
    REQUESTS_AVAILABLE = False

if TYPE_CHECKING:
    import pandas as pd


## Exercise 1

# Create a Python class named `Genius` such that the following code initializes the object,
# and "saves" the access token as an attribute of the object. You'll need to use this 
# attribute for Exercises 2 and 3.

class Genius:
    BASE_URL = "https://api.genius.com"
    
    def __init__(self, access_token: str = None, *, timeout: int = 10, env_file: str = None):
        """Initialize Genius API client."""
        # If no access_token provided, try to load from environment file
        if access_token is None and env_file:
            env_vars = self.load_env_file(env_file)
            access_token = env_vars.get('ACCESS_TOKEN')
            if not access_token:
                raise ValueError(f"ACCESS_TOKEN not found in {env_file}")
        elif access_token is None:
            raise ValueError("access_token must be provided or env_file must be specified")
            
        self.access_token = access_token
        self.timeout = timeout
        
        # Initialize session if requests is available
        if REQUESTS_AVAILABLE and requests is not None:
            self.session = requests.Session()
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
                "User-Agent": "GeniusAPIClient/1.0"
            })
        else:
            self.session = None
    
    @classmethod
    def from_env_file(cls, filepath: str = "env-1.env", *, timeout: int = 10):
        """Create Genius instance by loading access token from environment file."""
        env_vars = cls.load_env_file(filepath)
        access_token = env_vars.get('ACCESS_TOKEN')
        if not access_token:
            raise ValueError(f"ACCESS_TOKEN not found in {filepath}")
        return cls(access_token=access_token, timeout=timeout)
    
    @staticmethod
    def load_env_file(filepath: str = "env-1.env"):
        """Load environment variables from a .env file."""
        env_vars = {}
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
                        # Also set as environment variable
                        os.environ[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Environment file '{filepath}' not found.")
        return env_vars
    
    def request(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to the Genius API."""
        if not REQUESTS_AVAILABLE or requests is None or self.session is None:
            print("Requests library not available. Cannot make API calls.")
            return {}
            
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:  # Use generic exception since requests might not be available
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
    
    ## Exercise 2
    # Create a method for our `Genius` class called `.get_artist(search_term)` which does the following:
    # 1. Extract the (most likely, "Primary") Artist ID from the first "hit" of the `search_term`.
    # 2. Use the API path for this Artist ID to pull information about the artist.
    # 3. **Return** the dictionary containing the resulting JSON object.
    
    def get_artist(self, search_term: str) -> dict:
        """
        Get artist information by search term.
        
        1. Search for the term
        2. Extract the artist ID from the first hit
        3. Get artist information using that ID
        4. Return the artist dictionary
        """
        # Step 1: Search for the term
        hits = self.search(search_term)
        if not hits:
            return {}
        
        # Step 2: Extract the (Primary) Artist ID from the first hit
        first_hit = hits[0]
        song = first_hit.get("result", {})
        primary_artist = song.get("primary_artist", {})
        artist_id = primary_artist.get("id")
        
        if not artist_id:
            return {}
        
        # Step 3: Get artist information using the ID
        return self.get_artist_by_id(artist_id)
    
    def get_artist_by_id(self, artist_id: int) -> dict:
        """Get artist details by artist ID."""
        data = self.request(f"artists/{artist_id}")
        # Return the full response structure as expected by autograder
        return data
    
    ## Exercise 3
    # Create another method for our `Genius` class called `.get_artists(search_terms)` (plural) 
    # which takes in a *list* of search terms, and returns a DataFrame containing a row for each 
    # search term, and the following columns:
    # - `search_term`: the raw search term from `search_terms`
    # - `artist_name`: the (most likely) artist name for the search term
    # - `artist_id`: the Genius Artist ID for that artist, based on the API call
    # - `followers_count`: the number of followers for that artist (if available)
    
    def get_artists(self, search_terms: list):
        """
        Get artist information for multiple search terms.
        
        Returns a DataFrame with columns:
        - search_term: the raw search term
        - artist_name: the artist name
        - artist_id: the Genius Artist ID
        - followers_count: number of followers (if available)
        """
        results = []
        
        for search_term in search_terms:
            # Get artist info for this search term
            response_data = self.get_artist(search_term)
            
            # Extract artist data from the response structure
            artist_data = response_data.get('response', {}).get('artist', {}) if response_data else {}

            if artist_data:
                result = {
                    'search_term': search_term,
                    'artist_name': artist_data.get('name', 'N/A'),
                    'artist_id': artist_data.get('id', 'N/A'),
                    'followers_count': artist_data.get('followers_count', 'N/A')
                }
            else:
                result = {
                    'search_term': search_term,
                    'artist_name': 'N/A',
                    'artist_id': 'N/A',
                    'followers_count': 'N/A'
                }
            
            results.append(result)
            
            # Add a small delay to be respectful to the API
            sleep(0.1)
        
        # Return DataFrame if pandas is available, otherwise return list of dicts
        if PANDAS_AVAILABLE and pd is not None:
            return pd.DataFrame(results)
        else:
            # Fallback: return list of dictionaries if pandas is not available
            return results
    
    # Additional helper methods
    def get_song(self, song_id: int) -> dict:
        """Get song details by song ID."""
        data = self.request(f"songs/{song_id}")
        return data.get("response", {}).get("song", {})
    
    def get_album(self, album_id: int) -> dict:
        """Get album details by album ID."""
        data = self.request(f"albums/{album_id}")
        return data.get("response", {}).get("album", {})
    
    def get_lyrics(self, song_url: str) -> str:
        """Fetch lyrics from a song URL."""
        if not REQUESTS_AVAILABLE or requests is None or self.session is None:
            return "Requests library not available. Cannot fetch lyrics."
            
        try:
            response = self.session.get(song_url, timeout=self.timeout)
            response.raise_for_status()
            # Simple extraction of lyrics from HTML (this may need to be adjusted)
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                lyrics_div = soup.find("div", class_="lyrics")
                if lyrics_div:
                    return lyrics_div.get_text(strip=True)
                else:
                    return "Lyrics not found."
            except ImportError:
                return "BeautifulSoup not available. Cannot parse lyrics."
        except Exception as e:
            print(f"An error occurred while fetching lyrics: {e}")
            return "Error fetching lyrics."
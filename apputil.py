import requests
import pandas as pd


class Genius:
    """
    A class for interacting with the Genius API.
    """

    def __init__(self, access_token):
        """
        Initialize the Genius object with an access token.
        """
        self.access_token = access_token
        self.base_url = "https://api.genius.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    # ---------- Exercise 2 ----------
    def get_artist(self, search_term):
        """
        Extract the Artist ID from the first hit of the search_term.
        Use the API path for the Artist ID to pull information about
        the artist.
        Return the dictionary containing the resulting JSON object.
        """
        # Step 1: Search for the artist
        search_url = f"{self.base_url}/search"
        params = {"q": search_term}

        response = requests.get(
            search_url,
            headers=self.headers,
            params=params,
        )
        json_data = response.json()

        # Step 2: Extract the Artist ID from the first hit
        artist_id = json_data["response"]["hits"][0]["result"][
            "primary_artist"
        ]["id"]

        # Step 3: Use the artist ID to fetch artist information
        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(
            artist_url,
            headers=self.headers,
        )

        artist_data = artist_response.json()

        return artist_data

    # ---------- Exercise 3 ----------
    def get_artists(self, search_terms):
        """
        Take in a list of search terms and return a DataFrame
        containing one row per search term with:
        - search_term
        - artist_name
        - artist_id
        - followers_count
        """
        rows = []

        for term in search_terms:
            artist_data = self.get_artist(term)
            artist_info = artist_data["response"]["artist"]

            rows.append(
                {
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get(
                        "followers_count"
                    ),
                }
            )

        df = pd.DataFrame(rows)

        return df
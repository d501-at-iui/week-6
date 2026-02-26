import requests
import pandas as pd


class Genius:
    """
    A utility class for interacting with the Genius API.

    This class allows users to:
    - Search for an artist using a search term
    - Retrieve detailed artist information by ID
    - Collect artist data for multiple search terms into a DataFrame

    Parameters
    ----------
    access_token : str
        A valid Genius API access token.
    """

    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token: str):
        """
        Initialize a Genius object.

        Parameters
        ----------
        access_token : str
            Genius API access token used for authenticated requests.
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    # ------------------------------------------------------------------
    # Internal Helper Methods
    # ------------------------------------------------------------------

    def _search(self, search_term: str, per_page: int = 10) -> dict:
        """
        Perform a search query against the Genius API.

        Parameters
        ----------
        search_term : str
            The search term to query (e.g., artist name).
        per_page : int, optional
            Number of results to return (default is 10).

        Returns
        -------
        dict
            JSON response from the Genius API search endpoint.

        Raises
        ------
        requests.HTTPError
            If the API request fails.
        """
        url = f"{self.BASE_URL}/search"
        params = {
            "q": search_term,
            "per_page": per_page
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def _get_artist_by_id(self, artist_id: int) -> dict:
        """
        Retrieve detailed artist information by Genius artist ID.

        Parameters
        ----------
        artist_id : int
            The Genius artist ID.

        Returns
        -------
        dict
            JSON response containing artist information.

        Raises
        ------
        requests.HTTPError
            If the API request fails.
        """
        url = f"{self.BASE_URL}/artists/{artist_id}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    # ------------------------------------------------------------------
    # Exercise 2
    # ------------------------------------------------------------------

    def get_artist(self, search_term: str) -> dict:
        """
        Retrieve artist information based on a search term.

        This method:
        1. Searches Genius using the provided search term.
        2. Extracts the primary artist ID from the first search hit.
        3. Retrieves detailed artist information using the Artist API endpoint.

        Parameters
        ----------
        search_term : str
            Name of the artist to search for.

        Returns
        -------
        dict
            Dictionary containing the full JSON response for the artist.

        Raises
        ------
        ValueError
            If no search results are found.
        requests.HTTPError
            If an API request fails.
        """
        search_json = self._search(search_term)

        hits = search_json.get("response", {}).get("hits", [])

        if not hits:
            raise ValueError(f"No results found for '{search_term}'")

        first_hit = hits[0]
        artist_id = first_hit["result"]["primary_artist"]["id"]

        artist_json = self._get_artist_by_id(artist_id)

        return artist_json

    # ------------------------------------------------------------------
    # Exercise 3
    # ------------------------------------------------------------------

    def get_artists(self, search_terms: list) -> pd.DataFrame:
        """
        Retrieve artist information for multiple search terms.

        Parameters
        ----------
        search_terms : list of str
            A list of artist names to search for.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing one row per search term with the columns:
            - search_term
            - artist_name
            - artist_id
            - followers_count

        Notes
        -----
        If an artist cannot be found or an API error occurs,
        the corresponding row will contain None values.
        """
        rows = []

        for term in search_terms:
            try:
                artist_json = self.get_artist(term)
                artist_data = artist_json["response"]["artist"]

                rows.append({
                    "search_term": term,
                    "artist_name": artist_data.get("name"),
                    "artist_id": artist_data.get("id"),
                    "followers_count": artist_data.get("followers_count")
                })

            except Exception:
                rows.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(rows)
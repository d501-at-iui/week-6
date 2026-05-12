from __future__ import annotations

import os
from time import sleep

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    pd = None
    PANDAS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None
    REQUESTS_AVAILABLE = False


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class OpenMeteo:
    """Open-Meteo helper class used by the exercises."""

    def __init__(self, access_token: str = None, *, timeout: int = 10,
                 env_file: str = None):
        # Keep access_token for backward compatibility with older exercise calls.
        self.access_token = access_token
        if self.access_token is None and env_file:
            env_vars = self.load_env_file(env_file)
            self.access_token = env_vars.get("ACCESS_TOKEN")
        self.timeout = timeout

    @staticmethod
    def load_env_file(filepath: str = "env-1.env"):
        """Load KEY=VALUE pairs from a .env-style file into os.environ."""
        env_vars = {}
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        env_vars[key] = value
                        os.environ[key] = value
        except FileNotFoundError:
            print(f"Environment file '{filepath}' not found.")
        return env_vars

    @classmethod
    def from_env_file(cls, filepath: str = "env-1.env", *, timeout: int = 10):
        env_vars = cls.load_env_file(filepath)
        return cls(access_token=env_vars.get("ACCESS_TOKEN"), timeout=timeout)

    def request(self, url: str, params: dict = None) -> dict:
        if not REQUESTS_AVAILABLE or requests is None:
            print("Requests library not available. Cannot make API calls.")
            return {}

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    def geocode(self, place_name: str, count: int = 10, language: str = "en") -> list:
        params = {
            "name": place_name,
            "count": count,
            "language": language,
            "format": "json",
        }
        data = self.request(GEOCODING_URL, params=params)
        return data.get("results", [])

    def get_forecast(self, latitude: float, longitude: float, *,
                     hourly: str = "temperature_2m,relative_humidity_2m",
                     timezone: str = "auto", forecast_days: int = 3) -> dict:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": hourly,
            "timezone": timezone,
            "forecast_days": forecast_days,
        }
        return self.request(FORECAST_URL, params=params)

    def get_location(self, search_term: str) -> dict:
        locations = self.geocode(search_term, count=1)
        if not locations:
            return {}
        return locations[0]

    def get_locations(self, search_terms: list):
        rows = []

        for term in search_terms:
            location = self.get_location(term)
            if location:
                rows.append({
                    "search_term": term,
                    "location_name": location.get("name", "N/A"),
                    "latitude": location.get("latitude", "N/A"),
                    "longitude": location.get("longitude", "N/A"),
                })
            else:
                rows.append({
                    "search_term": term,
                    "location_name": "N/A",
                    "latitude": "N/A",
                    "longitude": "N/A",
                })
            sleep(0.05)

        if PANDAS_AVAILABLE and pd is not None:
            return pd.DataFrame(rows)
        return rows

    # Legacy aliases to keep old exercise scripts/tests working.
    def get_artist(self, search_term: str) -> dict:
        return self.get_location(search_term)

    def get_artists(self, search_terms: list):
        df_or_rows = self.get_locations(search_terms)
        if PANDAS_AVAILABLE and pd is not None and hasattr(df_or_rows, "rename"):
            return df_or_rows.rename(
                columns={
                    "location_name": "artist_name",
                    "latitude": "artist_id",
                    "longitude": "followers_count",
                }
            )
        return df_or_rows


class Genius(OpenMeteo):
    """Backward-compatible alias for older notebook/exercise imports."""

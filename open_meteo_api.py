import requests
import pandas as pd
from tqdm import tqdm
import numpy as np
from concurrent.futures import ProcessPoolExecutor


def geocode(place_name, count=10, language="en"):
    """
    Query Open-Meteo Geocoding API for location coordinates.
    
    Parameters:
    -----------
    place_name : str
        The name of the place to search for (e.g., "Bloomington, Indiana")
    count : int
        Maximum number of results to return (default: 10)
    language : str
        Language for results (default: "en")
    
    Returns:
    --------
    dict
        JSON response from the API with location data
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": place_name,
        "count": count,
        "language": language
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def forecast(latitude, longitude, hourly_variables=None, timezone="auto", forecast_days=3):
    """
    Query Open-Meteo Forecast API for weather data.
    
    Parameters:
    -----------
    latitude : float
        Latitude coordinate
    longitude : float
        Longitude coordinate
    hourly_variables : list, optional
        List of hourly variables to retrieve (e.g., ["temperature_2m", "precipitation"])
    timezone : str
        Timezone for results (default: "auto" for automatic detection)
    forecast_days : int
        Number of days to forecast (default: 3)
    
    Returns:
    --------
    dict
        JSON response from the API with forecast data
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "forecast_days": forecast_days
    }
    
    if hourly_variables:
        params["hourly"] = ",".join(hourly_variables)
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def forecast_to_df(place_name, hourly_variables=None, timezone="auto", forecast_days=3):
    """
    Get forecast data for a place and convert to a pandas DataFrame.
    
    Parameters:
    -----------
    place_name : str
        The name of the place (e.g., "Bloomington, Indiana")
    hourly_variables : list, optional
        List of hourly variables to retrieve
    timezone : str
        Timezone for results (default: "auto")
    forecast_days : int
        Number of days to forecast (default: 3)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with forecast data
    """
    # Get location coordinates
    geo_data = geocode(place_name)
    if not geo_data.get("results"):
        raise ValueError(f"No location found for '{place_name}'")
    
    location = geo_data["results"][0]
    lat, lon = location["latitude"], location["longitude"]
    
    # Get forecast
    forecast_data = forecast(lat, lon, hourly_variables=hourly_variables, 
                            timezone=timezone, forecast_days=forecast_days)
    
    # Convert to DataFrame
    hourly = forecast_data.get("hourly", {})
    if hourly:
        df = pd.DataFrame(hourly)
        # Expand nested structures if needed using apply(pd.Series)
        return df
    
    return pd.DataFrame()


def forecast_to_dfs(place_names, hourly_variables=None, timezone="auto", forecast_days=3):
    """
    Get forecast data for multiple places and return as DataFrames.
    
    Parameters:
    -----------
    place_names : list
        List of place names
    hourly_variables : list, optional
        List of hourly variables to retrieve
    timezone : str
        Timezone for results (default: "auto")
    forecast_days : int
        Number of days to forecast (default: 3)
    
    Returns:
    --------
    dict
        Dictionary mapping place names to their DataFrames
    """
    results = {}
    for place_name in tqdm(place_names, desc="Fetching forecasts"):
        try:
            results[place_name] = forecast_to_df(place_name, hourly_variables=hourly_variables,
                                               timezone=timezone, forecast_days=forecast_days)
        except Exception as e:
            print(f"Error fetching data for {place_name}: {e}")
            results[place_name] = pd.DataFrame()
    
    return results


# ============================================================================
# Testing and Example Usage
# ============================================================================

def testing():
    """Test basic geocoding and forecast functionality."""
    print("Testing 1: Basic geocoding...")
    result = geocode("Bloomington, Indiana")
    if result.get("results"):
        print(f"  Found: {result['results'][0]['name']}, {result['results'][0]['country']}")
    
    print("Testing 2: Forecast to DataFrame...")
    df = forecast_to_df("Chicago, Illinois", hourly_variables=["temperature_2m"])
    print(f"  DataFrame shape: {df.shape}")
    print(f"  Columns: {list(df.columns)[:3]}...")


def job_test(place_name):
    """Helper function for multiprocessing - get forecast data for a single place."""
    try:
        return place_name, forecast_to_df(place_name, hourly_variables=["temperature_2m"])
    except Exception as e:
        print(f"Error for {place_name}: {e}")
        return place_name, pd.DataFrame()


def multiprocessing_example(place_names, num_workers=4):
    """
    Example of using multiprocessing to fetch data for multiple places in parallel.
    """
    results = {}
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(job_test, name) for name in place_names]
        for future in tqdm(futures, desc="Processing"):
            place_name, df = future.result()
            results[place_name] = df
    
    return results


if __name__ == "__main__":
    testing()
    print("Testing 3: Multiprocessing...")
    places = ["Bloomington, Indiana", "Chicago, Illinois", "New York, USA"]
    results = multiprocessing_example(places)
    print(f"  Retrieved data for {len(results)} places")

"""Legacy compatibility wrappers backed by Open-Meteo helpers.

This file is kept only to avoid breaking older imports.
New code should import from open_meteo_api.py directly.
"""

from open_meteo_api import (  # noqa: F401
    NAME_DEMO,
    forecast_to_df,
    forecast_to_dfs,
    geocode,
    job_test,
    testing,
)


def genius(search_term, per_page=15):
    """Legacy name retained for compatibility.

    Returns geocoding results (list of location dictionaries).
    """
    count = max(1, min(int(per_page), 100))
    return geocode(search_term, count=count)


def genius_to_df(search_term, n_results_per_term=10, **kwargs):
    """Legacy wrapper to keep older scripts functional."""
    return forecast_to_df(
        search_term,
        forecast_days=kwargs.get("forecast_days", 3),
        verbose=kwargs.get("verbose", True),
        savepath=kwargs.get("savepath"),
    )


def genius_to_dfs(search_terms, **kwargs):
    """Legacy wrapper to keep older scripts functional."""
    return forecast_to_dfs(search_terms, **kwargs)

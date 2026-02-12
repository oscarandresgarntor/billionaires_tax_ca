"""
Forbes Real-Time Billionaires API client.

Uses the community RTB API (github.com/komed3/rtb-api) to fetch
current billionaire data. Falls back to baseline JSON if API is unavailable.
"""

import json
import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

from src.data.baseline_data import TOTAL_CA_BILLIONAIRES, TOTAL_COLLECTIVE_WEALTH_B

RTB_BASE_URL = "https://cdn.statically.io/gh/komed3/rtb-api/main/api"
BASELINE_PATH = Path(__file__).parent.parent.parent / "data" / "baseline" / "ca_billionaires_baseline.json"

# California-related location keywords
CA_LOCATIONS = [
    "California", "San Francisco", "Los Angeles", "San Jose", "Palo Alto",
    "Menlo Park", "Atherton", "Woodside", "Beverly Hills", "Malibu",
    "Santa Monica", "San Diego", "Sacramento", "Newport Beach", "Cupertino",
    "Mountain View", "Sunnyvale", "Santa Clara", "Oakland", "Hillsborough",
    "Portola Valley", "Ross", "Tiburon", "Saratoga", "Los Altos",
    "Rancho Santa Fe", "La Jolla", "Pacific Palisades", "Bel Air",
    "Holmby Hills", "Laguna Beach", "Corona del Mar",
]


@st.cache_data(ttl=86400)
def fetch_forbes_index():
    """Fetch the Forbes RTB profile index."""
    try:
        resp = requests.get(f"{RTB_BASE_URL}/forbes/profiles/index.json", timeout=15)
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, json.JSONDecodeError):
        return None


@st.cache_data(ttl=86400)
def fetch_profile_info(uri: str):
    """Fetch detailed info for a single billionaire profile."""
    try:
        resp = requests.get(f"{RTB_BASE_URL}/forbes/profiles/{uri}/info.json", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, json.JSONDecodeError):
        return None


def _is_california_resident(profile_info: dict) -> bool:
    """Check if a profile appears to be a California resident."""
    location_fields = [
        profile_info.get("residence", ""),
        profile_info.get("city", ""),
        profile_info.get("state", ""),
        profile_info.get("country", ""),
    ]
    location_str = " ".join(str(f) for f in location_fields if f).lower()
    return any(loc.lower() in location_str for loc in CA_LOCATIONS)


def load_baseline_data() -> pd.DataFrame:
    """Load the curated baseline dataset from JSON."""
    if BASELINE_PATH.exists():
        with open(BASELINE_PATH) as f:
            data = json.load(f)
        if data.get("billionaires"):
            return pd.DataFrame(data["billionaires"])
    return _generate_synthetic_baseline()


def _generate_synthetic_baseline() -> pd.DataFrame:
    """Generate a synthetic baseline dataset matching Berkeley report statistics."""
    import numpy as np

    np.random.seed(42)

    industries = {
        "Technology": 82,
        "Finance & Investments": 38,
        "Real Estate": 18,
        "Healthcare": 14,
        "Retail & Consumer": 12,
        "Media & Entertainment": 10,
        "Energy": 8,
        "Manufacturing": 7,
        "Other": 15,
    }

    records = []
    idx = 0
    for industry, count in industries.items():
        for _ in range(count):
            # Generate wealth using a Pareto-like distribution
            # Most billionaires cluster near $1-5B, few are ultra-wealthy
            base = np.random.pareto(1.2) + 1.0
            wealth = min(base * 2.5, 250)  # Cap at $250B

            publicly_traded_pct = np.clip(
                np.random.normal(0.60, 0.15), 0.1, 0.95
            )
            real_estate_pct = np.clip(
                np.random.normal(0.10, 0.05), 0.02, 0.30
            )

            records.append({
                "id": idx,
                "name": f"Billionaire_{idx}",
                "net_worth_b": round(wealth, 2),
                "industry": industry,
                "publicly_traded_pct": round(publicly_traded_pct, 2),
                "estimated_re_pct": round(real_estate_pct, 2),
                "state": "California",
            })
            idx += 1

    df = pd.DataFrame(records)

    # Scale wealth to match Berkeley report total
    current_total = df["net_worth_b"].sum()
    scale_factor = TOTAL_COLLECTIVE_WEALTH_B / current_total
    df["net_worth_b"] = (df["net_worth_b"] * scale_factor).round(2)

    return df.sort_values("net_worth_b", ascending=False).reset_index(drop=True)


@st.cache_data(ttl=86400)
def get_billionaire_data(use_api: bool = False) -> pd.DataFrame:
    """
    Get California billionaire data.

    Args:
        use_api: If True, attempt to fetch from Forbes RTB API first.

    Returns:
        DataFrame with columns: name, net_worth_b, industry,
        publicly_traded_pct, estimated_re_pct, state
    """
    if use_api:
        index = fetch_forbes_index()
        if index is not None:
            ca_profiles = []
            # Sample a subset to avoid rate limiting
            uris = list(index.keys())[:500]
            for uri in uris:
                info = fetch_profile_info(uri)
                if info and _is_california_resident(info):
                    net_worth = info.get("finalWorth", 0)
                    if net_worth and net_worth >= 1000:  # Worth >= $1B (in millions)
                        ca_profiles.append({
                            "name": info.get("personName", uri),
                            "net_worth_b": round(net_worth / 1000, 2),
                            "industry": info.get("industries", ["Other"])[0] if info.get("industries") else "Other",
                            "publicly_traded_pct": 0.60,
                            "estimated_re_pct": 0.10,
                            "state": "California",
                        })
            if len(ca_profiles) >= 50:  # Only use if we got a meaningful number
                return pd.DataFrame(ca_profiles).sort_values(
                    "net_worth_b", ascending=False
                ).reset_index(drop=True)

    return load_baseline_data()


def get_summary_stats(df: pd.DataFrame) -> dict:
    """Compute summary statistics from billionaire DataFrame."""
    return {
        "count": len(df),
        "total_wealth_b": round(df["net_worth_b"].sum(), 1),
        "median_wealth_b": round(df["net_worth_b"].median(), 2),
        "mean_wealth_b": round(df["net_worth_b"].mean(), 2),
        "max_wealth_b": round(df["net_worth_b"].max(), 2),
        "min_wealth_b": round(df["net_worth_b"].min(), 2),
    }

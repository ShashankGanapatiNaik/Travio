"""
Arivo — Dynamic Parking Pricing Model (PoC)
Suggests a price per hour based on demand signals.
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np


def generate_mock_training_data(n: int = 500) -> pd.DataFrame:
    """Generates synthetic training data for the PoC."""
    np.random.seed(42)
    df = pd.DataFrame({
        "hour_of_day":         np.random.randint(6, 23, n),
        "day_of_week":         np.random.randint(0, 7, n),   # 0=Mon, 6=Sun
        "event_distance_km":   np.random.exponential(3, n),  # km to nearest event
        "weather_rain":        np.random.randint(0, 2, n),   # 0/1
        "area_demand_score":   np.random.uniform(0, 1, n),   # 0–1
        "host_fill_rate":      np.random.uniform(0.3, 1, n), # historical fill rate
        # Target: price multiplier above the floor (1.0 = floor price)
        "price_multiplier":    None
    })
    # Synthetic label: higher demand on weekends, evenings, near events
    df["price_multiplier"] = (
        1.0
        + 0.3 * (df["day_of_week"] >= 5)          # weekend boost
        + 0.2 * (df["hour_of_day"].between(17, 21)) # evening boost
        + 0.4 * (df["event_distance_km"] < 1)      # event boost
        + 0.1 * df["area_demand_score"]
        + np.random.normal(0, 0.05, n)             # noise
    ).clip(1.0, 3.0)
    return df


def train_pricing_model():
    """Trains a Random Forest pricing model on mock data."""
    df = generate_mock_training_data()
    features = ["hour_of_day", "day_of_week", "event_distance_km",
                "weather_rain", "area_demand_score", "host_fill_rate"]
    X = df[features]
    y = df["price_multiplier"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"Pricing model R² score: {score:.3f}")
    return model


def suggest_price(model, floor_price: float, hour: int, day: int,
                  event_km: float, rain: int, demand: float, fill_rate: float) -> float:
    """Returns the AI-suggested price per hour above the host's floor."""
    features = pd.DataFrame([{
        "hour_of_day": hour, "day_of_week": day,
        "event_distance_km": event_km, "weather_rain": rain,
        "area_demand_score": demand, "host_fill_rate": fill_rate
    }])
    multiplier = model.predict(features)[0]
    return round(floor_price * multiplier, -1)   # round to nearest ₹10


if __name__ == "__main__":
    model = train_pricing_model()

    # Example: Sunday evening, event 0.5km away, high demand
    price = suggest_price(
        model=model,
        floor_price=30,     # host set ₹30/hr floor
        hour=19,            # 7pm
        day=6,              # Sunday
        event_km=0.5,       # IPL match nearby
        rain=0,
        demand=0.8,
        fill_rate=0.7
    )
    print(f"\nSuggested price: ₹{price}/hr (floor was ₹30/hr)")

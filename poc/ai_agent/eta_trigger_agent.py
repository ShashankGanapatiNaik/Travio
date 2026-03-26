"""
Arivo — ETA Trigger Agent
Polls live GPS every 30 seconds, recalculates ETA,
and fires the food order at the optimal moment.

Usage:
    python eta_trigger_agent.py --trip_id trip_001 --order_id ord_001
"""

import time
import httpx
import argparse
from datetime import datetime

BACKEND_URL = "http://localhost:8000"
MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"   # replace with env var
POLL_INTERVAL_SECONDS = 30
BUFFER_MINUTES = 2


def get_live_eta(origin_lat: float, origin_lng: float,
                 dest_lat: float, dest_lng: float) -> int:
    """
    Fetches live ETA in minutes from Google Maps Directions API.
    Falls back to mock value for PoC demo.
    """
    # PoC: return a simulated decreasing ETA
    # Production: call Google Maps Directions API with departure_time=now
    mock_eta = getattr(get_live_eta, "_mock_eta", 35)
    get_live_eta._mock_eta = max(0, mock_eta - 0.5)   # decrements each call
    return int(get_live_eta._mock_eta)


def get_restaurant_prep_time(restaurant_id: str) -> int:
    """Returns the restaurant's average prep time in minutes."""
    # Production: query DB or restaurant service
    prep_times = {
        "rest_001": 18,   # Meghana Foods
        "rest_002": 12,
    }
    return prep_times.get(restaurant_id, 15)


def place_order(order_id: str) -> dict:
    """Calls the backend to trigger the food order."""
    response = httpx.post(f"{BACKEND_URL}/food-orders/{order_id}/trigger")
    return response.json()


def run_agent(trip_id: str, order_id: str, restaurant_id: str,
              origin_lat: float, origin_lng: float,
              dest_lat: float, dest_lng: float):
    """
    Main agent loop. Runs until order is placed or trip is cancelled.
    """
    prep_time = get_restaurant_prep_time(restaurant_id)
    order_placed = False

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Agent started for trip {trip_id}")
    print(f"  Restaurant prep time: {prep_time} min | Buffer: {BUFFER_MINUTES} min")
    print(f"  Order will fire when ETA ≤ {prep_time + BUFFER_MINUTES} min\n")

    while not order_placed:
        eta = get_live_eta(origin_lat, origin_lng, dest_lat, dest_lng)
        trigger_delta = eta - prep_time - BUFFER_MINUTES

        print(f"[{datetime.now().strftime('%H:%M:%S')}] ETA: {eta} min | "
              f"Trigger delta: {trigger_delta} min")

        if trigger_delta <= 0:
            print(f"\n>>> TRIGGER CONDITION MET — placing order {order_id}")
            result = place_order(order_id)
            print(f">>> Order placed: {result}")
            order_placed = True
        elif eta == 0:
            print(">>> User has arrived — trip complete")
            break
        else:
            time.sleep(POLL_INTERVAL_SECONDS)

    print(f"\nAgent completed for trip {trip_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arivo ETA Trigger Agent")
    parser.add_argument("--trip_id",       default="trip_001")
    parser.add_argument("--order_id",      default="ord_001")
    parser.add_argument("--restaurant_id", default="rest_001")
    parser.add_argument("--origin_lat",    type=float, default=12.9716)
    parser.add_argument("--origin_lng",    type=float, default=77.5946)
    parser.add_argument("--dest_lat",      type=float, default=12.9507)
    parser.add_argument("--dest_lng",      type=float, default=77.5848)
    args = parser.parse_args()

    run_agent(
        trip_id=args.trip_id,
        order_id=args.order_id,
        restaurant_id=args.restaurant_id,
        origin_lat=args.origin_lat,
        origin_lng=args.origin_lng,
        dest_lat=args.dest_lat,
        dest_lng=args.dest_lng,
    )

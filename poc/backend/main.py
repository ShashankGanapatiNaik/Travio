"""
Arivo — FastAPI Backend (PoC skeleton)
Run: uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Arivo API", version="0.1.0")


# ── Models ──────────────────────────────────────────────────────────────────

class ParkingSpot(BaseModel):
    host_id: str
    latitude: float
    longitude: float
    address: str
    price_floor: float          # ₹ per hour
    available_from: str         # "08:00"
    available_to: str           # "20:00"
    photos: list[str] = []

class BookingRequest(BaseModel):
    spot_id: str
    traveller_id: str
    start_time: str
    end_time: str

class FoodOrderRequest(BaseModel):
    trip_id: str
    restaurant_id: str
    items: list[dict]           # [{"name": "Biryani", "qty": 1, "price": 180}]

class TripRequest(BaseModel):
    user_id: str
    origin_lat: float
    origin_lng: float
    destination_lat: float
    destination_lng: float
    destination_address: str


# ── Health ───────────────────────────────────────────────────────────────────

@app.get("/")
def health():
    return {"status": "ok", "app": "Arivo", "version": "0.1.0"}


# ── Parking Spots ────────────────────────────────────────────────────────────

@app.get("/spots/nearby")
def get_nearby_spots(lat: float, lng: float, radius_m: int = 500):
    """
    Returns parking spots within radius_m metres of (lat, lng).
    PoC: returns mock data. Production: PostGIS ST_DWithin query.
    """
    # TODO: replace with real PostGIS query
    mock_spots = [
        {
            "spot_id": "spot_001",
            "host_name": "Ravi Kumar",
            "latitude": lat + 0.002,
            "longitude": lng + 0.001,
            "distance_m": 180,
            "price_per_hour": 35,
            "ai_suggested_price": 42,      # dynamic pricing model output
            "reliability_score": 87,
            "address": "12th Cross, Koramangala, Bengaluru",
            "photos": ["https://placeholder.com/spot1.jpg"],
        },
        {
            "spot_id": "spot_002",
            "host_name": "Meena S.",
            "latitude": lat - 0.001,
            "longitude": lng + 0.003,
            "distance_m": 320,
            "price_per_hour": 25,
            "ai_suggested_price": 25,
            "reliability_score": 92,
            "address": "8th Main, Koramangala, Bengaluru",
            "photos": ["https://placeholder.com/spot2.jpg"],
        },
    ]
    return {"spots": mock_spots, "count": len(mock_spots)}


@app.post("/spots")
def list_spot(spot: ParkingSpot):
    """Host lists a new parking spot."""
    # TODO: save to PostgreSQL with PostGIS POINT geometry
    return {"spot_id": "spot_new_001", "status": "listed", "message": "Spot listed successfully"}


@app.post("/bookings")
def create_booking(req: BookingRequest):
    """Traveller books a spot — initiates Razorpay payment hold."""
    # TODO: create Razorpay order, hold payment, save booking to DB
    return {
        "booking_id": "bk_001",
        "spot_id": req.spot_id,
        "status": "confirmed",
        "payment_hold_id": "pay_mock_001",
        "message": "Booking confirmed. Payment held."
    }


@app.post("/bookings/{booking_id}/checkin")
def checkin(booking_id: str, photo_url: str, lat: float, lng: float):
    """Traveller checks in with a geotagged photo."""
    return {"booking_id": booking_id, "status": "active", "checkin_photo": photo_url}


@app.post("/bookings/{booking_id}/checkout")
def checkout(booking_id: str):
    """Traveller checks out — releases payment to host."""
    # TODO: calculate duration, release Razorpay hold, trigger rating prompt
    return {"booking_id": booking_id, "status": "completed", "amount_charged": 70}


# ── Restaurants ──────────────────────────────────────────────────────────────

@app.get("/restaurants/enroute")
def get_enroute_restaurants(origin_lat: float, origin_lng: float,
                            dest_lat: float, dest_lng: float,
                            cuisine: Optional[str] = None):
    """Returns restaurants along the route."""
    # TODO: real route + PostGIS corridor query
    mock_restaurants = [
        {
            "restaurant_id": "rest_001",
            "name": "Meghana Foods",
            "cuisine": "South Indian",
            "avg_prep_time_min": 18,
            "distance_from_route_m": 50,
            "rating": 4.5,
            "price_for_two": 200,
            "whatsapp_number": "+91XXXXXXXXXX",
            "menu": [
                {"item_id": "m1", "name": "Chicken Biryani", "price": 180},
                {"item_id": "m2", "name": "Raita", "price": 30},
            ]
        }
    ]
    return {"restaurants": mock_restaurants}


# ── Food Orders ──────────────────────────────────────────────────────────────

@app.post("/food-orders/stage")
def stage_food_order(req: FoodOrderRequest):
    """Stage a food order — does NOT place it yet. Agent will trigger it."""
    return {
        "order_id": "ord_001",
        "status": "staged",
        "message": "Order staged. Agent will place it at the right moment."
    }


@app.post("/food-orders/{order_id}/trigger")
def trigger_food_order(order_id: str):
    """
    Called by the ETA trigger agent when the optimal moment arrives.
    Sends WhatsApp order to the restaurant via Twilio.
    """
    # TODO: Twilio WhatsApp send
    return {
        "order_id": order_id,
        "status": "placed",
        "message": "Order sent to restaurant via WhatsApp",
        "estimated_ready_at": "19:45"
    }


# ── Trips ────────────────────────────────────────────────────────────────────

@app.post("/trips")
def create_trip(req: TripRequest):
    """Creates a trip context — the parent object that links parking + food."""
    return {
        "trip_id": "trip_001",
        "status": "created",
        "destination": req.destination_address
    }


@app.get("/trips/{trip_id}/dashboard")
def get_trip_dashboard(trip_id: str):
    """Returns unified trip status: parking + food + ETA."""
    return {
        "trip_id": trip_id,
        "parking": {"status": "confirmed", "address": "12th Cross, Koramangala", "spot_id": "spot_001"},
        "food_order": {"status": "staged", "restaurant": "Meghana Foods", "trigger_in_minutes": 14},
        "navigation": {"current_eta_minutes": 32, "destination": "Lalbagh Botanical Garden"},
        "total_estimated_cost": 105
    }

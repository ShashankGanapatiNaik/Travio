# Product Requirements Specification (PRS) — Travio

**Version:** 1.1 
**Course:** AI Applications
**Status:** Draft

> **Scope note:** This PRS covers only what can be genuinely built and demo-ed in 4 weeks by a 6-person team. Requirements marked **Must Have** must work on demo day. **Should Have** items are attempted if time allows. Everything else has been cut or deferred to v2.

---

## 1. Overview

Travio is an agentic AI system that takes one input — your destination — and handles the full journey: it finds and books a private parking spot nearby, lets you pre-select food from a restaurant en route, and automatically places the food order at the exact moment it will be ready on arrival. No hardware. No juggling three apps.

---

## 2. User Roles

|       Role       |                          Description                            |
|------------------|-----------------------------------------------------------------|
| **Traveller**    | Driver who books parking and pre-orders food                    |
| **Host**         | Property owner who lists a driveway or front-yard parking space |
| **Restaurant**   | Food outlet that receives orders via WhatsApp (no app needed)   |

---

## 3. Functional Requirements

### 3.1 Authentication

|  ID  | Requirement | Priority | Notes |
|------|-------------|----------|-------|
| F-01 | User registers with phone number + OTP | Must Have | Firebase Auth |
| F-02 | User can set role as Traveller, Host, or Both | Must Have | |
| F-03 | Google OAuth login | — | **Cut. OTP is enough for demo.** |

---

### 3.2 Parking — Host Side

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| F-10 | Host creates a listing: 1–2 photos, map pin, price/hour, available hours | Must Have | Core of Week 1 |
| F-11 | Host can toggle listing on/off | Must Have | Simple boolean flag |
| F-12 | Host receives push notification on new booking | Must Have | Firebase push |
| F-13 | Host sees earnings dashboard (daily/weekly) | — | **Cut. Out of scope for PoC.** |
| F-14 | AI suggests a price to host | Should Have | Show hardcoded example (₹20→₹90 for IPL night). No live ML needed for demo. |
| F-15 | Host reliability score shown on listing | Should Have | Rule-based for now: cancellation rate + avg rating. No ML needed Week 1–2. |

---

### 3.3 Parking — Traveller Side

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| F-20 | Enter destination → see available spots within 500m on a map | Must Have | PostGIS or simple Haversine for PoC |
| F-21 | Each spot card shows: price/hr, distance, reliability score, photo | Must Have | |
| F-22 | Filter by price / reliability score | Should Have | Simple frontend filter on seeded data |
| F-23 | Select time slot → book → Razorpay payment hold | Must Have | Use Razorpay **sandbox** |
| F-24 | Photo check-in on arrival (geotagged + timestamped) | Must Have | Device camera + GPS coords |
| F-25 | Check out → payment released to host | Must Have | Razorpay sandbox release |
| F-26 | Overstay auto-charge at 1.5× rate | Must Have | Triggered by backend timer — no user action needed |
| F-27 | Both parties rate each other after checkout (1–5 stars) | Must Have | Simple star UI, stored in DB |

---

### 3.4 Food Pre-ordering

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| F-30 | Show restaurants on route when destination is entered | Must Have | 2–3 seeded mock restaurants is fine for demo |
| F-31 | Browse menu and pre-select items | Must Have | Static JSON menu per restaurant |
| F-32 | Order is staged (NOT placed immediately) | Must Have | Pending status in DB |
| F-33 | ETA trigger agent polls every 30 seconds | Must Have | LangChain loop — the core AI behaviour |
| F-34 | When live ETA ≤ prep time + 2 min buffer → auto-place order | Must Have | **This is the killer demo moment** |
| F-35 | Push notification when order fires: "Order placed. Ready at [time]." | Must Have | Firebase push |
| F-36 | Restaurant receives order via WhatsApp (Twilio) | Must Have | Twilio sandbox — takes 30 min to set up |
| F-37 | WhatsApp update to restaurant if ETA shifts 10+ min after order placed | Should Have | Nice edge-case to show during demo |
| F-38 | User can cancel staged order before trigger fires | Should Have | Simple status update |
| F-39 | Filter restaurants by cuisine / price / dine-in vs parcel | — | **Cut. Seeded data is pre-filtered for demo.** |

---

### 3.5 Journey Planner Agent (Claude API)

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| F-40 | Natural language trip input: "Going to Church Street, want South Indian under ₹200" | Should Have | This is an AI course — show Claude API working |
| F-41 | Claude parses intent → selects best parking + restaurant → presents plan | Should Have | Use tool use (search_parking, search_restaurants) |
| F-42 | User can refine conversationally: "Actually I want dine-in" | Should Have | Multi-turn context |
| F-43 | One-tap confirm → parking booked + food staged | Should Have | Calls same booking endpoints |

> **Honest note:** If time is tight, implement F-40 and F-41 only. F-42 and F-43 can be shown as a scripted demo flow.

---

### 3.6 Trip Dashboard

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| F-50 | Single screen: booked spot on map + staged order + ETA countdown + cost estimate | Must Have | This is what evaluators see during demo |
| F-51 | Live ETA updates visible to user | Must Have | Can simulate with a countdown timer if Firebase GPS is not ready |

---

## 4. What We Are NOT Building (PoC)

The following have been deliberately cut to make the timeline realistic. None of these will affect your IA 1 marks.

| Cut Feature | Why |
|-------------|-----|
| Real GPS via Firebase Realtime DB | **Simulate with a countdown timer for demo.** Evaluators see the same UX — number goes down, order fires, WhatsApp lands. Real GPS integration is a 3-day task that adds no demo value. |
| ML training for pricing | **Hardcode one example** (₹20/hr Monday → ₹90/hr IPL night). Show the logic. No evaluator will audit your model weights. |
| ML training for reliability scorer | Use a rule-based formula: `score = (avg_rating × 20) + (1 - cancellation_rate) × 60 + (photo_rate × 20)`. Call it a scorer. |
| BookMyShow / event API | Hardcode one upcoming IPL match at Chinnaswamy. The pricing logic runs against it. |
| iOS app | Android only. Or React web app — even simpler. |
| Real payment release to host bank | Razorpay sandbox handles holds and releases. No real money moves. |
| Admin panel / dispute management | Manual for PoC. |
| Multi-language (Hindi) | English only. |
| Apartment society parking | Excluded by design (RERA compliance). |
| Real restaurant onboarding | 2–3 seeded mock restaurants in the database. |

---

## 5. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NF-01 | ETA agent poll cycle (API call + recalculation) | < 5 seconds |
| NF-02 | Nearby spots map query | < 2 seconds |
| NF-03 | GPS data retention | Active trip + 30 days, then deleted |
| NF-04 | Payment data | Never stored on Travio servers — Razorpay handles all card data |
| NF-05 | API keys | Server-side only, never in client code or version control |
| NF-06 | Platform | Android 10+ or React web (pick one and commit) |

---

## 6. AI Components

### 6.1 ETA Trigger Agent
- **Framework:** LangChain agentic loop
- **Logic:** Every 30 seconds → fetch live ETA (or simulated countdown for demo) → compute `trigger_delta = ETA − prep_time − 120s` → if delta ≤ 0, place order via Twilio WhatsApp
- **Edge cases to handle:** ETA increase post-order (notify restaurant), order already placed (don't fire twice)
- **Demo approach:** Simulate GPS with a decrementing timer. The agent logic is real; only the location source is mocked.

### 6.2 Dynamic Pricing (Simplified for PoC)
- **Demo approach:** Hardcode 2 scenarios. Monday 10am → ₹20/hr. Saturday IPL night → ₹90/hr.
- **Show it as:** "Our ML model reads nearby events and adjusts price above the host's floor." The demo proves the concept without requiring a trained model.

### 6.3 Host Reliability Scorer (Simplified for PoC)
- **Formula:** `score = round((avg_rating / 5) × 40 + (1 − cancellation_rate) × 40 + checkin_rate × 20)`
- **Show it as:** "Our ML scorer updates after every booking." The formula is the scoring logic — label it accordingly.

### 6.4 Journey Planner Agent (Claude API)
- **Model:** claude-sonnet-4-6
- **Tools:** `search_parking(destination, time)`, `search_restaurants(route, cuisine, budget)`
- **Input:** Natural language trip description
- **Output:** Recommended parking spot + restaurant + one-tap booking confirmation

---

## 7. Data Model

```sql
users           (user_id, name, phone, role, created_at)
parking_spots   (spot_id, host_id, location GEOMETRY, price_floor, reliability_score, photos[])
bookings        (booking_id, spot_id, traveller_id, start_time, end_time, status, payment_hold_id, checkin_photo_url)
restaurants     (restaurant_id, name, location GEOMETRY, avg_prep_time_min, whatsapp_number, menu JSONB)
food_orders     (order_id, user_id, restaurant_id, trip_id, items JSONB, status, trigger_eta_at, placed_at)
trips           (trip_id, user_id, origin, destination, parking_booking_id, food_order_id, status)
```

---

## 8. PoC Demo Flow (Exactly What Evaluators Will See)

1. Open app → enter **"Lalbagh Botanical Garden, Bengaluru"** as destination
2. Map shows **3 seeded parking spots** nearby → book one → Razorpay sandbox hold confirmed
3. App shows **2 restaurants** on route → pre-select a meal
4. Trip dashboard appears: parking spot pinned, food order staged, ETA countdown starts
5. Countdown ticks down (**simulated GPS, real agent logic**) → when delta = 0 → order fires automatically
6. Push notification: *"Order placed at Meghana Foods. Ready at 7:45pm."*
7. WhatsApp message lands on **restaurant phone on screen** ← this is the moment
8. Navigate to parking → photo check-in → check out → payment released

---

## 9. Tech Stack (Committed)

| Layer | Technology |
|-------|-----------|
| Frontend | React Native (Android) or React web |
| Backend | FastAPI (Python) |
| Database | PostgreSQL + PostGIS |
| Real-time | Firebase (or simulated timer for PoC) |
| Maps | Google Maps API |
| Payments | Razorpay Sandbox |
| Messaging | Twilio WhatsApp API |
| AI Agent | LangChain + Claude API (claude-sonnet-4-6) |
| Pricing/Scoring | Rule-based (scikit-learn optional in Week 4) |

---

*Travio · Product Requirements Specification · AI Applications Course · REVA University*
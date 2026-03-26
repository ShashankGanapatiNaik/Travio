# Travio — Smart Journey Companion

> **AI-Powered Travel, Parking & Food — One Agent**

Travio is an agentic AI system that manages your entire road trip from a single destination input. It books a private parking spot near your destination, pre-orders food from a restaurant en route, and auto-fires the food order at the exact right moment based on your live GPS — so food is ready when you arrive. No juggling three apps. No cold food. No circling for parking.

---

## The Problem

Google Maps plans your route. Zomato finds food. Parkobot books parking. None of them talk to each other. Travio does.

|                           Stat                               |            Source               |
|--------------------------------------------------------------|---------------------------------|
| 23 min avg wasted searching for parking daily                | TERI Urban Mobility Report 2024 |
| 30% of Bengaluru traffic congestion caused by parking search | TERI 2024                       |
| 70% of QSR customers aged 18–54 use mobile order-ahead       | NRA 2025                        |
| $114B global smart parking market TAM (2025)                 | Industry Reports                |
| 4 AI modules in one agentic system                           | —                               |
| 0 IoT hardware needed — pure software                        | —                               |

---

## Solution Overview

Travio combines two core modules:

**Module A — P2P Parking Marketplace**
Homeowners list spare driveways and front yards. Travellers book by destination. Check-in via geotagged photo. Zero IoT hardware required.

**Module B — GPS-Timed Food Pre-ordering**
User pre-selects a meal en route. AI agent monitors live GPS ETA every 30 seconds. Order auto-fires at the optimal moment. Restaurant gets the order via WhatsApp — no POS integration needed.

---

## Repository Structure

```
travio/
├── README.md                          ← This file
├── .gitignore                         ← Protects API keys
├── documents/
│   ├── product_statement.md           ← Problem, ICP, personas, differentiation
│   ├── product_requirements_spec.md   ← F-01 to F-52 requirements, user stories, NFRs
│   ├── customer_interviews.md         ← Interview scripts, findings, synthesis
│   └── ia_presentation_pitch.md       ← 14-slide deck structure + evaluator Q&A prep
├── weekly_reports/
│   ├── week_01_2025-MM-DD.md          ← Week 1 report (update date)
│   └── week_template.md               ← Copy every Friday
└── src/
    └── README.md                      ← Code structure, setup, environment variables
```

---

## Technology Stack

|      Layer       |                         Technologies                      |
|------------------|-----------------------------------------------------------|
| Core APIs        | Google Maps API, Razorpay, Twilio WhatsApp API, Firebase  |
| AI / Agentic     | Claude API, scikit-learn, LangChain, Pandas               |
| Backend          | FastAPI (Python), PostgreSQL, PostGIS, Redis              |
| Frontend         | React Native, Google Maps JS SDK, Tailwind CSS, WebSocket |
| Dev Tools        | Razorpay Sandbox, Postman, pytest, Expo                   |

---


## Team

|         Name           |    SRN   |
|------------------------|----------|
| Ullas                  | R23EF288 |
| Srujan L               | R23EF263 |
| Thejas M G             | R23EF283 |
| Shreyas D              | R23EF252 |
| Shreyas B R            | R23EF251 |
| Shashank Ganapati Naik | R23EF245 |

---

## Environment Variables Required

```
GOOGLE_MAPS_API_KEY=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=
CLAUDE_API_KEY=
FIREBASE_PROJECT_ID=
DATABASE_URL=
REDIS_URL=
```

> **Never commit your `.env` file. It is listed in `.gitignore`.**

---

*Travio · AI Applications Course Project · REVA University*


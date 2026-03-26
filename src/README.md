# Travio — Source Code

This directory contains the Travio proof-of-concept codebase.

## Structure

```
src/
├── backend/          ← FastAPI backend (Python)
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── parking.py
│   │   ├── food.py
│   │   └── trips.py
│   ├── agents/
│   │   └── eta_trigger_agent.py   ← LangChain ETA agent
│   └── requirements.txt
│
├── frontend/         ← React Native / React web
│   ├── src/
│   │   ├── screens/
│   │   ├── components/
│   │   └── api/
│   └── package.json
│
├── ai_agents/        ← Standalone AI scripts
│   ├── pricing_model.py           ← Dynamic parking pricing
│   ├── eta_agent.py               ← GPS ETA trigger loop
│   └── journey_planner.py         ← Claude API agent
│
└── poc/              ← Quick proof-of-concept demos
    ├── demo_eta_trigger.py        ← Standalone ETA trigger demo
    └── demo_pricing.py            ← Pricing model demo
```

## Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env          # Fill in your API keys
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## Environment Variables (.env)

```
GOOGLE_MAPS_API_KEY=your_key_here
RAZORPAY_KEY_ID=your_key_here
RAZORPAY_KEY_SECRET=your_key_here
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
CLAUDE_API_KEY=your_key_here
FIREBASE_CONFIG=your_config_json_here
DATABASE_URL=postgresql://localhost:5432/Travio
```

## Running the PoC Demo

```bash
# ETA trigger demo (simulates a journey)
cd poc
python demo_eta_trigger.py

# Pricing model demo
python demo_pricing.py
```

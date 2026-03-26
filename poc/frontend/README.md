# Arivo Frontend — PoC

React Native app (Android).

## Setup

```bash
cd poc/frontend
npx create-expo-app arivo-app
cd arivo-app
npx expo install expo-location react-native-maps
npm install axios
npx expo start
```

## Screens to Build (Week 1–4)

1. **Home** — destination search input + "Start Trip" button
2. **Parking Map** — Google Maps with available spot markers + booking card
3. **Restaurant List** — en-route restaurants with cuisine filter
4. **Trip Dashboard** — unified view: parking status + food order countdown + ETA
5. **Host: List a Spot** — photo upload + location pin + price input
6. **Check-in Camera** — take photo + auto-geotag for proof of parking

## Key Libraries
- `expo-location` — GPS tracking
- `react-native-maps` — Google Maps integration
- `react-native-camera` — photo check-in
- `axios` — API calls to FastAPI backend

# Arivo AI Agent — PoC

## ETA Trigger Agent

Polls GPS every 30 seconds and fires the food order at the optimal moment.

```bash
cd poc/ai_agent
pip install langchain langchain-anthropic pandas scikit-learn httpx

# Run the agent (simulates a trip)
python eta_trigger_agent.py \
  --trip_id trip_001 \
  --order_id ord_001 \
  --restaurant_id rest_001
```

**What you'll see:**
```
[19:32:10] Agent started for trip trip_001
  Restaurant prep time: 18 min | Buffer: 2 min
  Order will fire when ETA ≤ 20 min

[19:32:10] ETA: 35 min | Trigger delta: 15 min
[19:32:40] ETA: 34 min | Trigger delta: 14 min
...
[19:37:40] ETA: 20 min | Trigger delta: 0 min

>>> TRIGGER CONDITION MET — placing order ord_001
>>> Order placed: {"status": "placed", "estimated_ready_at": "19:55"}
```

## Dynamic Pricing Model

```bash
python pricing_model.py
# Output: Suggested price: ₹90/hr (floor was ₹30/hr)
```

Test Commands
Normal flow
state = {
    "root_cause": {
        "issue": "Database timeout",
        "category": "technical",
        "severity": "HIGH",
        "root_cause": "Database connection timeout",
        "evidence": [
            "Connection timeout observed in payment logs."
        ]
    },
    "confidence": 91.8,
    "sources": [
        "payments_2026_06.csv"
    ]
}

state = recommendation_agent(state)

print(state["recommendation"])

2) Low-confidence flow

state = {
    "root_cause": {},
    "confidence": 45,
    "sources": []
}

state = recommendation_agent(state)

print(state["recommendation"])

3) Expected Output
High confidence
{
  "recommendations": [
    {
      "priority": "HIGH",
      "action": "Investigate and resolve database connection timeouts affecting payment processing.",
      "reason": "The retrieved evidence indicates database connection timeouts as the primary failure cause."
    }
  ],
  "confidence": 91.8,
  "sources": [
    "payments_2026_06.csv"
  ]
}
Low confidence

{
  "recommendations": [],
  "message": "No relevant information found in the indexed payment reports.",
  "confidence": 45,
  "sources": []
}

curl -X POST http://localhost:8000/ask \
-H "Content-Type: application/json" \
-d "{\"question\":\"Why did payment ABC123 fail?\"}"

uvicorn api.main:app --reload

curl http://localhost:8000/health


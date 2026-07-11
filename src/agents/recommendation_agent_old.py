from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2"
)
import json

def recommendation_agent(state):

    prompt = f"""
    You are a payment failure recommendation agent.

    Root cause:
    {state['root_cause']}

    Return ONLY valid JSON.

    Format:
    {{
        "recommendations": [
            {{
                "priority": "HIGH",
                "action": "action description",
                "reason": "why this helps"
            }}
        ]
    }}
    """

    response = llm.invoke(prompt)

    try:
        state["recommendation"] = json.loads(response.content)
    except Exception:
        state["recommendation"] = {
            "recommendations": [
                {
                    "priority": "UNKNOWN",
                    "action": response.content,
                    "reason": "LLM returned non JSON response"
                }
            ]
        }

    return state
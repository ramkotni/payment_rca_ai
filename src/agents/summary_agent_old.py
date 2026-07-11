from langchain_ollama import ChatOllama
import json


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def summary_agent(state):

    prompt = f"""
    You are a Payment Failure Incident Summary AI Agent.

    Create a final executive summary.

    Root Cause:
    {state['root_cause']}

    Recommendation:
    {state['recommendation']}


    Return ONLY valid JSON.

    Format:

    {{
        "incident_summary": "short summary",
        "impact": "business impact",
        "root_cause_summary": "main root cause",
        "recommended_actions": [
            "action 1",
            "action 2"
        ],
        "next_steps": [
            "step 1",
            "step 2"
        ],
        "priority": "HIGH/MEDIUM/LOW"
    }}

    """

    response = llm.invoke(prompt)


    try:
        state["answer"] = json.loads(response.content)

    except Exception:

        state["answer"] = {
            "incident_summary": response.content,
            "impact": "UNKNOWN",
            "root_cause_summary": "",
            "recommended_actions": [],
            "next_steps": [],
            "priority": "UNKNOWN"
        }


    return state
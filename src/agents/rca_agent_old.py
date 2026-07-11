from langchain_ollama import ChatOllama
import json

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def rca_agent(state):

    prompt = f"""
    You are a Payment Failure Root Cause Analysis AI Agent.

    Analyze the payment failure.

    Context:
    {state['context']}

    Question:
    {state['question']}

    Return ONLY valid JSON.

    Format:

    {{
        "issue": "main failure reason",
        "category": "technical/business/network",
        "severity": "HIGH/MEDIUM/LOW",
        "root_cause": "detailed explanation",
        "evidence": [
            "log or context evidence"
        ]
    }}

    """

    response = llm.invoke(prompt)


    try:
        state["root_cause"] = json.loads(response.content)

    except Exception:
        state["root_cause"] = {
            "issue": response.content,
            "category": "UNKNOWN",
            "severity": "UNKNOWN",
            "root_cause": response.content,
            "evidence": []
        }


    return state
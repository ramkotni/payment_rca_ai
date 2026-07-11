from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def intent_agent(state):

    question = state["question"]
    q = question.lower()

    # -----------------------------
    # Rule-based intent detection
    # -----------------------------

    if any(word in q for word in [
        "why", "root cause", "failed", "failure",
        "reason", "error", "timeout", "declined"
    ]):
        state["intent"] = "RCA"

    elif any(word in q for word in [
        "trend", "statistics", "report",
        "last month", "last quarter", "dashboard"
    ]):
        state["intent"] = "TREND"

    elif any(word in q for word in [
        "summary", "summarize",
        "overview", "executive summary"
    ]):
        state["intent"] = "SUMMARY"

    elif any(word in q for word in [
        "recommend", "recommendation",
        "solution", "fix",
        "prevent", "improve", "best practice"
    ]):
        state["intent"] = "RECOMMENDATION"

    elif any(word in q for word in [
        "hello", "hi", "hey",
        "good morning", "good evening"
    ]):
        state["intent"] = "GREETING"

    else:

        prompt = f"""
You are an Intent Classification Agent for a Payment Failure Analysis Platform.

Your domain is ONLY payment systems.

Supported domains include:
- payment failures
- payment processing
- payment gateway
- payment transactions
- transaction errors
- banking payments
- settlement
- reconciliation
- payment analytics

Return ONLY one of these values:

RCA
TREND
SUMMARY
RECOMMENDATION
GREETING
UNKNOWN

If the question is NOT related to payment systems,
return:

UNKNOWN

Question:
{question}

Return ONLY one word.
"""

        response = llm.invoke(prompt)

        intent = response.content.strip().upper()

        valid_intents = {
            "RCA",
            "TREND",
            "SUMMARY",
            "RECOMMENDATION",
            "GREETING",
            "UNKNOWN"
        }

        if intent not in valid_intents:
            intent = "UNKNOWN"

        state["intent"] = intent

    print("=" * 60)
    print(f"Intent Detected : {state['intent']}")
    print("=" * 60)

    return state
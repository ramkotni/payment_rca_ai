from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def trend_agent(state):

    context = state["context"]

    prompt = f"""
    You are a Payment Operations Analyst.

    Analyze the payment failure trend.

    Context:

    {context}

    Provide

    1. Top failures
    2. Monthly trend
    3. Critical failures
    4. Business impact
    """

    response = llm.invoke(prompt)

    state["answer"] = response.content

    return state
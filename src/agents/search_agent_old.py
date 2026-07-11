from rag.retriever_old import retriever

def search_agent(state):

    docs = retriever.invoke(
        state["question"]
    )

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    state["context"] = context

    return state
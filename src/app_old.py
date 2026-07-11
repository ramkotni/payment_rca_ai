from graph import graph

while True:

    question = input(
        "\nAsk Question: "
    )

    if question == "exit":
        break

    result = graph.invoke(
        {
            "question": question
        }
    )

    print("\nAnswer:\n")
    print(result["answer"])
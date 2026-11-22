from ai_researcher_2 import graph, config
from langchain_core.messages import HumanMessage

print("\n===================================")
print(" AI Researcher Agent Started ")
print("===================================")

print("\nType 'exit' to stop\n")

while True:

    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit"]:
        print("\nStopping AI Researcher...")
        break

    # ✅ FIX: use HumanMessage instead of dict
    input_data = {
        "messages": [
            HumanMessage(content=user_input)
        ]
    }

    try:

        stream = graph.stream(
            input_data,
            config=config,
            stream_mode="values"
        )

        for s in stream:

            message = s["messages"][-1]

            # ✅ SAFE HANDLING (object check)
            if hasattr(message, "content"):

                print("\n===================================\n")
                print(message.content)

            # fallback (just in case dict comes)
            elif isinstance(message, dict) and "content" in message:
                print("\n===================================\n")
                print(message["content"])

    except Exception as e:

        print("\n===================================")
        print(" ERROR ")
        print("===================================")
        print(str(e))
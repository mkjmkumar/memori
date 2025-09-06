import os
from openai import OpenAI
from dotenv import load_dotenv
from memori import Memori

load_dotenv()

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

print("Initializing Memori with OpenAI...")
nimbus_memory = Memori(
    database_connect="sqlite:///nimbus_demo.db",
    conscious_ingest=True,
    auto_ingest=True,
    verbose=True,
)

print("Enabling memory tracking...")
nimbus_memory.enable()

print("Memori OpenAI Example - Chat with GPT-4o while memory is being tracked")
print("Type 'exit' or press Ctrl+C to quit")
print("-" * 50)

while 1:
    try:
        user_input = input("User: ")
        if not user_input.strip():
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("Processing your message with memory tracking...")
        response = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct", messages=[{"role": "user", "content": user_input}]
        )
        print(f"AI: {response.choices[0].message.content}")
        print()  # Add blank line for readability
    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue

## works with : openai/gpt-oss-120b
import anthropic

from dotenv import load_dotenv
import os
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
print("Chatbot ready! Type 'quit' to exit.")

conversation = []

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    conversation.append({"role": "user", "content": user_input})
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=conversation
    )
    
    reply = response.content[0].text
    conversation.append({"role": "assistant", "content": reply})
    
    print(f"Claude: {reply}\n")

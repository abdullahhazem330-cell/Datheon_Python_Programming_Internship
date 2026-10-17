import json
import os
import re

def load_faqs(filename="faqs.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"[!] Warning: '{filename}' not found.")
        return []

def get_bot_response(user_input, faqs):
    cleaned_input = user_input.lower().strip()

    if cleaned_input in ["exit", "quit", "bye"]:
        return "bye"

    if cleaned_input == "help":
        return "Available topics: hours, location, services, contact, refund. Or type 'exit' to quit."

    for faq in faqs:
        for keyword in faq.get("keywords", []):
            if re.search(r'\b' + re.escape(keyword) + r'\b', cleaned_input):
                return faq["response"]

    return "I'm sorry, I didn't quite understand that. Type 'help' to see what topics I can answer!"
def main():
    faqs = load_faqs("faqs.json")

    print("=" * 60)
    print("🤖 Welcome to the Interactive Customer Support Assistant!")
    print("Type 'help' to view available topics, or 'exit' to quit.")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ")

        if not user_input.strip():
            continue

        response = get_bot_response(user_input, faqs)

        if response == "bye":
            print("\nBot: Thank you for contacting support! Have a great day! 👋")
            break

        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
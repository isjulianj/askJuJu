import os
from pyexpat.errors import messages

from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Could not get api key")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(
        prog="askJuJu",
        description="Your personal cli ai assistant, connected to gemini"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt",type=str, help="User prompt")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    content = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    if not content.usage_metadata:
        raise RuntimeError("failed to get a response")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
    print(f"Response:\n{content.text}")

if __name__ == "__main__":
    main()
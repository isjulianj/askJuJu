import os
from pyexpat.errors import messages

from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

from functions.call_function import available_functions, call_function
from prompts import system_prompt


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

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    generate_content(client, messages, args.verbose)

def generate_content(client, messages_list, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages_list,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)
        function_results = []
        if len(function_call_result.parts) > 0:
            if not isinstance(function_call_result.parts[0], genai.types.Part):
                raise Exception("This is not a function response type")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("No function response")
            function_results.append(function_call_result.parts[0])
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        print(f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()
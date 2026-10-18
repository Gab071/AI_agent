import os
import argparse, json, sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import call_function, available_functions



def main():

    try: 
        load_dotenv()
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if api_key is None:
            raise RuntimeError("api_key wasn't found")

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        parser = argparse.ArgumentParser(description="Chatbot")
        parser.add_argument("user_prompt", type=str, help="User prompt")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        args = parser.parse_args()
        # Now we can access `args.user_prompt`

        messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
        ]
        for _ in range(20):
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=available_functions,
            )
            message = response.choices[0].message
            messages.append(message)
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, verbose=args.verbose)
                    

                    if not result_message["content"]:
                        raise Exception("Not content in result_message")
                    if args.verbose:
                        print(f"-> {result_message['content']}")
                    
                    messages.append(result_message)
            else:
                if args.verbose:       
                    print(f"User prompt: {args.user_prompt}")
                    print(f"Prompt tokens: {response.usage.prompt_tokens}")
                    print(f"Response tokens: {response.usage.completion_tokens}")
                print(response.choices[0].message.content)
                break
        else:
            print("All 20 iterations were used and AI agent didn't give a response")
            sys.exit(1)

         

    except Exception as e:
        print(f"Error {e}")

if __name__ == "__main__":
    main()


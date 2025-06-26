import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

if len(sys.argv) < 2:
    print('Provide a prompt you idiot!')
    exit(1)

user_prompt = sys.argv[1]
messages = [types.Content(role='user', parts=[types.Part(text=user_prompt)])]
system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, contrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself"
            )
        }
    )
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file in a directory"
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=config)


for call in response.function_calls:
    print(f"Calling function: {call.name}({call.args})")
print(response.text)

if len(sys.argv) > 2:
    if '--verbose' in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
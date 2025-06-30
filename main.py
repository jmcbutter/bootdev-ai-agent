import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function

if len(sys.argv) < 2:
    print('Provide a prompt you idiot!')
    exit(1)

user_prompt = sys.argv[1]
messages = [types.Content(role='user', parts=[types.Part(text=user_prompt)])]
system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory",
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
    description="Gets the content of the specified file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file, relative to the working directory."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python subprocess in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the python file, relative to the working directory"
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=config)

for call in response.function_calls:
    result = call_function(call)
    call_response = result.parts[0].function_response.response

    if call_response is None:
        raise Exception('Error: No response')
    elif len(sys.argv) > 2 and '--verbose' in sys.argv:
        if '--verbose' in sys.argv:
            print(f"-> {call_response}")

print(response.text)
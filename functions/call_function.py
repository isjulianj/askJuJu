from google.genai import types

from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_to_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_to_file,
        schema_run_python_file
    ]
)

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file

}

def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    if function_name in function_map:
        if verbose:
            print(f"Calling function: {function_name}({args})")
            function_result = function_map[function_name](**args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )
        else:
            print(f"- Calling function: {function_name}")
            function_result = function_map[function_name](**args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                     name= function_name,
                     response= {"error": f"Unknown function: {function_name}"}
                   ),
            ]
        )
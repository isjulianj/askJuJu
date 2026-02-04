import os.path

from config import MAX_NUM_CHARACTERS
from google.genai import types

def get_file_content(working_directory, file_path):

    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_path = os.path.commonpath([target_path, abs_path]) == abs_path

        if not valid_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        content = ""
        with open(target_path) as f:
            content = f.read(MAX_NUM_CHARACTERS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_NUM_CHARACTERS} characters]'
        return content
    except Exception as err:
        return f"Error: {err}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="It will read the beginning of the file specified by the file path, up to the max characters set in the env variables.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that we'd like to read the contents of."
            )
       },
        required=["file_path"]
    )
)

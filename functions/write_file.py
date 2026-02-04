import os.path

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_path = os.path.commonpath([target_file, abs_path]) == abs_path
        print(target_file)
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'


        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as err:
        return f"Error: {err}"

schema_write_to_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the given content to the file specified by the file path",
    parameters=types.Schema(
        type= types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the specific file for the content to be written to"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content provided to be written to the specified file."
            )
        }
    )

)
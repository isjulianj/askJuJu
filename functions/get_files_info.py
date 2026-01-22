import os.path

from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        valid_working_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if not valid_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        output = []
        for item in os.listdir(path=target_dir):
            file_path = os.path.join(target_dir, item)
            if os.path.isfile(path=file_path):
                detail = create_output_string(item,os.path.getsize(file_path),False)
                output.append(detail)
            else:
                detail = create_output_string(item, os.path.getsize(file_path), True)
                output.append(detail)
        return "\n".join(output)
    except Exception as e:
        return f"Error listing files: {e}"

def create_output_string(name, size, is_dir):
    return f"- {name}: file_size={size}, is_dir={is_dir}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
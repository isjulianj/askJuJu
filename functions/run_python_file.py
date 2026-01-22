import os.path
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_file_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_file_path, file_path))
        valid_path = os.path.commonpath([target_file, abs_file_path]) == abs_file_path

        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'


        command = ["python3", target_file]
        if args:
            command.append(*args)

        ran_process = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=target_file)


        output = ""

        if ran_process.returncode != 0:
            output += f"Process exited with code {ran_process.returncode}\n"

        if ran_process.stdout and ran_process.stderr:
            output += "No output produced\n"

        output += f"STDOUT: {ran_process.stdout}\nSTDERR: {ran_process.stderr}\n"
        return output


    except Exception as err:
        return f"Error: {err}"
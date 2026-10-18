import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory) # absolute directory
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path)) # creating target directory
        # Will be True or False - checking if common path of target_dir and working_directory is the same
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        
        # Checking if it is a file and if it exists
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Adding arguments to command
        command = ["python", target_file]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, timeout=30, text=True)
        output_string = ""
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}\n"     
        if completed_process.stdout:
            output_string += f"STDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            output_string += f"STDERR: {completed_process.stderr}"

        return output_string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run Python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run a file, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "Arguments that will be added to a function subprocess.run() as a first argument",
                    "items": {
                        "type": "string"
                    },
                },
            },
            "required": ["file_path"],
        },
    },
}
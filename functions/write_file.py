import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
        try:
            working_dir_abs = os.path.abspath(working_directory) # absolute directory
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path)) # creating target directory
            # Will be True or False - checking if common path of target_dir and working_directory is the same
            valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
            if not valid_target_dir:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

            # If it is a directory (not a file) return error                
            if os.path.isdir(target_file):
                return f'Error: Cannot write to "{file_path}" as it is a directory'

            # Creating directories if they do not exist before our file
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            with open(target_file, "w") as f:
                f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'            

        except Exception as e:
            return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write or overwrite contents of a file in a specified file path relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write information to a file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content that will be written to a file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
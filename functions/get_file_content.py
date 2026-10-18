import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory) # absolute directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path)) # creating target directory
        # Will be True or False - checking if common path of target_dir and working_directory is the same
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # If we pass not a file as an argument it will raise an error that will be caught 
        # target_dir is used because we need to pass full path to the file for that fucntion 
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Opening with correct file path - target_dir 
        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
             # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
       
        return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets file content in a specified file path relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get file information from, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
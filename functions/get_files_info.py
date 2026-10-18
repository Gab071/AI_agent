import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory) # absolute directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory)) # creating target directory
        # Will be True or False - checking if common path of target_dir and working_directory is the same
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # If we pass a file as an argument (not directory) it will catch it
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        target_dir_items: list[str] = []
        for item in os.listdir(target_dir):
            item_path = f"{target_dir}/{item}"
            target_dir_items.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

        return "\n".join(target_dir_items)


    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
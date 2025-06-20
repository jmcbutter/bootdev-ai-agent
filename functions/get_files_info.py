import os

def get_files_info(working_directory, directory=None):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_dir_path = working_dir_path
        if directory:
            target_dir_path = os.path.abspath(os.path.join(working_directory, directory))

        if not target_dir_path.startswith(working_dir_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir_path):
            return f'Error: "{directory}" is not a directory'
        else:
            dir_listing = os.listdir(path=target_dir_path)
            lines = []
            for item in dir_listing:
                item_path = os.path.abspath(os.path.join(target_dir_path, item))
                item_size = os.path.getsize(item_path)
                item_is_dir = os.path.isdir(item_path)
                lines.append(f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}")
            return '\n'.join(lines)
    except Exception as e:
        return f"Error: {e}"

import os


def get_file_content(working_directory, file_path):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = working_dir_path
        if file_path:
            target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_file_path.startswith(working_dir_path):
            return f'Error: Cannot read "{file_path} as it is outside the permitted working directory'
        elif not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file_path, "r") as f:
                content = f.read(10000)
                if len(content) == 10000:
                    content = f'{content}[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f'Error: {e}'
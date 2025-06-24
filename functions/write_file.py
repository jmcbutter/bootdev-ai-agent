import os.path


def write_file(working_directory, file_path, content):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.abspath(os.path.join(working_dir_path, file_path))
        target_file_directory_path = os.path.dirname(target_file_path)

        if not target_file_path.startswith(working_dir_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(target_file_directory_path):
            os.makedirs(target_file_directory_path)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

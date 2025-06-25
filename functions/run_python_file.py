import os.path
import subprocess


def run_python_file(working_directory, file_path):
    working_dir_path = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_dir_path, file_path))

    if not target_file_path.startswith(working_dir_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(target_file_path):
        return f'Error: File "{file_path}" not found.'
    elif target_file_path[-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file'
    else:
        try:
            subp = subprocess.run(["python3", target_file_path], timeout=30, cwd=working_dir_path, capture_output=True)
            stdout = subp.stdout
            stderr = subp.stderr

            msg = ''
            if stdout is not None:
                msg += f'STDOUT: {stdout}\n'
            if stderr is not None:
                msg += f'STDERR: {stderr}\n'
            if subp.returncode != 0:
                msg += f'Process exited with code {subp.returncode}\n'
            if stdout is None and stderr is None:
                msg += f'No output produced'
            return msg
        except Exception as e:
            return f'Error: executing Python file: {e}'

import subprocess
import shutil
import os
import io
import logging
import select
import sys
import shlex

logger = logging.getLogger(__name__)

VERBOSE = True


def run_command(command, silent=False):
    if VERBOSE:
        print(f"Executing command: {command}")
    output = io.StringIO()
    args = shlex.split(command)
    try:
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )
        readable = {process.stdout, process.stderr}
        writable = {process.stdin}
        while readable or writable:
            r, w, x = select.select(readable, writable, [])

            for stream in r:
                if stream in (process.stdout, process.stderr):
                    line = stream.readline()
                    if not line:
                        readable.remove(stream)
                        continue
                    if not silent:
                        if stream == process.stderr:
                            print(line, end="", file=sys.stderr, flush=True)
                        else:
                            print(line, end="", flush=True)
                    output.write(line)

            if process.stdin in w:
                # Check if there's any input from the user
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    user_input = input()
                    process.stdin.write(user_input + "\n")
                    process.stdin.flush()
                else:
                    writable.remove(process.stdin)

        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command, output.getvalue())
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {command}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Output: {e.output}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error executing command: {command}")
        logger.error(f"Error: {str(e)}")
        raise
    return output.getvalue()


def copy_file(source, destination):
    if not os.path.exists(source):
        logger.error(f"Error: {source} not found")
        return False
    if os.path.exists(destination):
        logger.info(f"Skipping copying {destination} since it already exists")
        return False

    try:
        shutil.copy2(source, destination)
        logger.info(f"Copied {source} to {destination}")
        return True
    except Exception as e:
        logger.error(f"Error copying config file: {str(e)}")
        return False


def update_file(file_path, key, value):
    with open(file_path, "r") as f:
        lines = f.readlines()

    modified_lines = []
    for line in lines:
        if line.startswith(key):
            modified_lines.append(f"{key}={value}\n")
        else:
            modified_lines.append(line)

    with open(file_path, "w") as f:
        f.writelines(modified_lines)

    print(f"Updated file: {file_path} to set {key}={value}")

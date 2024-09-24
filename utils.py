import subprocess
import shutil
import os

VERBOSE = True


def run_command(command, silent=False):
    if VERBOSE:
        print(f"Executing command: {command}")
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        if not silent and (VERBOSE or result.stdout or result.stderr):
            # Print a more readable version of the CompletedProcess
            print("RESULT:")
            print(f"  Command: {command}")
            print(f"  Return code: {result.returncode}")
            print(f"  STDOUT: {result.stdout.strip() or '(empty)'}")
            print(f"  STDERR: {result.stderr.strip() or '(empty)'}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        if e.stderr:
            print(f"Error message: {e.stderr}")
        raise


class Utils:
    @staticmethod
    def copy_file(source, destination):
        if not os.path.exists(source):
            print(f"Error: {source} not found")
            return False
        if os.path.exists(destination):
            print(f"Skipping copying {destination} since it already exists")
            return False

        try:
            shutil.copy2(source, destination)
            print(f"Copied {source} to {destination}")
            return True
        except Exception as e:
            print(f"Error copying config file: {str(e)}")
            return False

    def update_file(self, file_path, key, value):
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

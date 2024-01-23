import subprocess

def run_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return None, e.stderr

# Example usage
command_to_run = "ls -l"
stdout, stderr = run_shell_command(command_to_run)

if stdout is not None:
    print(f"Command output:\n{stdout}")
else:
    print(f"Command failed with error:\n{stderr}")

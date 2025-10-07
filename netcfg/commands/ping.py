import subprocess
import platform


def stream_ping(host: str, count: int = 4):
    """Yield ping output line by line."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, str(count), host]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        yield line.rstrip()

    process.wait()
    if process.returncode != 0:
        yield f"Ping failed with exit code {process.returncode}"


def run_ping(host: str, count: int = 4) -> str:
    """Run ping and return the output as a string."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, str(count), host]

    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return completed.stdout
    except subprocess.CalledProcessError as e:
        return f"Ping failed with exit code {e.returncode}\n{e.stdout}\n{e.stderr}"


def main(args):
    """
    CLI entry point: ping a given host.
    """
    host = args.host
    count = args.count if args.count is not None else 4

    result = run_ping(host, count)
    print(result)
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

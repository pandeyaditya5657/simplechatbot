"""One-click launcher: creates a virtual environment, installs the
requirements (first run only) and starts the chatbot in your browser."""
import os
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
VENV = ROOT / ".venv"
PY = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
REQ = ROOT / "requirements.txt"
MARKER = VENV / ".deps_installed"


def main():
    os.chdir(ROOT)
    if sys.version_info < (3, 9):
        sys.exit("Python 3.9 or newer is required. Get it from https://www.python.org/downloads/")

    if not PY.exists():
        print("First run: creating virtual environment...")
        try:
            venv.create(VENV, with_pip=True)
        except Exception as e:
            sys.exit(f"Could not create a virtual environment: {e}\n"
                     "On Ubuntu/Debian run: sudo apt install python3-venv")

    if not MARKER.exists() or MARKER.stat().st_mtime < REQ.stat().st_mtime:
        print("Installing dependencies (one time, may take a minute)...")
        subprocess.check_call([str(PY), "-m", "pip", "install", "--disable-pip-version-check", "-q", "-r", str(REQ)])
        MARKER.touch()

    try:
        subprocess.call([str(PY), str(ROOT / "app.py")])
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        sys.exit("Installing dependencies failed. Check your internet connection and try again.")

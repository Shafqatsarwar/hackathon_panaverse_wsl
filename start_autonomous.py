import subprocess
import os
import sys
import time
from pathlib import Path

def start_process(name, cmd, cwd=None):
    print(f"[START] Launching {name}...")
    # Use start on windows to open new windows
    if os.name == 'nt':
        return subprocess.Popen(f"start \"{name}\" cmd /k {cmd}", shell=True, cwd=cwd)
    else:
        return subprocess.Popen(cmd.split(), cwd=cwd)

def main():
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)

    python_exe = sys.executable
    
    # Check for venv
    if os.name == 'nt':
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = project_root / ".venv" / "bin" / "python"

    if venv_python.exists():
        python_exe = str(venv_python)
        print(f"[INFO] Using virtual environment: {python_exe}")

    # 1. Cleanup (Node only to be safe, avoid killing self)
    print("Cleaning up old Node processes...")
    if os.name == 'nt':
        # subprocess.run("taskkill /F /IM python.exe /T 2>nul", shell=True) # DONT KILL SELF
        subprocess.run("taskkill /F /IM node.exe /T 2>nul", shell=True)
        time.sleep(1)

    # 2. Start Components
    start_process("Watchers", f"{python_exe} watchers.py")
    start_process("Brain Agent", f"{python_exe} agents/brain_agent.py")
    start_process("Backend API", f"{python_exe} src/api/chat_api.py")
    
    frontend_dir = project_root / "frontend"
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies...")
        subprocess.run("npm install", shell=True, cwd=frontend_dir)
    
    start_process("Frontend UI", "npm run dev", cwd=frontend_dir)

    print("\n[SUCCESS] Autonomous System Started!")
    print("Dashboard: http://localhost:3000/dashboard")
    print("Chat:      http://localhost:3000")
    print("\nKeep the new windows open. Press Ctrl+C in this terminal to exit (does not stop children).")

if __name__ == "__main__":
    try:
        main()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting orchestrator...")

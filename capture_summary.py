import subprocess
import os
import sys

def run_and_capture():
    project_root = "/home/shafqatsarwar/Projects/hackathon_panaverse"
    script_path = os.path.join(project_root, "scripts", "send_summary.py")
    
    print(f"Running {script_path}...")
    try:
        # Run with a 5 minute timeout
        result = subprocess.run(
            [sys.executable, "-u", script_path],
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=300,
            encoding='utf-8' # Force utf-8
        )
        
        with open("summary_execution.log", "w", encoding='utf-8') as f:
            f.write("STDOUT:\n")
            f.write(result.stdout)
            f.write("\nSTDERR:\n")
            f.write(result.stderr)
            
        print("Execution complete. Check summary_execution.log")
        print("STDOUT PREVIEW:")
        print(result.stdout[:500])
        
    except subprocess.TimeoutExpired:
        print("Execution timed out after 5 minutes.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_and_capture()

import os
import subprocess
import time

def kill_processes():
    print("Stopping all AI Employee processes...")
    if os.name == 'nt': # Windows
        # Kill Python processes (Watchers, Agents, API)
        subprocess.run("taskkill /F /IM python.exe /T 2>nul", shell=True)
        # Kill Node processes (Frontend)
        subprocess.run("taskkill /F /IM node.exe /T 2>nul", shell=True)
    else: # Unix/Mac
        subprocess.run("pkill -f python", shell=True)
        subprocess.run("pkill -f node", shell=True)
    
    time.sleep(1)
    print("[STOPPED] All systems shut down.")

if __name__ == "__main__":
    kill_processes()

"""
Panaversity Assistant - Management CLI
Run this script to manage and execute different parts of the system.
Usage: python manage.py
"""
import os
import sys
import subprocess
import time
from typing import List

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 60)
    print("   Panaversity Student Assistant - Management Console")
    print("=" * 60)
    print("")

def run_command(command: str, new_window: bool = False, title: str = ""):
    """Run a command in the current or new window"""
    print(f"[*] Starting: {title if title else command}")
    
    if new_window:
        if os.name == 'nt':
            # Windows
            subprocess.Popen(f'start "{title}" cmd /k "{command}"', shell=True)
        else:
            # Linux/Mac (Basic support)
            subprocess.Popen(f"x-terminal-emulator -e '{command}'", shell=True)
    else:
        # Run in current window
        os.system(command)

def menu_full_stack():
    print("Launching Full Stack Environment...")
    # Launch Backend
    run_command("python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000", new_window=True, title="Backend API")
    time.sleep(3)
    # Launch Frontend
    frontend_cmd = "cd frontend && npm run dev"
    run_command(frontend_cmd, new_window=True, title="Next.js Frontend")
    print("\n[+] Systems launched in new windows!")
    input("\nPress Enter to return to menu...")

def menu_backend():
    print("Launching Backend API...")
    run_command("python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000", new_window=False)
    input("\nPress Enter to return to menu...")

def menu_frontend():
    print("Launching Frontend...")
    os.chdir("frontend")
    run_command("npm run dev", new_window=False)
    os.chdir("..")
    input("\nPress Enter to return to menu...")

def menu_test_email():
    print("Running Email Check Test...")
    run_command("python -m src.main check", new_window=False)
    input("\nPress Enter to return to menu...")

def menu_debug_whatsapp():
    print("Running WhatsApp Debug Mode...")
    # We can create a small temporary script or run a specific module
    # For now, let's just run the main agent in foreground
    run_command("python -m src.main start", new_window=False)
    input("\nPress Enter to return to menu...")

def main_menu():
    while True:
        print_header()
        print("1. 🚀 Run Full Project (Backend + Frontend)")
        print("2. 🐍 Run Backend API Only (Port 8000)")
        print("3. ⚛️  Run Frontend Only (Port 3000)")
        print("4. 📧 Run Manual Email Check")
        print("5. 🧠 Run Main Agent (Background Tasks)")
        print("6. 📦 Install Dependencies (Setup)")
        print("q. 🚪 Quit")
        print("-" * 60)
        
        choice = input("Select an option: ").strip().lower()
        
        if choice == '1':
            menu_full_stack()
        elif choice == '2':
            menu_backend()
        elif choice == '3':
            menu_frontend()
        elif choice == '4':
            menu_test_email()
        elif choice == '5':
            menu_debug_whatsapp()
        elif choice == '6':
            print("Installing Python dependencies...")
            run_command("pip install -r requirements.txt", new_window=False)
            print("\nInstalling Frontend dependencies...")
            run_command("cd frontend && npm install", new_window=False)
            input("\nDone! Press Enter...")
        elif choice == 'q':
            print("Goodbye!")
            sys.exit(0)
        else:
            input("Invalid option. Press Enter...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

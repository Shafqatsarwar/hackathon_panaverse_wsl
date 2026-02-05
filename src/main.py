"""
Panaversity Student Assistant - Main Entry Point
"""
import sys
import argparse
import asyncio
import os
from agents.main_agent import MainAgent

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Panaversity Student Assistant - Email, WhatsApp, and LinkedIn monitoring'
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'check', 'status', 'config'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    agent = MainAgent()
    
    if args.command == 'start':
        # Start in background mode with scheduling
        agent.start()
    
    elif args.command == 'check':
        # Run a single manual check
        agent.run_manual_check()
    
    elif args.command == 'status':
        # Show status
        agent.status()
    
    elif args.command == 'config':
        # Show configuration
        from src.utils.config import Config
        Config.print_config()

if __name__ == '__main__':
    main()

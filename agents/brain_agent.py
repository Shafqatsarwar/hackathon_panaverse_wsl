"""
The Brain: Ralph Wiggum Persistence Loop
Processes tasks from /Needs_Action until they are in /Done.
"""
import time
import shutil
import logging
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Brain")

class BrainAgent:
    def __init__(self):
        self.vault_path = Path("data/vault")
        self.needs_action_path = self.vault_path / "Needs_Action"
        self.processing_path = self.vault_path / "In_Progress" # Optional
        self.done_path = self.vault_path / "Done"
        self.plans_path = self.vault_path / "Plans"
        
        # Ensure directories exist
        self.needs_action_path.mkdir(parents=True, exist_ok=True)
        self.done_path.mkdir(parents=True, exist_ok=True)
        self.plans_path.mkdir(parents=True, exist_ok=True)

    def run(self):
        logger.info("Starting Brain Agent (Ralph Wiggum Loop)...")
        while True:
            try:
                tasks = list(self.needs_action_path.glob("*.md"))
                for task_file in tasks:
                    self.process_task(task_file)
            except Exception as e:
                logger.error(f"Brain Loop Error: {e}")
            
            time.sleep(10) # Check frequently

    def process_task(self, task_file: Path):
        logger.info(f"Processing task: {task_file.name}")
        
        # 1. Read Task
        content = task_file.read_text(encoding="utf-8")
        
        # 2. Think (Simulated)
        # TODO: Call Gemini/Claude to generate a plan
        logger.info(f"Thinking about {task_file.name}...")
        
        # 3. Plan
        plan_file = self.plans_path / f"PLAN_{task_file.name}"
        plan_content = f"""---
original_task: {task_file.name}
status: active
created: {datetime.now().isoformat()}
---
# Plan
1. Analyze email content.
2. Draft reply (if needed).
3. Update Odoo (if lead).
"""
        plan_file.write_text(plan_content, encoding="utf-8")
        logger.info(f"Created Plan: {plan_file.name}")
        
        # 4. Act
        action_result = "Simulated Success"
        try:
            # Simple keyword based routing for now
            task_type = "unknown"
            if "EMAIL" in task_file.name:
                task_type = "email_processing"
                # Parse the .md content to get sender/body
                # This is a simplified example. In production, use frontmatter parser.
                pass 
            
            # Example: If the task implies a lead, create it in Odoo
            # For this hackathon, we assume 'Needs_Action' files are ready-to-process
            
            from agents.odoo_agent import OdooAgent
            odoo = OdooAgent()
            if odoo.enabled and "invoice" in content.lower():
                 odoo.create_lead_from_email({"subject": f"Task: {task_file.name}", "sender": "Brain", "body": content[:200]})
                 action_result = "Created Lead in Odoo"

        except Exception as e:
            logger.error(f"Action Failed: {e}")
            action_result = f"Failed: {e}"
        
        # 5. Move to Done
        dest = self.done_path / task_file.name
        
        # Add result result to file
        with open(task_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n# Execution Result\n{action_result}\nCompleted: {datetime.now().isoformat()}")
            
        shutil.move(str(task_file), str(dest))
        logger.info(f"Task Complete: Moved {task_file.name} to Done (Result: {action_result})")

if __name__ == "__main__":
    brain = BrainAgent()
    brain.run()

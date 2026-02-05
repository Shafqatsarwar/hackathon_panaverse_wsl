"""
Oracle Cloud Skill - Deploy and manage Panaverse AI on Oracle Cloud
"""
import subprocess
import os
import logging

logger = logging.getLogger(__name__)

class OracleCloudSkill:
    """
    Skill to deploy and manage the application on Oracle Cloud.
    Handles SSH commands, file uploads, and Docker operations.
    """
    
    def __init__(self):
        self.server_ip = "141.147.83.137"
        self.user = "ubuntu"
        self.key_path = os.path.join(os.path.dirname(__file__), "..", "..", "oracle_cloud", "oracle", "oracle_key.key")
        self.remote_path = "~/panaverse"
    
    def _run_ssh_command(self, command: str) -> tuple[bool, str]:
        """Run a command on the Oracle Cloud server via SSH"""
        ssh_cmd = f'ssh -i {self.key_path} -o StrictHostKeyChecking=no {self.user}@{self.server_ip} "{command}"'
        try:
            result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=300)
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out after 5 minutes"
        except Exception as e:
            return False, str(e)
    
    def check_container_status(self) -> dict:
        """Check if the Docker container is running"""
        success, output = self._run_ssh_command("sudo docker ps --format '{{.Names}} {{.Status}}'")
        return {
            "success": success,
            "output": output,
            "container_running": "panaversity_watcher" in output if success else False
        }
    
    def get_logs(self, lines: int = 50) -> dict:
        """Get recent logs from the container"""
        success, output = self._run_ssh_command(f"sudo docker logs --tail {lines} panaversity_watcher 2>&1")
        return {"success": success, "logs": output}
    
    def restart_watcher(self) -> dict:
        """Restart the watcher container"""
        command = f"cd {self.remote_path} && sudo rm -f whatsapp_session/whatsapp.lock && sudo docker-compose restart watcher"
        success, output = self._run_ssh_command(command)
        return {"success": success, "output": output}
    
    def full_deploy(self, zip_path: str) -> dict:
        """
        Full deployment: upload zip, extract, rebuild and start container.
        
        Args:
            zip_path: Local path to the deployment zip file
        """
        results = []
        
        # 1. Upload zip
        scp_cmd = f"scp -i {self.key_path} {zip_path} {self.user}@{self.server_ip}:~/"
        try:
            result = subprocess.run(scp_cmd, shell=True, capture_output=True, text=True, timeout=300)
            results.append(("upload", result.returncode == 0, result.stdout + result.stderr))
        except Exception as e:
            return {"success": False, "error": f"Upload failed: {e}"}
        
        # 2. Deploy
        deploy_cmd = f"""cd {self.remote_path} && \
            sudo docker-compose down && \
            sudo rm -f whatsapp_session/whatsapp.lock && \
            unzip -o ~/panaverse_fully_authenticated.zip -d ~/panaverse && \
            sudo docker-compose up --build -d"""
        
        success, output = self._run_ssh_command(deploy_cmd)
        results.append(("deploy", success, output))
        
        return {
            "success": all(r[1] for r in results),
            "steps": results
        }
    
    def download_debug_screenshot(self, local_path: str = "./whatsapp_debug.png") -> dict:
        """Download the WhatsApp debug screenshot from the server"""
        # First copy from container to host
        self._run_ssh_command("sudo docker cp panaversity_watcher:/app/whatsapp_debug.png ~/debug.png")
        
        # Then download to local
        scp_cmd = f"scp -i {self.key_path} {self.user}@{self.server_ip}:~/debug.png {local_path}"
        try:
            result = subprocess.run(scp_cmd, shell=True, capture_output=True, text=True, timeout=60)
            return {"success": result.returncode == 0, "path": local_path}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Standalone usage
if __name__ == "__main__":
    skill = OracleCloudSkill()
    
    print("Checking container status...")
    status = skill.check_container_status()
    print(status)
    
    print("\nGetting recent logs...")
    logs = skill.get_logs(20)
    print(logs["logs"])

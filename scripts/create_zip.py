import os
import zipfile

# Configuration
ZIP_NAME = "panaverse_deploy.zip"
PROJECT_ROOT = "."

EXCLUDES = {
    'node_modules', '.venv', '__pycache__', '.git', '.next', 'dist', 
    'oracle', 'tests', '.vscode', '.idea', 'screenshots', 
    'Cache', 'Code Cache', 'GPUCache', 'ShaderCache', 'GrShaderCache',
    'whatsapp_session', 'linkedin_session'
}

def create_zip():
    if os.path.exists(ZIP_NAME):
        print(f"🗑️  Removing old {ZIP_NAME}...")
        os.remove(ZIP_NAME)

    print(f"📦 Creating deployment package: {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            
            for file in files:
                if file == ZIP_NAME: continue
                if file.endswith('.zip'): continue
                if file.endswith('.key'): continue
                if file.endswith('.log'): continue
                
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, PROJECT_ROOT)
                
                # Skip specific huge files if any (screenshots etc)
                if 'screenshots' in file_path: continue
                
                print(f"  Adding: {arc_name}")
                zipf.write(file_path, arc_name)
    
    size_mb = os.path.getsize(ZIP_NAME) / 1024 / 1024
    print(f"✅ Package created: {ZIP_NAME}")
    print(f"📊 Size: {size_mb:.2f} MB")
    print("\nMove this file to your Ubuntu/WSL environment to deploy.")

if __name__ == "__main__":
    create_zip()

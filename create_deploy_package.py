import os
import zipfile

ZIP_NAME = "panaverse_full_project.zip"
PROJECT_ROOT = "."

EXCLUDES = {
    'node_modules', '.venv', '__pycache__', '.git', '.next', 'dist', 
    'oracle', 'tests', '.vscode', '.idea', 'screenshots', 
    'Cache', 'Code Cache', 'GPUCache', 'ShaderCache', 'GrShaderCache',
    'linkedin_session_backup', 'whatsapp_session_backup', 'temp_session_qr_test',
    'whatsapp_session', 'whatsapp_baileys_session', 'sessions', 'linkedin_session'
}

def create_zip():
    if os.path.exists(ZIP_NAME):
        try:
            os.remove(ZIP_NAME)
        except:
            pass

    print(f"📦 Compressing project into: {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            
            for file in files:
                if file == ZIP_NAME: continue
                if file.endswith('.zip'): continue
                if file.endswith('.log'): continue
                
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, PROJECT_ROOT)
                
                if 'screenshots' in file_path: continue
                
                print(f"  Adding: {arc_name}")
                zipf.write(file_path, arc_name)
    
    print(f"✅ SUCCESS: {ZIP_NAME} is ready!")
    print(f"📍 Location: {os.path.abspath(ZIP_NAME)}")

if __name__ == "__main__":
    create_zip()

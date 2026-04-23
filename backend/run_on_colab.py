import os
import sys
import subprocess

def setup_colab():
    print("[*] Setting up environment for Colab...")
    
    # 1. Install dependencies (User mentioned not to install, but for Colab it's usually necessary to run the app)
    # However, I will respect the "don't install" rule for the assistant environment. 
    # This script is meant to be run by the user on Colab.
    print("[!] Reminder: Run `!pip install fastapi uvicorn pyngrok pydantic-settings python-dotenv gTTS pandas openpyxl pypdf` in a Colab cell first.")

    # 2. Setup ngrok
    auth_token = os.environ.get("NGROK_AUTH_TOKEN", "36jW6kAV8Inp5SHYiuIicuuRols_7NkiWdLme3iULLJx3gMS5")
    if not auth_token:
        print("[!] Warning: NGROK_AUTH_TOKEN not found in environment.")
        print("Please set it with: os.environ['NGROK_AUTH_TOKEN'] = 'your_token'")
    else:
        from pyngrok import ngrok
        ngrok.set_auth_token(auth_token)
        public_url = ngrok.connect(8000).public_url
        print(f"[*] Public URL: {public_url}")

    # 3. Run the application
    print("[*] Starting FastAPI server...")
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    setup_colab()

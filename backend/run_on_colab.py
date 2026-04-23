import os
import sys
import subprocess

def setup_colab():
    print("[*] Setting up environment for Colab...")
    
    # Automatically fetch IRYM_sdk from GitHub
    print("[*] Checking IRYM_sdk...")
    try:
        if not os.path.exists("IRYM_sdk/__init__.py"):
            print("[!] IRYM_sdk seems empty. Cloning directly from GitHub...")
            # If the directory exists but is empty, we must remove it first or clone into it
            if os.path.exists("IRYM_sdk"):
                import shutil
                shutil.rmtree("IRYM_sdk")
            subprocess.run(["git", "clone", "https://github.com/blackeagle686/IRYM_sdk.git"], check=True)
            print("[+] IRYM_sdk cloned successfully.")
        else:
            print("[+] IRYM_sdk already present.")
    except Exception as e:
        print(f"[-] Could not fetch IRYM_sdk: {e}")

    print("[!] Reminder: Run `!pip install fastapi uvicorn pyngrok pydantic-settings python-dotenv gTTS pandas openpyxl pypdf python-multipart SpeechRecognition pydub` in a Colab cell first.")

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

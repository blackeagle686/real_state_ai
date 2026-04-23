import speech_recognition as sr
import os
import io
import tempfile
from pydub import AudioSegment

class SpeechRecognitionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    async def transcribe_audio(self, audio_bytes: bytes, lang: str = "ar-SA"):
        """
        Transcribes audio bytes using SpeechRecognition (Google Web Speech API).
        Requires pydub and ffmpeg installed on the system to convert webm to wav.
        """
        try:
            # Save bytes to a temporary webm file
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_webm:
                temp_webm.write(audio_bytes)
                temp_webm_path = temp_webm.name

            temp_wav_path = temp_webm_path.replace(".webm", ".wav")

            # Convert to wav using pydub
            audio = AudioSegment.from_file(temp_webm_path)
            audio.export(temp_wav_path, format="wav")

            # Transcribe
            with sr.AudioFile(temp_wav_path) as source:
                audio_data = self.recognizer.record(source)
                # Use Google Web Speech API (free)
                text = self.recognizer.recognize_google(audio_data, language=lang)

            # Cleanup
            os.remove(temp_webm_path)
            os.remove(temp_wav_path)

            return text
        except sr.UnknownValueError:
            print("SpeechRecognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from SpeechRecognition service; {e}")
            return ""
        except Exception as e:
            print(f"Error in transcription: {e}")
            return ""

sr_service = SpeechRecognitionService()

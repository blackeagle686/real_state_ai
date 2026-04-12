from gtts import gTTS
import io

class TTSService:
    async def text_to_speech(self, text: str, lang: str = 'ar'):
        """
        Convert text to speech using gTTS (temporary for MVP).
        Returns bytes of the audio file.
        """
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()

tts_service = TTSService()

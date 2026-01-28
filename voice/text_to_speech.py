from gtts import gTTS
import tempfile
import base64
import streamlit as st
import time

def speak(text):
    try:
        tts = gTTS(text=text, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            audio_path = f.name

        audio_bytes = open(audio_path, "rb").read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """

        st.markdown(audio_html, unsafe_allow_html=True)

        # 🔥 IMPORTANT: wait so audio actually plays
        time.sleep(2)

    except Exception as e:
        st.error(f"TTS Error: {e}")

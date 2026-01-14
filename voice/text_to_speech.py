from gtts import gTTS
import tempfile
import base64
import streamlit as st

def speak(text):
    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        audio_path = f.name

    audio_bytes = open(audio_path, "rb").read()
    audio_base64 = base64.b64encode(audio_bytes).decode()

    # 🔥 HTML autoplay + hidden
    audio_html = f"""
    <audio autoplay hidden>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """

    st.markdown(audio_html, unsafe_allow_html=True)


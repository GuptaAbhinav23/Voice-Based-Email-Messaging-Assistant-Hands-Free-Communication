import speech_recognition as sr

def listen():
    r = sr.Recognizer()

    # ---------------- TUNING PARAMETERS ----------------
    r.pause_threshold = 1.2
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 0.8

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening... Speak full command")

        try:
            audio = r.listen(
                source,
                timeout=6,
                phrase_time_limit=8
            )
        except sr.WaitTimeoutError:
            return None   # 👈 IMPORTANT

    try:
        text = r.recognize_google(audio, language="en-IN")
        return text.lower()

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        return None

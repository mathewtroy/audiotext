"""
AudioText App

This application listens through the microphone and converts spoken words into text.
It starts recording after hearing the keyword: "START MY FRIEND"
and stops after hearing: "FINISH MY FRIEND".

All recognized text and system events are saved in logs.txt
"""
from typing import Any

import speech_recognition as sr
from datetime import datetime

LANG = "en-US"           # Language for speech recognition
MIC_INDEX = None         # Use default microphone (set index if needed)
LOG_FILE = "logs.txt"    # Path to the log file


def log(level: str, message: str):
    """
    Write a message to logs.txt with timestamp and level (INFO, DEBUG, ERROR, etc.)
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time_str}] [{level.upper()}] {message}\n")


def setup_recognizer() -> sr.Recognizer:
    """
    Initialize and configure the speech recognizer.
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    return recognizer


def listen_audio(recognizer: sr.Recognizer, source: sr.Microphone):
    """
    Listen to the microphone input and return an audio segment.
    Handles timeout errors gracefully.
    """
    try:
        return recognizer.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        print("⌛ Timeout — no speech detected.")
        return None


def recognize_speech(recognizer: sr.Recognizer, audio) -> Any | None:
    """
    Convert an audio segment to text using Google Speech Recognition.
    Returns recognized text or None if not understood.
    """
    if not audio:
        return None
    try:
        text = recognizer.recognize_google(audio, language=LANG).strip()
        print("➡️ ", text)
        log("DEBUG", f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("🤷 Speech not recognized.")
    except sr.RequestError as e:
        print(f"⚠️ Recognition service error: {e}")
        log("ERROR", f"Recognition service error: {e}")
    return None


def handle_command(text: str, recording: bool, buffer_text: list) -> tuple[bool, bool]:
    """
    Handle special voice commands ("START MY FRIEND", "FINISH MY FRIEND").
    Returns:
        (recording_active, should_exit)
    """
    if not text:
        return recording, False

    low = text.lower()

    # --- Start recording ---
    if "start my friend" in low:
        if not recording:
            buffer_text.clear()
            print("🟢 Recording started.")
            log("INFO", "Recording started.")
        return True, False

    # --- Finish recording and exit ---
    if "finish my friend" in low:
        if recording:
            full_text = " ".join(buffer_text)
            print("🔴 Recording finished.")
            log("INFO", f"Recording stopped. Text: {full_text}")
            print("\n💾 Text saved to logs.txt\n")
        else:
            print("⚠️ 'FINISH MY FRIEND' detected but recording was not active.")
        log("INFO", "Program finished by user command.")
        return False, True

    return recording, False


def record_loop(recognizer: sr.Recognizer):
    """
    Main recording loop:
    - Continuously listens for input
    - Starts recording on "START MY FRIEND"
    - Stops and exits on "FINISH MY FRIEND"
    """
    recording = False
    buffer_text = []

    print("🎙 Say 'START MY FRIEND' to begin recording, 'FINISH MY FRIEND' to stop and exit.")
    log("INFO", "Program started.")

    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

            while True:
                print("🎧 Listening...")
                audio = listen_audio(recognizer, source)
                text = recognize_speech(recognizer, audio)

                # Handle commands
                recording, should_exit = handle_command(text, recording, buffer_text)
                if should_exit:
                    break

                # Save recognized speech during active recording
                if recording and text and not any(
                    phrase in text.lower() for phrase in ["start my friend", "finish my friend"]
                ):
                    buffer_text.append(text)

    except KeyboardInterrupt:
        print("\n👋 Program stopped manually.")
        log("INFO", "Program interrupted manually.")
    except OSError as e:
        print(f"🎧 Microphone error: {e}")
        log("ERROR", f"Microphone error: {e}")
    finally:
        log("INFO", "Program closed.")


def main():
    """
    Entry point: initializes recognizer and starts the recording loop.
    """
    recognizer = setup_recognizer()
    record_loop(recognizer)


if __name__ == "__main__":
    main()

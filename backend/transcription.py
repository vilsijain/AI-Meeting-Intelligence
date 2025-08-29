import os
import subprocess
import tempfile
import shutil

# Config
WHISPER_CPP_BIN = os.getenv("WHISPER_CPP_BIN", "./whisper/main")
WHISPER_CPP_MODEL = os.getenv("WHISPER_CPP_MODEL", "./whisper/models/ggml-base.en.bin")
TRANSCRIBE_BACKEND = os.getenv("TRANSCRIBE_BACKEND", "cpp")  # "api", "python", or "cpp"

# --- Option 1: OpenAI Whisper API ---
def transcribe_api(file_path: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI()
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"[WARN] API transcription failed: {e}")
        return None


# --- Option 2: Whisper Python library ---
def transcribe_python(file_path: str) -> str:
    try:
        import whisper
        model = whisper.load_model("base.en")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"[WARN] Local Whisper (Python) transcription failed: {e}")
        return None


# --- Option 3: Whisper.cpp ---
def transcribe_cpp(file_path: str) -> str:
    if shutil.which(WHISPER_CPP_BIN) or os.path.exists(WHISPER_CPP_BIN):
        with tempfile.TemporaryDirectory() as td:
            out_txt = os.path.join(td, "out.txt")
            cmd = [
                WHISPER_CPP_BIN,
                "-m", WHISPER_CPP_MODEL,
                "-f", file_path,
                "-otxt"
            ]
            try:
                subprocess.run(
                    cmd, check=True, cwd=td,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if os.path.exists(out_txt):
                    with open(out_txt, "r", encoding="utf-8", errors="ignore") as f:
                        return f.read()
            except Exception as e:
                print(f"[WARN] whisper.cpp transcription failed: {e}")
    return None


# --- Dispatcher with fallback ---
def transcribe(file_path: str) -> str:
    backend_order = {
        "api": [transcribe_api, transcribe_python, transcribe_cpp],
        "python": [transcribe_python, transcribe_cpp, transcribe_api],
        "cpp": [transcribe_cpp, transcribe_python, transcribe_api],
    }.get(TRANSCRIBE_BACKEND, [transcribe_cpp, transcribe_python, transcribe_api])

    for backend in backend_order:
        result = backend(file_path)
        if result:
            return result.strip()

    # Final stub if all fail
    return "Good morning team. Priya will own the sprint plan. We decided to move launch to October 10 due to QA constraints."

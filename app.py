from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import tempfile
import os

app = FastAPI()

print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded!")


@app.get("/")
def home():
    return {
        "message": "Speech-to-Text API is running"
    }


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    # Create a temporary file
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Transcribe audio
        segments, info = model.transcribe(temp_file_path)

        # Combine all segments
        text = " ".join(segment.text for segment in segments)

        return {
            "filename": file.filename,
            "language": info.language,
            "text": text
        }

    finally:
        # Delete temporary audio file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
# FastAPI Speech-to-Text API

live running on this address https://speech-to-text-api-gi5p.onrender.com/

A Python FastAPI microservice for converting speech/audio into text using `faster-whisper`.

---

## 1. Project Overview

The Speech-to-Text service is responsible for:

1. Receiving an audio file.
2. Saving the uploaded audio temporarily.
3. Processing the audio using Whisper.
4. Detecting the spoken language.
5. Converting speech into text.
6. Returning the transcription as JSON.

### Architecture

```text
React
   |
   | Audio File
   v
ASP.NET Core API
   |
   | HTTP POST
   v
FastAPI Speech Service
   |
   v
faster-whisper
   |
   v
Whisper Model
   |
   v
Transcribed Text
   |
   v
ASP.NET Core
   |
   v
React
```

---

# 2. Requirements

Install the following:

- Python 3.13
- VS Code
- Git
- GitHub account
- FastAPI
- Uvicorn
- faster-whisper

For this project, Python 3.13 is used because the speech-processing dependencies need a compatible Python environment.

---

# 3. Create the Project Folder

Create a folder for the speech service.

Example:

```text
D:\Akash\College Project\speech-service
```

Open PowerShell and run:

```powershell
cd "D:\Akash\College Project"
mkdir speech-service
cd speech-service
```

---

# 4. Check Python

Check the installed Python versions:

```powershell
py --list
```

Check Python 3.13:

```powershell
py -3.13 --version
```

Expected:

```text
Python 3.13.x
```

---

# 5. Create a Virtual Environment

Create a virtual environment using Python 3.13:

```powershell
py -3.13 -m venv venv
```

The project should now contain:

```text
speech-service/
└── venv/
```

---

# 6. Activate the Virtual Environment

For PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(venv) PS D:\Akash\College Project\speech-service>
```

The `(venv)` indicates that the virtual environment is active.

---

# 7. Upgrade pip

Run:

```powershell
python -m pip install --upgrade pip
```

---

# 8. Install FastAPI

Install FastAPI, Uvicorn, and multipart support:

```powershell
pip install fastapi uvicorn python-multipart
```

### Packages

| Package | Purpose |
|---|---|
| FastAPI | Creates the REST API |
| Uvicorn | Runs the FastAPI application |
| python-multipart | Handles multipart file uploads |

---

# 9. Create `app.py`

Create the following file:

```text
speech-service/
├── venv/
└── app.py
```

Add the following code:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Speech-to-Text API is running"
    }
```

---

# 10. Run the FastAPI Server

Run:

```powershell
uvicorn app:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
    "message": "Speech-to-Text API is running"
}
```

---

# 11. Open FastAPI Swagger Documentation

FastAPI automatically provides Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger will allow you to test API endpoints directly from the browser.

---

# 12. Install faster-whisper

Install the Whisper speech-recognition library:

```powershell
pip install faster-whisper
```

This installs the Python library and its required dependencies.

---

# 13. Test faster-whisper Separately

Before connecting Whisper to FastAPI, test the Whisper model independently.

Create:

```text
test_whisper.py
```

Project structure:

```text
speech-service/
├── venv/
├── app.py
└── test_whisper.py
```

Add:

```python
from faster_whisper import WhisperModel

print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Model loaded successfully!")
```

Run:

```powershell
python test_whisper.py
```

The first time the model is used, required model files may be downloaded.

Expected result:

```text
Loading Whisper model...
Model loaded successfully!
```

If this works without errors, the Whisper environment is ready.

---

# 14. Create the `/transcribe` Endpoint

Now modify `app.py` so that it accepts an uploaded audio file.

Use:

```python
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

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:

        segments, info = model.transcribe(
            temp_file_path
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return {
            "filename": file.filename,
            "language": info.language,
            "text": text
        }

    finally:

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
```

---

# 15. Start the API

Run:

```powershell
uvicorn app:app --reload
```

The server should load the Whisper model.

Expected:

```text
Loading Whisper model...
Whisper model loaded!
```

---

# 16. Test `/transcribe` Using Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

You should now see:

```text
GET  /
POST /transcribe
```

Open:

```text
POST /transcribe
```

Click:

```text
Try it out
```

Then choose an audio file.

Click:

```text
Execute
```

---

# 17. Example Response

A successful request should return something similar to:

```json
{
    "filename": "test.wav",
    "language": "en",
    "text": "This is a speech to text conversion test."
}
```

The important property is:

```json
"text": "This is a speech to text conversion test."
```

This is the actual transcription produced by Whisper.

---

# 18. Supported Audio Files

The service can work with many common audio formats when the underlying audio decoder supports them.

Common formats to test include:

```text
.wav
.mp3
.m4a
.flac
.ogg
.opus
.aac
```

MP4 is different because it is normally a container that may contain video and audio.

For MP4 support, it is better to extract/convert the audio track before sending it to Whisper.

Recommended project support:

```text
WAV
MP3
M4A
FLAC
OGG
MP4 (with audio extraction/conversion)
```

---

# 19. Temporary Audio Files

The API uses a temporary file:

```python
tempfile.NamedTemporaryFile()
```

The uploaded audio is temporarily stored on the server.

After transcription:

```python
os.remove(temp_file_path)
```

deletes the temporary file.

This prevents uploaded audio from accumulating on the server.

---

# 20. React → FastAPI Request

React can send an audio file using `FormData`.

Example:

```javascript
const formData = new FormData();

formData.append("file", audioFile);

const response = await fetch(
    "http://127.0.0.1:8000/transcribe",
    {
        method: "POST",
        body: formData
    }
);

const result = await response.json();

console.log(result.text);
```

The field name must be:

```text
file
```

because FastAPI expects:

```python
file: UploadFile = File(...)
```

---

# 21. FastAPI → React Response

FastAPI returns:

```json
{
    "filename": "recording.wav",
    "language": "en",
    "text": "Hello this is my speech."
}
```

React can display:

```javascript
result.text
```

Example:

```javascript
setTranscript(result.text);
```

---

# 22. ASP.NET Core → FastAPI

For the final project architecture, React should communicate with the ASP.NET Core API.

ASP.NET Core then communicates with FastAPI.

```text
React
   |
   | POST audio
   v
ASP.NET Core
   |
   | POST audio
   v
FastAPI
   |
   v
Whisper
   |
   v
Text
   |
   v
FastAPI
   |
   | JSON
   v
ASP.NET Core
   |
   v
React
```

This keeps FastAPI as a dedicated speech-processing microservice.

---

# 23. ASP.NET Core Request

ASP.NET Core can send the uploaded file to FastAPI using `HttpClient`.

Example:

```csharp
using var content = new MultipartFormDataContent();

using var stream = audio.OpenReadStream();

using var fileContent = new StreamContent(stream);

content.Add(
    fileContent,
    "file",
    audio.FileName
);

var response = await _httpClient.PostAsync(
    "http://localhost:8000/transcribe",
    content
);
```

Notice:

```text
"file"
```

must match the FastAPI endpoint.

---

# 24. FastAPI Response Model in ASP.NET Core

Example:

```csharp
public class SpeechResponse
{
    public string Filename { get; set; } = "";
    public string Language { get; set; } = "";
    public string Text { get; set; } = "";
}
```

Then:

```csharp
var result =
    await response.Content.ReadFromJsonAsync<SpeechResponse>();
```

The ASP.NET Core API can then return:

```json
{
    "text": "Hello this is my speech."
}
```

to React.

---

# 25. CORS

If React communicates directly with FastAPI during development, CORS may be required.

Install/use:

```python
from fastapi.middleware.cors import CORSMiddleware
```

Configure:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If React communicates only with ASP.NET Core and ASP.NET Core communicates with FastAPI, FastAPI does not necessarily need to expose CORS to the browser.

---

# 26. Create `.gitignore`

Create:

```text
.gitignore
```

Add:

```gitignore
venv/
__pycache__/
*.pyc
.env
```

Do not upload the `venv` directory to GitHub.

---

# 27. Create `requirements.txt`

After installing all required packages:

```powershell
pip freeze > requirements.txt
```

The project becomes:

```text
speech-service/
├── venv/
├── app.py
├── test_whisper.py
├── requirements.txt
└── .gitignore
```

---

# 28. Run the Project Again

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Test:

```text
POST /transcribe
```

---

# 29. Deployment Architecture

For deployment, the FastAPI service can be hosted separately from the ASP.NET Core API.

```text
                    React
                       |
                       v
              ASP.NET Core API
                       |
                       | HTTP
                       v
              FastAPI Microservice
                       |
                       v
                 faster-whisper
                       |
                       v
                  Whisper Model
                       |
                       v
                  Transcription
```

The ASP.NET Core API becomes the main backend, while FastAPI is responsible for speech recognition.

---

# 30. Production/Deployment Start Command

When deploying FastAPI to a cloud platform, do not use:

```text
uvicorn app:app --reload
```

Use a production-style command such as:

```text
uvicorn app:app --host 0.0.0.0 --port $PORT
```

The hosting platform provides the `$PORT` environment variable.

---

# 31. Local Development vs Deployment

### Local

```text
uvicorn app:app --reload
```

### Cloud

```text
uvicorn app:app --host 0.0.0.0 --port $PORT
```

---

# 32. Final Project Structure

Recommended structure:

```text
speech-service/
│
├── venv/
│
├── app.py
│
├── test_whisper.py
│
├── requirements.txt
│
└── .gitignore
```

---

# 33. Complete API Flow

```text
1. User selects/records audio
             |
             v
2. React sends audio to ASP.NET Core
             |
             v
3. ASP.NET Core sends audio to FastAPI
             |
             v
4. FastAPI receives UploadFile
             |
             v
5. FastAPI creates temporary file
             |
             v
6. faster-whisper reads the audio
             |
             v
7. Whisper converts speech to text
             |
             v
8. FastAPI creates JSON response
             |
             v
9. ASP.NET Core receives JSON
             |
             v
10. ASP.NET Core returns result to React
             |
             v
11. React displays transcription
```

---

# 34. Important Commands Summary

### Create environment

```powershell
py -3.13 -m venv venv
```

### Activate

```powershell
.\venv\Scripts\Activate.ps1
```

### Install packages

```powershell
pip install fastapi uvicorn python-multipart
pip install faster-whisper
```

### Start API

```powershell
uvicorn app:app --reload
```

### Create requirements

```powershell
pip freeze > requirements.txt
```

### Swagger

```text
http://127.0.0.1:8000/docs
```

### Root endpoint

```text
http://127.0.0.1:8000/
```

### Transcription endpoint

```text
POST http://127.0.0.1:8000/transcribe
```

---

# 35. Current Status

At this stage, the FastAPI speech service should be able to:

- Start successfully.
- Load the Whisper model.
- Accept an uploaded audio file.
- Process the audio.
- Detect the spoken language.
- Generate a transcription.
- Return the transcription as JSON.
- Delete the temporary uploaded file.

The next development stage is to connect this service to the ASP.NET Core backend and then connect the ASP.NET Core endpoint to the React frontend.
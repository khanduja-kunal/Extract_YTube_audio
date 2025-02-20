from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import time
import os
import tempfile

app = FastAPI()

# Temporary folder for storing files during download
TEMP_DIR = tempfile.gettempdir()

@app.get("/extract-YouTube-audio/")
async def download_audio(url: str):
    try:
        # Generate a unique filename based on the timestamp
        timestamp = int(time.time())
        file_name = f"audio_{timestamp}.mp3"
        file_path = os.path.join(TEMP_DIR, file_name)

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best available audio
            'outtmpl': file_path,  # Save the file temporarily in the temp folder
        }

        # Use yt-dlp to download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Return the file path for download (this will be served to the user)
        return FileResponse(file_path, media_type="audio/mp3", headers={"Content-Disposition": f"attachment; filename={file_name}"})
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading audio: " + str(e))

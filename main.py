import os
from fastapi import FastAPI, Response
import edge_tts
import io
from pydub import AudioSegment

app = FastAPI()

@app.post("/talk")
async def talk():
    try:
        # النص اللي زيزو حيقوله باختبار الـ 16000Hz
        text = "يا خالد، أنا زيزو، الصوت دلوقت مضبوط على ستة عشر ألف هرتز."
        
        communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
        mp3_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3_data += chunk["data"]
                
        # تحويل من MP3 إلى PCM خام (16000Hz) عشان السماعة تفهم
        audio = AudioSegment.from_file(io.BytesIO(mp3_data), format="mp3")
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        pcm_data = audio.raw_data
        
        return Response(content=pcm_data, media_type="application/octet-stream")
    except Exception as e:
        return Response(content=str(e), status_code=500)

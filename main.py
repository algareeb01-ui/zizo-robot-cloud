from fastapi import FastAPI, Response
import edge_tts
import io
from pydub import AudioSegment

app = FastAPI()

@app.get("/talk-wav")
async def talk_wav():
    text = "يا خالد، أنا زيزو، بنجرب الصوت دلوقت بدون صفارة القطر."
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    
    data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            data += chunk["data"]
            
    # تحويل الـ MP3 لـ WAV (PCM 16-bit, 16000Hz, Mono)
    audio = AudioSegment.from_file(io.BytesIO(data), format="mp3")
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    
    raw_data = audio.raw_data # هنا الزيتونة: بيانات خام صافية
    
    return Response(content=raw_data, media_type="application/octet-stream")

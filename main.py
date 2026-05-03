from fastapi import FastAPI, Response
import edge_tts
import io
import wave

app = FastAPI()

@app.get("/talk-wav")
async def talk_wav():
    text = "يا خالد، أنا زيزو، بنجرب الصوت بنظام الويف الصافي."
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    
    # تحويل الصوت لبيانات
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    # إرسالها كملف صوتي خام (WAV)
    return Response(content=audio_data, media_type="audio/wav")

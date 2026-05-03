from fastapi import FastAPI, Response
import edge_tts

app = FastAPI()

@app.get("/talk-wav")
async def talk_wav():
    text = "يا خالد، أنا زيزو، شغالين دلوقت بأخف نظام عشان ريندر يرضى علينا."
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    # بنرسل البيانات MP3 بس بنعرف الأردوينو إنها داتا دفق
    return Response(content=audio_data, media_type="audio/mpeg")

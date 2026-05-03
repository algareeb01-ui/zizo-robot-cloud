from fastapi import FastAPI, Response
import edge_tts

app = FastAPI()

@app.get("/talk-wav")
async def talk_wav():
    text = "يا خالد، أنا زيزو، بنجرب الصوت الخام دلوقت."
    # لاحظ هنا: طلبنا منه يطلع صوت خام (raw) وبجودة محددة
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    # بنرسلها كبيانات ثنائية خام
    return Response(content=audio_data, media_type="application/octet-stream")

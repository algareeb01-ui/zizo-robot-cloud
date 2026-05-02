from fastapi import FastAPI, Response
import edge_tts

app = FastAPI()

@app.post("/talk")
async def talk():
    try:
        # النص اللي زيزو حيقوله
        text = "يا خالد، أنا زيزو، دلوقت السيرفر شغال بأقل استهلاك ومستعد للأوامر."
        
        # تحويل النص لصوت
        communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        # إرسال البيانات كـ Stream
        return Response(content=audio_data, media_type="application/octet-stream")
    except Exception as e:
        return Response(content=str(e), status_code=500)

import os
from fastapi import FastAPI, Response
import edge_tts

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Zizo is Live"}

@app.post("/talk")
async def talk():
    try:
        # نص بسيط جداً للاختبار
        text = "يا خالد، أنا زيزو، سامعني دلوقت؟"
        communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
        
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        return Response(content=str(e), status_code=500)

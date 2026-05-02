import os
from fastapi import FastAPI, Response
import edge_tts

app = FastAPI()

@app.post("/talk")
async def talk():
    try:
        # نص قصير جداً
        communicate = edge_tts.Communicate("يا خالد، هل الصوت الآن أوضح؟", "ar-EG-ShakirNeural")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        # بنرسل البيانات "خام" قدر الإمكان
        return Response(content=audio_data, media_type="application/octet-stream")
    except Exception as e:
        return Response(content=str(e), status_code=500)

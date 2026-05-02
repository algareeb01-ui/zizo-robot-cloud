import os
from fastapi import FastAPI, Response
import edge_tts
import io

app = FastAPI()

@app.post("/talk")
async def talk():
    try:
        text = "يا خالد، أنا زيزو، دلوقت بكلمك بأخف طريقة ممكنة."
        communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
        
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        # بنرسل الداتا زي ما هي، والأردوينو حيشغلها بتردد 24000
        return Response(content=audio_data, media_type="application/octet-stream")
    except Exception as e:
        return Response(content=str(e), status_code=500)

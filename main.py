from fastapi import FastAPI, Response
import edge_tts

app = FastAPI()

@app.post("/talk")
async def talk():
    try:
        text = "يا خالد، أنا زيزو، بنجرب نهدي الكلاشنكوف ونسمع الصوت."
        communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return Response(content=audio_data, media_type="application/octet-stream")
    except Exception as e:
        return Response(content=str(e), status_code=500)

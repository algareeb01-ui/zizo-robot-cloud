from fastapi import FastAPI, Response
import edge_tts
import io

app = FastAPI()

@app.get("/talk-wav")
async def talk_wav():
    text = "يا خالد، أنا زيزو، القطر وقف في المحطة دلوقت."
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    # بنرسل البيانات زي ما هي، بس في الأردوينو حنغير "السرعة"
    return Response(content=audio_data, media_type="audio/mpeg")

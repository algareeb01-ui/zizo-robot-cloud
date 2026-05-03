from fastapi import FastAPI, Response
import edge_tts

app = FastAPI()

@app.get("/talk-wav")
async def talk_wav():
    # دي الجملة اللي حنسمعها عشان نتأكد إن "القطر" وقف
    text = "يا خالد، أنا زيزو، الصوت دلوقت صافي والقطر وقف في المحطة."
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    # بنرسل البيانات بصيغة Octet-Stream يعني "بيانات خام" للسماعة
    return Response(content=audio_data, media_type="application/octet-stream")

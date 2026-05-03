from fastapi import FastAPI, Response
import edge_tts
import io
import wave

app = FastAPI()

@app.get("/talk-wav")
async def talk_wav():
    text = "يا خالد، أنا زيزو، بنجرب التنسيق الصافي دلوقت."
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    
    # استلام الـ MP3 في الذاكرة
    mp3_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_data += chunk["data"]
            
    # هنا التريك: بنرسل البيانات دي للأردوينو
    # وعشان نتفادى مشاكل التشفير، حنرسل الـ bytes مباشرة 
    # بس بنظام chunking عشان الأردوينو ما يغرق
    return Response(content=mp3_data, media_type="audio/mpeg")

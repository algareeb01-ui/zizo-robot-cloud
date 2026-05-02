import os
from fastapi import FastAPI, Request, Response
import google.generativeai as genai
import edge_tts
import io

app = FastAPI()

@app.post("/talk")
async def talk_to_zizo(request: Request):
    try:
        # نص الاختبار
        test_text = "يا خالد، أنا زيزو. لو سامعني دلوقت بوضوح، يبقى الماسورة سلكت تمام."
        
        # تحويل النص لصوت
        communicate = edge_tts.Communicate(test_text, "ar-EG-ShakirNeural")
        
        # هنا السر: حنخلي السيرفر يبعت البيانات بطريقة السماعة تفهمها
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        # إرسال البيانات
        return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        return Response(content=str(e), status_code=500)

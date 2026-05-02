import os
from fastapi import FastAPI, Request, Response
import edge_tts

app = FastAPI()

@app.post("/talk")
async def test_pipe(request: Request):
    try:
        # نص الاختبار اللي حيحوله السيرفر لصوت
        test_text = "يا خالد، أنا زيزو، سماعاتك شغالة مية مية والصوت واصل من السحاب."
        
        # تحويل النص لصوت (نقي جداً)
        communicate = edge_tts.Communicate(test_text, "ar-EG-ShakirNeural")
        audio_content = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_content += chunk["data"]
        
        print("📤 Sending Clean Test Audio...")
        return Response(content=audio_content, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return Response(content="Error", status_code=500)

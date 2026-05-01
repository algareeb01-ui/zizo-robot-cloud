import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import speech_recognition as sr
import google.generativeai as genai
import edge_tts

app = FastAPI()

# إعداد جيميناي بمفتاحك
genai.configure(api_key="AIzaSyC1vFu_CVnwVxgS4V6UlTL1AjJ4mNbZv7g")
model = genai.GenerativeModel("gemini-1.5-flash")
recognizer = sr.Recognizer()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ ESP32 Connected")
    
    try:
        while True:
            # استلام إشارة من الـ ESP32
            msg = await websocket.receive()
            
            if "text" in msg:
                cmd = msg["text"]
                
                # السيناريو: الـ ESP32 سمع "زيزو" ورد "نعم" ويبدأ الآن إرسال السؤال
                if cmd == "START_QUERY":
                    print("🎤 زيزو بدأ يستلم السؤال من خالد...")
                    audio_data_list = []
                    
                    # استلام بايتات الصوت (السؤال)
                    try:
                        while True:
                            # تايم آوت 7 ثوانٍ للسؤال
                            audio_msg = await asyncio.wait_for(websocket.receive(), timeout=7.0)
                            if "bytes" in audio_msg:
                                audio_data_list.append(audio_msg["bytes"])
                            else:
                                break
                    except asyncio.TimeoutError:
                        print("⏳ انتهى وقت تسجيل السؤال.")

                    if audio_data_list:
                        full_audio = b"".join(audio_data_list)
                        try:
                            # تحويل الصوت لنص عبر جوجل
                            audio_io = sr.AudioData(full_audio, 16000, 2)
                            query = recognizer.recognize_google(audio_io, language="ar-TN")
                            print(f"❓ السؤال المسموع: {query}")

                            # إرسال السؤال لـ جيميناي مع البرومبت الخاص بـ "زيزو"
                            prompt = "أنت زيزو، روبوت تونسي ذكي. أجب بجملة واحدة قصيرة جداً بلهجة تونسية ودودة."
                            response = model.generate_content([prompt, query])
                            reply = response.text.strip()
                            print(f"🤖 رد زيزو: {reply}")

                            # تحويل الرد لصوت (Edge-TTS) - صيغة MP3 خفيفة جداً
                            # معدل السرعة +10% والحدة +10% لصوت طفولي
                            communicate = edge_tts.Communicate(reply, "ar-EG-SalmaNeural", rate="+10%", pitch="+10%")
                            
                            # إبلاغ الـ ESP32 ببدء إرسال الرد الصوتي
                            await websocket.send_text("START_AUDIO")
                            
                            async for chunk in communicate.stream():
                                if chunk["type"] == "audio":
                                    # إرسال بايتات الـ MP3
                                    await websocket.send_bytes(chunk["data"])
                            
                            # إبلاغ الـ ESP32 بانتهاء الرد
                            await websocket.send_text("END_AUDIO")
                            print("✅ تم إرسال الرد بالكامل.")
                            
                        except Exception as e:
                            print(f"❌ خطأ في المعالجة: {e}")
                            await websocket.send_text("ERROR")

    except WebSocketDisconnect:
        print("🔌 انقطع الاتصال مع ESP32")

if __name__ == "__main__":
    import uvicorn
    # الحصول على البورت من بيئة Render أو استخدام 8000 افتراضياً
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

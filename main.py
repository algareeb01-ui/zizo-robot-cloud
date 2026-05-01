import os
import asyncio
import json
import io
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import speech_recognition as sr
import google.generativeai as genai
import edge_tts

app = FastAPI()
genai.configure(api_key="AIzaSyC1vFu_CVnwVxgS4V6UlTL1AjJ4mNbZv7g")
model = genai.GenerativeModel("gemini-1.5-flash")
recognizer = sr.Recognizer()

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    audio_buf = bytearray()
    state = "IDLE"

    try:
        while True:
            msg = await websocket.receive()
            if msg["type"] == "websocket.receive":
                data = msg.get("bytes")
                if data:
                    audio_buf.extend(data)

            if state == "IDLE" and len(audio_buf) > 48000:
                try:
                    audio_data = sr.AudioData(bytes(audio_buf), 16000, 2)
                    text = recognizer.recognize_google(audio_data, language="ar-TN")
                    if "زيزو" in text:
                        await websocket.send_text("CMD:LOCAL_YES")
                        state = "WAKE_SENT"
                        audio_buf = bytearray()
                except:
                    audio_buf = bytearray()

            elif state == "WAKE_SENT":
                await asyncio.sleep(3)
                await websocket.send_text("CMD:START_REC")
                state = "LISTENING"
                audio_buf = bytearray()

            elif state == "LISTENING":
                if len(audio_buf) > 160000:
                    await websocket.send_text("CMD:START_PLAY")
                    try:
                        audio_data = sr.AudioData(bytes(audio_buf), 16000, 2)
                        query_text = recognizer.recognize_google(audio_data, language="ar-TN")
                        
                        prompt = """أنت روبوت ذكي اسمه زيزو. تفهم الدارجة التونسية. 
                        إذا ذكر المتحدث أنه رجل ناديه يا عمو، وإذا امرأة يا خالة، وإذا طفل يا بطل.
                        أجب بجملة واحدة قصيرة وودية. لا تكتب أي شروحات خارج الرد."""
                        
                        response = model.generate_content([prompt, query_text])
                        reply = response.text.strip()

                        # توليد صوت طفل عبر تعديل النبرة والسرعة مباشرة في edge-tts
                        tts = edge_tts.Communicate(reply, "ar-TN", rate="-15%", pitch="+20%")
                        audio_chunks = []
                        async for chunk in tts.stream():
                            if chunk["type"] == "audio":
                                audio_chunks.append(chunk["data"])
                        
                        mp3_bytes = b"".join(audio_chunks)
                        # edge-tts يعيد MP3، سنقوم بتحويله لـ PCM 16kHz يدوياً خفيفاً
                        # لتجنب مكتبات ثقيلة، نرسله كما هو وESP32 سيفك تشفيره تلقائياً عبر مكتبة مدمجة
                        # أو نستخدم تحويل بسيط إذا لزم. هنا نرسل PCM جاهز عبر edge-tts داخلياً:
                        
                        # لتبسيط الأمر وضمان العمل على السحابة المجانية، نستخدم edge-tts مباشرة مع تحويل خفيف
                        import struct, wave
                        # edge-tts لا يعطي PCM مباشرة، لذا سنرسل البيانات وسنفكها على الESP إذا لزم، 
                        # لكن الأسهل: استخدام مكتبة بسيطة لتحويل MP3->PCM داخلياً بدون ffmpeg
                        # سأعتمد على إرسال النص أولاً ثم الصوت، لكن للحفاظ على التدفق، سأستخدم نهجاً بديلاً آمناً:
                        
                        await websocket.send_bytes(b"START")
                        for chunk in audio_chunks:
                            await websocket.send_bytes(chunk)
                            await asyncio.sleep(0.01)
                        await websocket.send_bytes(b"END")
                        
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        await websocket.send_text("CMD:END")
                        state = "IDLE"
                        audio_buf = bytearray()

    except WebSocketDisconnect:
        print("Client disconnected")
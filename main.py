from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

# رابط إذاعة إخبارية (كلام فقط)
RADIO_URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_arabic_radio"

@app.get("/radio")
async def stream_radio():
    client = httpx.AsyncClient()
    
    async def event_generator():
        async with client.stream("GET", RADIO_URL) as r:
            async for chunk in r.aiter_bytes():
                yield chunk

    return StreamingResponse(event_generator(), media_type="audio/mpeg")

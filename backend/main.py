from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS für Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OSSRS URLs
OSSRS_BASE_URL = "http://localhost:8080"
OSSRS_API_URL = "http://localhost:1985/api/v1"


@app.get("/")
async def root():
    return {"message": "Stream API is running"}


@app.get("/api/stream-info")
async def fetch_stream():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OSSRS_API_URL}/streams/")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stream-url")
async def get_stream_url():
    stream_name = "livestream"

    # HTTP-FLV Stream URL für direkten Zugriff
    stream_url = f"{OSSRS_BASE_URL}/live/{stream_name}.flv"

    # HLS Stream URL (alternative)
    hls_url = f"{OSSRS_BASE_URL}/live/{stream_name}.m3u8"

    return {
        "flv_url": stream_url,
        "hls_url": hls_url,
        "rtmp_url": f"rtmp://localhost/live/{stream_name}",
        "player_url": f"{OSSRS_BASE_URL}/players/srs_player.html?autostart=true&app=live&stream={stream_name}.flv&server=localhost&port=8080&vhost=localhost&schema=http",
    }

from fastapi import FastAPI
# from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/")
def fetch_stream(streamBytes: bytes):
    # return StreamingResponse(streamBytes, {"message": "Stream fetched successfully"})
    return {"message": "Stream fetched successfully", "data: ": streamBytes}

@app.post("/post-stream")
def create_stream(rtmp_url: str):
    if not rtmp_url:
        return {"error": "No data provided"}
    return {"message": "Stream created successfully", "data": rtmp_url}



from fastapi import FastAPI, File, UploadFile
import asyncio
from gait_processor import process_image, process_video

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    is_video = file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
    
    # Read file into memory quickly
    file_bytes = await file.read()
    
    if not is_video:
        # Offload image processing to a background thread
        features = await asyncio.to_thread(process_image, file_bytes)
        return {"feature_vector": features}
        
    else:
        # Offload heavy video frame extraction and batched inference to a thread
        try:
            features, frame_count = await asyncio.to_thread(process_video, file_bytes)
            
            if features is None:
                return {"error": "Could not extract frames from the video."}
                
            return {
                "message": f"Processed {frame_count} frames",
                "feature_vector": features
            }
            
        except Exception as e:
            return {"error": f"Video processing failed: {str(e)}"}

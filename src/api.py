# src/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .service import pipeline
from .logger import setup_logger

logger = setup_logger()
app = FastAPI(title="🎬 YouTube RAG Backend", version="1.0")

# Cache pipelines per video
pipelines = {}

# ----------------- Request Schemas -----------------
class ProcessRequest(BaseModel):
    video_id: str

class QueryRequest(BaseModel):
    video_id: str
    question: str

# ----------------- ROUTES -----------------

@app.post("/process")
async def process_video(request: ProcessRequest):
    """
    Process a YouTube video (fetch transcript, split text, create embeddings, store FAISS index).
    This runs once per video.
    """
    video_id = request.video_id.strip()
    logger.info(f" Processing video: {video_id}")

    try:
        if video_id in pipelines:
            logger.info(f" Video {video_id} already processed. Skipping re-processing.")
            return {"status": "success", "message": "Video already processed."}

        # Initialize pipeline and prepare data
        pl = pipeline(video_id)
        await pl.prepare()
        pipelines[video_id] = pl

        logger.info(f" Video {video_id} processed successfully.")
        return {"status": "success", "message": f"Video {video_id} processed successfully."}

    except Exception as e:
        logger.error(f" Error processing video {video_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_video(request: QueryRequest):
    """
    Query a previously processed video for an answer.
    """
    video_id = request.video_id.strip()
    question = request.question.strip()
    logger.info(f" Query for {video_id}: {question}")

    try:
        # Check if video is processed
        if video_id not in pipelines:
            raise HTTPException(status_code=404, detail=f"Video {video_id} not processed yet. Call /process first.")

        pl = pipelines[video_id]
        answer = await pl.ask(question)
        logger.info(f" Answer ready for {video_id}")

        return {"video_id": video_id, "question": question, "answer": answer}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f" Error answering question for {video_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "RAG API is running 🚀"}

from src.data_ingestion import fetch_transcript
import asyncio
async def main():
    video_id="BMym71Dwox0"
    ans=await fetch_transcript(video_id)
    
asyncio.run(main)
    
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import asyncio
from concurrent.futures import ThreadPoolExecutor
from googletrans import Translator
from src.logger import setup_logger

logger=setup_logger()
executor=ThreadPoolExecutor()
translator=Translator()
async def fetch_transcript(video_id:str,translate_to_en=True    )->str:
    """
    Asynchronously fetches and joins transcript text for a given YouTube video ID.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        str: The concatenated transcript text, or an empty string if unavailable.
    """
    logger.info(f"Fetching transcript for video_id: {video_id}")

    loop = asyncio.get_running_loop()
    
    try:
        
        #ytt_api = YouTubeTranscriptApi()
        transcript_list=await loop.run_in_executor(executor,lambda vid: YouTubeTranscriptApi().fetch(vid),video_id)
                                               
       
        transcript = " ".join(chunk.text for chunk in transcript_list)
        
        logger.info(f" Successfully fetched transcript ({len(transcript_list)} segments)")
        return transcript
    except NoTranscriptFound:
        logger.error("No transcript available for this video")
        return ""
    except TranscriptsDisabled:
        logger.error("No captions available for this video.")
        return ""
    except Exception as e:
        logger.exception(f" Unexpected error fetching transcript for {video_id}: {e}")
        return ""
    


    
    


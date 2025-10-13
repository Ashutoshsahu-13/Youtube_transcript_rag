from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

from logger import setup_logger

logger=setup_logger()

def fetch_transcript(video_id:str)->str:
    """Fetch and join transcript text for a given YouTube video ID."""
    try:
        logger.info(f"Fetching transcript for {video_id}")
        ytt_api = YouTubeTranscriptApi()
        transcript_list=ytt_api.fetch(video_id)
        transcript = " ".join(chunk.text for chunk in transcript_list)
        return transcript
    except NoTranscriptFound:
        logger.error("No transcript available for this video")
    except TranscriptsDisabled:
        logger.error("No captions available for this video.")

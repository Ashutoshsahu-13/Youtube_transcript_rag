from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator
from src.logger import setup_logger
import asyncio
logger = setup_logger()
translator = Translator()

async def translate_async(text: str) -> str:
    """Run async googletrans translate."""
    result = await translator.translate(text, dest="en")
    return result.text


def translate_sync(text: str) -> str:
    """Runs async translator inside sync function."""
    return asyncio.run(translate_async(text))

def fetch_transcript_sync(video_id: str, translate_to_en=True) -> str:
    """
    Works with youtube-transcript-api v1.2.3
    Fetches EN or HI subtitles (manual or auto-generated) using .fetch()
    Detects Hindi and translates to English.
    """
    logger.info(f"Fetching transcript for video_id: {video_id}")

    try:
        # Your version ONLY supports `.fetch`
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en', 'hi'])

        text = " ".join(item.text for item in transcript_list)
        print(len(transcript_list))
        
        print(transcript_list)
    
        

        # # Check if Hindi content exists (Unicode check)
        # if translate_to_en and contains_hindi(text):
        #     logger.info("Detected Hindi transcript. Translating to English...")
        #     text = translate_sync(text)

        logger.info("Transcript fetched successfully.")
        return text

    except NoTranscriptFound:
        logger.error("No transcript found.")
        return ""
    except TranscriptsDisabled:
        logger.error("Transcripts disabled.")
        return ""
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return ""


def contains_hindi(text: str) -> bool:
    """Detect Hindi characters by Unicode range."""
    for ch in text:
        if '\u0900' <= ch <= '\u097F':
            return True
    return False


if __name__=="__main__":
    text=fetch_transcript_sync(video_id="BMym71Dwox0")
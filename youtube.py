import re
import os
import logging
from typing import Optional, Tuple, List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_video_id(url: str) -> Optional[str]:
    """
    Extracts the 11-character video ID from a YouTube URL.
    Supports standard, shorts, and youtu.be URLs.
    """
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtube\.com\/shorts\/)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_video_title(video_id: str, api_key: str) -> Optional[str]:
    """
    Fetches the video title using the YouTube Data API.
    """
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        items = response.get("items", [])
        if items:
            return items[0]["snippet"]["title"]
        else:
            logger.error(f"No video found with id: {video_id}")
            return None
    except HttpError as e:
        logger.error(f"YouTube API error: {e}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return None


def get_transcript_text(video_id: str) -> Optional[str]:
    """
    Retrieves the transcript for the given video ID.
    If English transcripts are available, prefers manually created ones;
    otherwise falls back to automatically generated transcripts or translation.
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        all_transcripts: List[Any] = list(transcript_list)
        english_transcripts = [t for t in all_transcripts if t.language_code.startswith("en")]

        if english_transcripts:
            manual_transcripts = [t for t in english_transcripts if not t.is_generated]
            chosen_transcript = manual_transcripts[0] if manual_transcripts else english_transcripts[0]
            logger.info(
                f"Using {'manually created' if not chosen_transcript.is_generated else 'automatically generated'} "
                f"English transcript: {chosen_transcript.language_code}"
            )
            transcript = chosen_transcript.fetch()
        else:
            # Fallback: translate the first available transcript to English.
            logger.info(
                f"No English transcript found. Translating from {all_transcripts[0].language_code} to English."
            )
            transcript = all_transcripts[0].translate("en").fetch()

        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        logger.error("Transcripts are disabled or not found for this video.")
        return None
    except Exception as e:
        logger.exception("Unable to process this video. It may not have captions or audio.")
        return None


def validate_transcript(transcript: Optional[str]) -> bool:
    """Simple validation to check if transcript is not None or empty."""
    return bool(transcript and transcript.strip())


def process_youtube_video(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts the video ID from a URL, retrieves the video title and transcript.
    
    Returns a tuple (video_title, transcript) or (video_title, None) if transcript not available.
    """
    video_id = extract_video_id(url)
    if not video_id:
        logger.error("Invalid YouTube URL.")
        return None, None

    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if not youtube_api_key:
        logger.error("YOUTUBE_API_KEY is not set in environment variables.")
        return None, None

    video_title = get_video_title(video_id, youtube_api_key)
    transcript = get_transcript_text(video_id)
    if not validate_transcript(transcript):
        return video_title, None

    return video_title, transcript

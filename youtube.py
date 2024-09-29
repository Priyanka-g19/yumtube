import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import os

def extract_video_id(url):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtube\.com\/shorts\/)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title(video_id, api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        else:
            print(f"No video found with id: {video_id}")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_transcript_text(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        all_transcripts = list(transcript_list)
        
        english_transcripts = [t for t in all_transcripts if t.language_code.startswith('en')]
        
        if english_transcripts:
            manual_transcripts = [t for t in english_transcripts if not t.is_generated]
            chosen_transcript = manual_transcripts[0] if manual_transcripts else english_transcripts[0]
            print(f"Using {'manually created' if not chosen_transcript.is_generated else 'automatically generated'} English transcript: {chosen_transcript.language_code}")
            transcript = chosen_transcript.fetch()
        else:
            print(f"No English transcript found. Translating from {all_transcripts[0].language_code} to English")
            transcript = all_transcripts[0].translate('en').fetch()
        
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        print("Unable to process this video. It may not have captions or audio.")
        return None

def validate_transcript(transcript):
    return transcript is not None



def process_youtube_video(url):
    video_id = extract_video_id(url)
    if not video_id:
        print("Invalid YouTube URL.")
        return None, None

    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    video_title = get_video_title(video_id, youtube_api_key)
    
    transcript = get_transcript_text(video_id)
    if not validate_transcript(transcript):
        return video_title, None

    return video_title, transcript
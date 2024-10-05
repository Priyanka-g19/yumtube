import csv
import os
import re
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import pandas as pd

load_dotenv()
# Replace with your own API key

API_KEY =os.getenv("YOUTUBE_API_KEY")

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def extract_video_id(url):
    # Patterns for different YouTube URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:live\/)?(?P<id>[^\s?&\/]+)',
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:shorts\/)?(?P<id>[^\s?&\/]+)',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group('id')
    
    return None  # Return None if no match is found

def get_video_title(video_id):
    try:
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        else:
            return "Video not found or API request failed"
    except Exception as e:
        return f"An error occurred: {str(e)}"

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

def get_transcript(video_id):
    try:
        # Try to get manual English transcripts
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US', 'en'])
    except (NoTranscriptFound, TranscriptsDisabled):
        try:
            # Try to get auto-generated English transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except (NoTranscriptFound, TranscriptsDisabled):
            try:
                # Try to get transcript in any available language and translate to English
                transcript_list = YouTubeTranscriptApi.list_transcripts("HlHKpY3kHmk")
                language_codes = ["af", "ar", "az", "bn", "bs", "ca", "cs", "da", "de", "el", "en", "eo", "es", "et", "eu", "fa", "fi", "fr", "ga", "gl", "gu", "he", "hi", "hr", "hu", "hy", "id", "is", "it", "ja", "jv", "kn", "km", "ko", "la", "lv", "lt", "mk", "ml", "mn", "mr", "ms", "mt", "my", "ne", "nl", "no", "pa", "pl", "ps", "pt", "ro", "ru", "si", "sk", "sl", "sm", "sn", "so", "sq", "sr", "su", "sv", "sw", "ta", "te", "th", "tr", "uk", "ur", "vi", "cy", "xh", "yi", "yo", "zu"]
                transcript_lang = transcript_list.find_transcript(language_codes)
                if transcript_lang.is_translatable:
                    transcript=transcript_lang.translate('en').fetch()
                else:
                    print("Transcript is not translatable")   
            except (TranscriptsDisabled, NoTranscriptFound):
                return "Subtitle not available"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    # If we've reached here, we have a valid transcripttranscript = transcript_list.find_transcript(['de', 'en'])

    # Combine all transcript text
    full_transcript = ' '.join([entry['text'] for entry in transcript])
    return full_transcript

def process_videos(video_urls, output_file):
    file_exists = os.path.isfile(output_file)
    
    with open(output_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new or empty
        if not file_exists or os.path.getsize(output_file) == 0:
            writer.writerow(['Video ID', 'Title', 'Transcript'])
        
        for url in video_urls:
            video_id = extract_video_id(url)
            if video_id:
                title = get_video_title(video_id)
                transcript = get_transcript(video_id)
                writer.writerow([video_id, title, transcript])
                print(f"Processed video: {video_id}")
            else:
                print(f"Invalid URL: {url}")

# def csv_to_dataframe(csv_file):
#     print(pd.read_csv(csv_file))

# Example usage
# video_urls = [
#     # "https://www.youtube.com/watch?v=7bZH9r8c0iE",
#     # "https://youtu.be/KhGDAzF1_rQ",
#     # "https://www.youtube.com/shorts/ZIRZ-XFe2F0",
#     # Add more URLs here
#     "https://www.youtube.com/watch?v=P4i9jKiJZTk"
# ]
# output_file = 'youtube_data.csv'

# process_videos(video_urls, output_file)
# video_id=extract_video_id("https://www.youtube.com/watch?v=P4i9jKiJZTk")
# print(get_transcript("P4i9jKiJZTk"))
# Uncomment the following line if you want to display the CSV as a DataFrame
# csv_to_dataframe(output_file)
# print(f"Data has been appended to {output_file}")
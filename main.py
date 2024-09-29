import os
from dotenv import load_dotenv

# Import functions from youtube.py
from youtube import process_youtube_video

# Import GroqProcessor from LLM.py
from LLM import GroqProcessor

def main():
    # Load environment variables
    load_dotenv()

    # Get YouTube URL from environment variable
    youtube_url = os.getenv('YOUTUBE_URL')
    if not youtube_url:
        print("YOUTUBE_URL is not set in the environment variables.")
        return

    # Process YouTube video and get transcript and title
    video_title, transcript = process_youtube_video(youtube_url)
    
    if not transcript:
        print("Failed to obtain a valid transcript.")
        return

    # Process transcript with GroqProcessor
    processor = GroqProcessor()
    recipe = processor.process_transcript(transcript)

    # Print the result
    if recipe:
        print(f"Video Title: {video_title}")
        print("Recipe Information:")
        print(recipe.model_dump())
    else:
        print("Failed to process the recipe transcript.")

if __name__ == "__main__":
    main()
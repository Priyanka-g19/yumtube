import os
import re
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

# Load environment variables
load_dotenv()

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
            st.error(f"No video found with id: {video_id}")
            return None
    except HttpError as e:
        st.error(f"An HTTP error occurred: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def get_english_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Get all available transcripts
        all_transcripts = list(transcript_list)
        
        # Function to filter English transcripts
        def is_english(transcript):
            return transcript.language_code.startswith('en')
        
        # Get all English transcripts
        english_transcripts = list(filter(is_english, all_transcripts))
        
        if english_transcripts:
            # Prioritize manually created transcripts
            manual_transcripts = [t for t in english_transcripts if t.is_generated is False]
            if manual_transcripts:
                chosen_transcript = manual_transcripts[0]
                st.info(f"Using manually created English transcript: {chosen_transcript.language_code}")
            else:
                chosen_transcript = english_transcripts[0]
                st.info(f"Using automatically generated English transcript: {chosen_transcript.language_code}")
            
            return chosen_transcript.fetch()
        else:
            # If no English transcript, get the first available and translate to English
            st.info(f"No English transcript found. Translating from {all_transcripts[0].language_code} to English")
            return all_transcripts[0].translate('en').fetch()

    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video")
        return None
    except NoTranscriptFound:
        st.error("No transcripts found for this video")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def validate_transcript(transcript):
    if not transcript:
        st.error("Unable to process this video. It may not have captions or audio.")
        return False
    
    total_words = sum(len(entry['text'].split()) for entry in transcript)
    if total_words < 40:
        st.error("The transcript is too short. Please try with a different video.")
        return False
    
    return True

def process_with_groq(transcript, video_title):
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    # Debug: Print the length of the API key (not the key itself)
    st.write(f"Length of GROQ_API_KEY: {len(groq_api_key) if groq_api_key else 'None'}")
    
    if not groq_api_key:
        st.error("Error: GROQ_API_KEY is not set in the .env file.")
        return None

    try:
        client = Groq(api_key=groq_api_key)
        
        system_prompt = """You are an expert chef with extensive knowledge of various cuisines and cooking styles. Given a transcript of a recipe, you should perform the following tasks:

        Ingredient List: Extract and list all ingredients mentioned in the recipe, along with their respective quantities.
        Recipe Method: Break down the cooking process into clear, step-by-step instructions."""

        user_prompt = f"""Video Title: {video_title}

        Transcript:
        {' '.join([entry['text'] for entry in transcript])}

        Based on this transcript, please provide:
        1. A list of ingredients with their quantities
        2. Step-by-step cooking instructions"""

        # Debug: Print that we're about to make the API call
        st.write("Attempting to make Groq API call...")

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.4,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )

        recipe_text = ""
        for chunk in chat_completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                recipe_text += content
                # Update Streamlit with the streaming content
                recipe_placeholder.markdown(recipe_text)

        return recipe_text

    except Exception as e:
        st.error(f"An error occurred while processing with Groq: {str(e)}")
        return None
# Streamlit App

st.set_page_config(page_title="YouTube Recipe Generator", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #f0f0f0;
    }
    .logo {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .logo img {
        width: 100px;
        height: auto;
    }
    .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .search-input {
        width: 60%;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 25px;
        border: 1px solid #ddd;
        outline: none;
        padding-left: 40px;
    }
    .search-icon {
        position: absolute;
        left: 22%;
        color: #888;
    }
    .recipe-text {
        font-family: 'Georgia', serif;
        font-size: 18px;
        line-height: 1.6;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Display small centered logo
st.markdown('<div class="logo"><img src="yumtube_logo.png" alt="YumTube Logo"></div>', unsafe_allow_html=True)

# Create search bar with internal icon
col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.markdown('<div class="search-container"><span class="search-icon">🔍</span><input type="text" class="search-input" placeholder="Enter YouTube URL" id="url-input"></div>', unsafe_allow_html=True)
    url = st.text_input("", key="hidden_input", label_visibility="collapsed")

# Main app logic
if url:
    with st.spinner('Processing your request...'):
        video_id = extract_video_id(url)
        if not video_id:
            st.error("Invalid YouTube URL. Please check and try again.")
        else:
            youtube_api_key = os.getenv('YOUTUBE_API_KEY')
            video_title = get_video_title(video_id, youtube_api_key)
            if not video_title:
                st.error("Failed to retrieve video title. Please check your YouTube API key and try again.")
            else:
                transcript = get_english_transcript(video_id)
                if not validate_transcript(transcript):
                    st.error("Unable to process this video. It may not have captions, audio, or sufficient content.")
                else:
                    recipe_placeholder = st.empty()
                    groq_response = process_with_groq(transcript, video_title)
                    if not groq_response:
                        st.error("Failed to generate a recipe. Please try again or use a different video.")
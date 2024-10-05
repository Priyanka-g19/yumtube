import streamlit as st
from supabase import create_client, Client
from llm_parsing import *
from transcription import *
from database import store_recipe_in_db
import webbrowser
import os
from dotenv import load_dotenv
from streamlit_url_fragment import get_fragment
import urllib.parse

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Global variable to store user session
session = {"user": None}

def sign_in_with_google():
    try:
        # Initiate Google sign-in
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "redirect_to": "http://localhost:8501",  # Redirect back to Streamlit app after login
        })
        # Open a browser for Google login
        webbrowser.open(response.url)
    except Exception as e:
        st.error(f"Error with Google Sign-in: {e}")

def sign_out():
    supabase.auth.sign_out()
    session["user"] = None

def get_user():
    # Fetch the current authenticated user
    return supabase.auth.get_user()

def handle_redirect():
    # Get the URL fragment (part after #)
    fragment = get_fragment()
    st.write("Fragment received:", fragment)  # Debugging line

    if fragment:
        # Parse the fragment into parameters
        params = dict(urllib.parse.parse_qsl(fragment.removeprefix('#')))
        
        # Extract the access token
        access_token = params.get('access_token')
        st.write("Access token found:", access_token)  # Debugging line

        if access_token:
            st.session_state.access_token = access_token
            st.success("Logged in successfully!")

            # Fetch user information using the access token
            user_info = supabase.auth.get_user(access_token)
            if user_info:
                st.session_state.user = user_info  # Store user in session state
                st.write("User info:", user_info)  # Debugging line
            else:
                st.error("Failed to fetch user information.")

def login_page():
    st.title("Login")

    if st.button("Sign in with Google"):
        sign_in_with_google()

def main_page():
    st.title("YouTube Recipe Parser")

    # Input for YouTube URL
    url = st.text_input("Enter YouTube Video URL")

    if st.button("Get Recipe"):
        if url:
            try:
                # Extract video ID and get transcript
                video_id = extract_video_id(url)
                transcribed_text = get_transcript(video_id)

                # Get the recipe from the transcribed text
                recipe = get_recipe(transcribed_text)

                # Display the recipe
                st.subheader(recipe.recipe_name)
                st.write("### Ingredients:")
                for ingredient in recipe.ingredients:
                    st.write(f"- {ingredient.name}: {ingredient.quantity}")

                st.write("### Method:")
                for method in recipe.method_to_prepare:
                    st.write(f"{method.step_number}. {method.instructions}")

                st.write(f"### Servings: {recipe.servings}")

                # Store recipe in database with user ID
                user = st.session_state.get('user')
                if user:
                    store_recipe_in_db(recipe, url, video_id, user.user.id)  # Save with user-specific ID
                    st.success("Recipe saved to your account in the database.")
                else:
                    st.warning("Please log in to save the recipe.")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid YouTube URL.")

def main():
    handle_redirect()  # Handle token and user retrieval

    # Check if the user is in session state
    user = st.session_state.get('user')

    st.write("Current user:", user)  # Debugging line

    if user:
        email = user.user.user_metadata.get('email', 'Unknown')
        st.sidebar.success(f"Logged in as: {email}")
        if st.sidebar.button("Logout"):
            sign_out()
            st.experimental_rerun()

        # Show the main page if logged in
        main_page()
    else:
        # Show login page if not logged in
        login_page()



if __name__ == "__main__":
    main()

import streamlit as st
from streamlit_supabase_auth import login_form
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from supabase import create_client
from youtube import process_youtube_video
from LLM import GroqProcessor
from uuid import UUID
from typing import TypedDict, Optional, Dict
import uuid
import logging
import requests
from st_copy_to_clipboard import st_copy_to_clipboard
from streamlit_feedback import streamlit_feedback
from common import init_session_state, sign_out  # shared session helpers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecipeDB(TypedDict):
    recipe_id: UUID
    user_id: UUID
    recipe_title: str
    recipe: str
    ingredients: str
    serve_quantity: int
    flavour_profile: str
    texture_profile: str
    video_title: str
    youtube_url: str
    created_at: str
    updated_at: str

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    st.error("Supabase URL or anon key not set in environment variables.")
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# -------------------------------------------------------------------------
# Utility functions (translation, video processing, etc.)
# -------------------------------------------------------------------------
def translate_text(input_text: str, target_language_code: str) -> str:
    url = "https://api.sarvam.ai/translate"
    headers = {
        "api-subscription-key": os.getenv("SARVAM_API_KEY"),
        "Content-Type": "application/json"
    }
    payload = {
        "input": input_text,
        "source_language_code": "en-IN",
        "target_language_code": target_language_code,
        "speaker_gender": "Female",
        "mode": "formal",
        "enable_preprocessing": False,
        "output_script": None,
        "numerals_format": "international"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("translated_text", input_text)
    else:
        logger.error(f"Translation API error: {response.status_code} {response.text}")
        return input_text

def translate_section(text: str, target_language_code: str) -> str:
    if len(text) <= 1000:
        return translate_text(text, target_language_code)
    else:
        lines = text.split('\n')
        translated_lines = []
        for line in lines:
            if line.strip():
                translated_lines.append(translate_text(line, target_language_code))
            else:
                translated_lines.append("")
        return "\n".join(translated_lines)

def translate_recipe(recipe_data: Dict, target_language_code: str) -> Dict:
    recipe_data["recipe_title"] = translate_section(recipe_data.get("recipe_title", ""), target_language_code)
    ingredients_lines = recipe_data.get("ingredients", "").split("\n")
    translated_ingredients = []
    for line in ingredients_lines:
        if line.strip():
            translated_ingredients.append(translate_text(line, target_language_code))
        else:
            translated_ingredients.append("")
    recipe_data["ingredients"] = "\n".join(translated_ingredients)
    instructions_lines = recipe_data.get("recipe", "").split("\n")
    translated_instructions = []
    for line in instructions_lines:
        if line.strip():
            translated_instructions.append(translate_text(line, target_language_code))
        else:
            translated_instructions.append("")
    recipe_data["recipe"] = "\n".join(translated_instructions)
    return recipe_data

def process_video(url: str) -> Optional[Dict]:
    video_title, transcript = process_youtube_video(url)
    if not transcript:
        raise ValueError("No transcript available for this video")
    processor = GroqProcessor()
    recipe_output = processor.process_transcript(transcript)
    if not recipe_output:
        raise ValueError("Failed to generate recipe from transcript")
    recipe_data = recipe_output.model_dump()
    recipe_data.update({
        "video_title": video_title,
        "youtube_url": url,
    })
    return recipe_data

def save_recipe_to_db(recipe_data: Dict, user_id: str, access_token: str, refresh_token: str) -> bool:
    try:
        supabase.auth.set_session(access_token, refresh_token)
        current_time = datetime.now(timezone.utc).isoformat()
        db_recipe = {
            "user_id": user_id,
            "recipe_title": recipe_data["recipe_title"],
            "recipe": recipe_data["recipe"],
            "ingredients": recipe_data["ingredients"],
            "serve_quantity": recipe_data["serve_quantity"],
            "flavour_profile": recipe_data["flavour_profile"],
            "texture_profile": recipe_data["texture_profile"],
            "video_title": recipe_data["video_title"],
            "youtube_url": recipe_data["youtube_url"],
            "created_at": current_time,
            "updated_at": current_time,
        }
        response = supabase.table("recipes").insert(db_recipe).execute()
        if not response.data:
            logger.error("No data returned from insert operation")
            return False
        return True
    except Exception as e:
        logger.exception(f"Error saving recipe: {e}")
        st.error(f"Failed to save recipe: {e}")
        return False

def display_recipe(recipe: Dict) -> None:
    st.subheader(recipe.get("recipe_title", ""))
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Video Title:**", recipe.get("video_title", ""))
    with col2:
        st.write("**Servings:**", recipe.get("serve_quantity", ""))
    
    st.write("**Flavor Profile:**", recipe.get("flavour_profile", ""))
    st.write("**Texture Profile:**", recipe.get("texture_profile", ""))
    
    st.write("### Ingredients")
    for ingredient in recipe.get("ingredients", "").split("\n"):
        if ingredient.strip():
            st.write(f"- {ingredient.strip()}")
    
    st.write("### Instructions")
    for idx, step in enumerate(recipe.get("recipe", "").split("\n"), 1):
        if step.strip():
            st.write(f"{idx}. {step.strip()}")
    
    copy_text = f"{recipe.get('recipe_title', '')}\n\n"
    copy_text += "Ingredients:\n"
    for ingredient in recipe.get("ingredients", "").split("\n"):
        if ingredient.strip():
            copy_text += f"- {ingredient.strip()}\n"
    copy_text += "\nInstructions:\n"
    for idx, step in enumerate(recipe.get("recipe", "").split("\n"), 1):
        if step.strip():
            copy_text += f"{idx}. {step.strip()}\n"
    st_copy_to_clipboard(copy_text)

def _submit_feedback(feedback: dict):
    raw_score = feedback.get("score")
    rating_bool = None
    if raw_score is None:
        pass
    elif isinstance(raw_score, bool):
        rating_bool = raw_score
    elif isinstance(raw_score, str):
        score = raw_score.strip().lower()
        if score in ("👍", "up", "1", "true"):
            rating_bool = True
        elif score in ("👎", "down", "0", "false"):
            rating_bool = False
    feedback_data = {
        "feedback_id": str(uuid.uuid4()),
        "rating": rating_bool,
        "detailed_feedback": feedback.get("text", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response = supabase.table("feedback").insert(feedback_data).execute()
    if response.data:
        st.success("Thank you for your feedback!")
    else:
        st.error("Failed to submit feedback. Please try again.")
    return feedback_data

# ----------------------------------------------------------------------------
# Main App
# ----------------------------------------------------------------------------
def main() -> None:
    init_session_state()
    
    # Top logo and title
    try:
        st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
        st.image("logo_img/app_logo.png", width=200)
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading main logo: {e}")

    st.title('YumTube')
    # Sidebar: Authentication and additional links
    with st.sidebar:
        if st.session_state.session is None:
            if st.button("Sign In"):
                st.session_state.show_login = True
        else:
            if st.button("Sign Out", key="signout-btn"):
                sign_out()
                st.rerun()
        
        if st.session_state.get("show_login", False) and st.session_state.session is None:
            with st.expander("Sign In", expanded=True):
                session = login_form(
                    url=SUPABASE_URL,
                    apiKey=SUPABASE_ANON_KEY,
                    providers=["google"],
                )
                if session:
                    st.session_state.session = session
                    st.session_state.show_login = False
                    st.rerun()
        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-weight: bold;'>Powered by</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            try:
                with open("logo_img/GroqLogo_Black.svg", "r", encoding="utf-8") as f:
                    svg1 = f.read()
                st.markdown(f'<div style="width:80px; margin: 0 auto;">{svg1}</div>', unsafe_allow_html=True)
            except Exception:
                st.write("Logo error")
        with col2:
            try:
                st.image("logo_img/supabase-logo-wordmark--light.png", width=80)
            except Exception:
                st.write("Image error")
        with col3:
            try:
                st.image("logo_img/sarvam-logo.jpg", width=80)
            except Exception:
                st.write("Image error")
        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-weight: bold;'>Connect with us</p>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center;">
                <a href="https://www.linkedin.com/in/sagar-pandey-821927171" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" 
                         style="height: 30px; margin: 5px;">
                </a>
                <a href="https://linkedin.com/in/priyanka-gupta-b193a1212" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" 
                         style="height: 30px; margin: 5px;">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-weight: bold;'>Learn More About This App</p>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center;">
                <a href="https://github.com/Priyanka-g19/yumtube" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" 
                         style="height: 30px; margin: 5px;">
                </a>
                <a href="https://medium.com/@priyanka.dataian/yumtube-your-ai-powered-recipe-assistant-from-youtube-videos-a07966886bb5" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111505.png" 
                        style="height: 30px; margin: 5px;">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Translation language selection
    translation_options = [
        "Do not translate", "Hindi", "Bengali", "Gujarati", "Kannada",
        "Malayalam", "Marathi", "Odia", "Punjabi", "Tamil", "Telugu"
    ]
    st.session_state.selected_language = st.selectbox(
        "Select translation language",
        translation_options,
        index=0,
        help="Choose a language to translate the recipe. Only the recipe title, ingredients, and instructions will be translated."
    )
    
    # URL input for generating a recipe
    if st.session_state.get("search_visible", True):
        youtube_url = st.text_input(
            "Enter YouTube URL",
            key="youtube_url",
            help="Paste a YouTube cooking video URL to generate a recipe"
        )
        if st.button("Generate Recipe"):
            if not youtube_url:
                st.warning("Please enter a YouTube URL")
            else:
                st.session_state.search_visible = False
                with st.spinner("Processing video and generating recipe..."):
                    try:
                        recipe_data = process_video(youtube_url)
                        if st.session_state.selected_language != "Do not translate":
                            language_codes = {
                                "Hindi": "hi-IN",
                                "Bengali": "bn-IN",
                                "Gujarati": "gu-IN",
                                "Kannada": "kn-IN",
                                "Malayalam": "ml-IN",
                                "Marathi": "mr-IN",
                                "Odia": "od-IN",
                                "Punjabi": "pa-IN",
                                "Tamil": "ta-IN",
                                "Telugu": "te-IN"
                            }
                            target_code = language_codes.get(st.session_state.selected_language)
                            recipe_data = translate_recipe(recipe_data, target_code)
                        st.session_state.current_recipe = recipe_data
                        st.session_state.recipe_generated = True
                    except Exception as e:
                        st.error(str(e))
                        st.session_state.processing_error = str(e)
                        st.session_state.search_visible = True
    
    # Display generated recipe if available
    if st.session_state.get("recipe_generated") and st.session_state.get("current_recipe"):
        display_recipe(st.session_state.current_recipe)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate New Recipe"):
                st.session_state.search_visible = True
                st.session_state.recipe_generated = False
                st.session_state.current_recipe = None
                st.rerun()
        with col2:
            if st.session_state.session is None:
                st.info("Please sign in to save recipes")
            elif st.button("Save Recipe"):
                user_id = st.session_state.session["user"]["id"]
                access_token = st.session_state.session["access_token"]
                refresh_token = st.session_state.session["refresh_token"]
                if save_recipe_to_db(st.session_state.current_recipe, user_id, access_token, refresh_token):
                    st.success("Recipe saved successfully!")
                    # Navigate to the recipes page
                    st.experimental_set_query_params(page="Yummy_Recipes")
                    st.rerun()
                else:
                    st.error("Failed to save recipe. Please try again.")
    
    if st.session_state.session is None:
        st.info("Sign in to save recipes to your collection!")
    
    # Feedback section
    st.markdown("---")
    st.subheader("Feedback")
    with st.container():
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        _ = streamlit_feedback(
            feedback_type="thumbs",
            optional_text_label="Would love to hear from you",
            review_on_positive=True,
            on_submit=_submit_feedback,
            key="feedback_component",
            align="center"
        )
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

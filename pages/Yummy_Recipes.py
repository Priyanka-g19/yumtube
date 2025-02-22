import streamlit as st
from streamlit_supabase_auth import login_form
import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime
import dateutil.parser
from st_copy_to_clipboard import st_copy_to_clipboard
from youtube import extract_video_id
import uuid
from common import init_session_state, sign_out  # shared session helpers

# Inject custom CSS for styling.
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #FFC107;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        margin: 5px;
    }
    div.stButton > button:hover {
        background-color: #FFB300;
    }
    /* Sign Out button styled in red */
    div.stButton > button#signout-btn {
        background-color: red !important;
    }
    div.stButton > button#signout-btn:hover {
        background-color: darkred !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load environment variables.
load_dotenv()

# Initialize Supabase client.
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

RECIPES_PER_PAGE = 10

def initialize_pagination_state():
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1

def get_user_recipes(user_id, page_number, recipes_per_page, access_token, refresh_token):
    try:
        supabase.auth.set_session(access_token, refresh_token)
        start = (page_number - 1) * recipes_per_page
        end = start + recipes_per_page - 1
        response = supabase.table('recipes') \
            .select('*', count='exact') \
            .eq('user_id', user_id) \
            .order('created_at', desc=True) \
            .range(start, end) \
            .execute()
        total_recipes = response.count if response.count is not None else 0
        return response.data, total_recipes
    except Exception as e:
        st.error(f"Error fetching recipes: {str(e)}")
        return [], 0


def parse_datetime(datetime_str):
    try:
        return dateutil.parser.parse(datetime_str)
    except Exception:
        return None

def display_recipe_card(recipe):
    formatted_recipe = f"**Recipe Title:** {recipe.get('recipe_title', '')}\n\n"
    formatted_recipe += f"**Video Title:** {recipe.get('video_title', '')}\n\n"
    formatted_recipe += f"**Servings:** {recipe.get('serve_quantity', '')}\n\n"
    formatted_recipe += f"**Flavor Profile:** {recipe.get('flavour_profile', 'N/A')}\n\n"
    formatted_recipe += f"**Texture Profile:** {recipe.get('texture_profile', 'N/A')}\n\n"
    formatted_recipe += "### Ingredients:\n"
    ingredients = recipe.get('ingredients', "").split('\n') if isinstance(recipe.get('ingredients', ""), str) else recipe.get('ingredients', [])
    for ingredient in ingredients:
        if ingredient.strip():
            formatted_recipe += f"- {ingredient.strip()}\n"
    formatted_recipe += "\n### Instructions:\n"
    instructions = recipe.get('recipe', "").split('\n') if isinstance(recipe.get('recipe', ""), str) else recipe.get('recipe', [])
    for idx, instruction in enumerate(instructions, 1):
        if instruction.strip():
            formatted_recipe += f"{idx}. {instruction.strip()}\n"

    
    expander_label = f"📝 {recipe.get('recipe_title', '')}"
    
    with st.expander(expander_label):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Video Title:**", recipe.get('video_title', ''))
            if recipe.get('youtube_url'):
                st.write("[Watch Video](%s)" % recipe.get('youtube_url'))
        with col2:
            st.write("**Servings:**", recipe.get('serve_quantity', ''))
            created_at = parse_datetime(recipe.get('created_at', ''))
            if created_at:
                st.write("**Created:**", created_at.strftime('%Y-%m-%d'))
            else:
                st.write("**Created:** Date unavailable")
        st.write("**Flavor Profile:**", recipe.get('flavour_profile', 'N/A'))
        st.write("**Texture Profile:**", recipe.get('texture_profile', 'N/A'))
        st.write("### Ingredients")
        for ingredient in ingredients:
            if ingredient.strip():
                st.write(f"- {ingredient.strip()}")
        st.write("### Instructions")
        for idx, instruction in enumerate(instructions, 1):
            if instruction.strip():
                st.write(f"{idx}. {instruction.strip()}")
        st_copy_to_clipboard(formatted_recipe)

def display_pagination(total_recipes):
    total_pages = max((total_recipes + RECIPES_PER_PAGE - 1) // RECIPES_PER_PAGE, 1)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.page_number > 1:
            if st.button("← Previous"):
                st.session_state.page_number -= 1
                st.rerun()
    with col2:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")
    with col3:
        if st.session_state.page_number < total_pages:
            if st.button("Next →"):
                st.session_state.page_number += 1
                st.rerun()

def main() -> None:
    init_session_state()
    initialize_pagination_state()
    st.title("My Recipes")
    
    # Authentication: Check session state
    if st.session_state.session is None:
        with st.sidebar:
            st.warning("Please sign in to view your recipes")
            if st.button("Sign In"):
                st.session_state.show_login = True
            if st.session_state.get("show_login", False) and st.session_state.session is None:
                with st.expander("Sign In", expanded=True):
                    session = login_form(
                        url=os.getenv("SUPABASE_URL"),
                        apiKey=os.getenv("SUPABASE_ANON_KEY"),
                        providers=["google"],
                    )
                    if session:
                        st.session_state.session = session
                        st.session_state.show_login = False
                        st.rerun()
        st.stop()
    
    # Sidebar logo
    with st.sidebar:
        try:
            st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
            st.image("logo_img/app_logo.png", width=200)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.sidebar.error(f"Error loading sidebar logo: {e}")
    
    try:
        recipes, total_recipes = get_user_recipes(
            st.session_state.session['user']['id'],
            st.session_state.page_number,
            RECIPES_PER_PAGE,
            st.session_state.session['access_token'],
            st.session_state.session['refresh_token']
        )
        
        if not recipes:
            st.info("You haven't saved any recipes yet!")
            if st.button("Create your first recipe", key="create_recipe_btn"):
                st.switch_page("YumTube.py")
                # st.rerun()
        else:
            st.write(f"Total {total_recipes} recipe{'s' if total_recipes != 1 else ''}")
            for recipe in recipes:
                display_recipe_card(recipe)
            
            if total_recipes > RECIPES_PER_PAGE:
                display_pagination(total_recipes)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Refresh page"):
            st.rerun()

if __name__ == "__main__":
    main()

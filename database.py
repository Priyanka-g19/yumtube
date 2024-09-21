from supabase import create_client, Client
from dotenv import load_dotenv
import os
from llm_parsing import Recipe

load_dotenv()

def connect_to_db():
    url = os.getenv("SUPABASE_URL")
    key =  os.getenv("SUPABASE_KEY")
    return create_client(url, key)

# # Fetch data from a table
# data = supabase.table('recipe').select('*').execute()
# print(data)

def store_recipe_in_db(recipe: Recipe, video_url: str, video_id: str):
    supabase: Client = connect_to_db()
    # Prepare recipe data for insertion
    recipe_data = {
        "recipe_title": recipe.recipe_name,
        "ingredients": [{"name": ing.name, "quantity": ing.quantity} for ing in recipe.ingredients],
        "method_to_prepare": [{"step_number": step.step_number, "instructions": step.instructions} for step in recipe.method_to_prepare],
        "servings": recipe.servings,
        "video_url": video_url,
        "video_id": video_id
    }
    # Insert into your Supabase table
    response = supabase.table("recipe").insert(recipe_data).execute()
    print(response)

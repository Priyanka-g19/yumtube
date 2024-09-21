from llm_parsing import *
from database import *
from transcription import *



def generator(url):
    try:
        video_id=extract_video_id(url)
        transcribed_text=get_transcript(video_id)
        print(transcribed_text)
        json_recipe=get_recipe(transcribed_text)
        structured_recipe=print_recipe(json_recipe)
        store_recipe_in_db(json_recipe, url,video_id)
        return structured_recipe
            
    except Exception as e:
        raise e    


generator("https://www.youtube.com/watch?v=HlHKpY3kHmk")
import os
import json
import logging
from pydantic import BaseModel, ValidationError
from groq import Groq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecipeOutput(BaseModel):
    recipe_title: str
    recipe: str
    ingredients: str
    serve_quantity: int
    flavour_profile: str
    texture_profile: str

class GroqProcessor:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        self.client = Groq(api_key=self.api_key)

    def process_transcript(self, transcript: str) -> RecipeOutput | None:
        prompt = {
            "role": "user",
            "content": (
                "You are an expert culinary analyst with strong expertise in recipe dissection and culinary writing. "
                "Your task is to analyze the following detailed recipe transcript and extract key information with a clear, structured output. "
                "Please follow these instructions carefully and think step by step before providing your final answer:\n\n"
                "1. **Recipe Title:** Create a concise title that combines the main ingredients with the primary cooking method.\n"
                "2. **Ingredients:** Extract a complete, newline-separated list of ingredients, each with the exact quantities mentioned.\n"
                "3. **Cooking Steps:** Break down the cooking process into detailed, sequential steps (each step on a new line).\n"
                "4. **Servings:** Identify the number of servings the recipe yields.\n"
                "5. **Flavor Profile:** Determine the dominant flavors (e.g., SWEET, SALTY, SOUR, BITTER, UMAMI, or combinations).\n"
                "6. **Texture Profile:** Describe the expected texture (e.g., CRISPY, CRUNCHY, TENDER, etc.).\n\n"
                "Ensure that your response is provided strictly in valid JSON format with exactly the following keys:\n\n"
                "{\n"
                '    "recipe_title": <string>,\n'
                '    "ingredients": <string>,    // each ingredient on a new line\n'
                '    "recipe": <string>,         // each step on a new line\n'
                '    "serve_quantity": <number>,\n'
                '    "flavour_profile": <string>,\n'
                '    "texture_profile": <string>\n'
                "}\n\n"
                "Do not include any additional commentary or keys. "
                "Now, analyze the recipe transcript provided below and output your final answer in the specified JSON format.\n\n"
                "### Recipe Transcript:\n"
                f"{transcript}"
            )
        }


        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert chef analyzing recipe transcripts."},
                    prompt
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=1024,
                # Force the model to return a valid JSON object:
                response_format={"type": "json_object"}
            )

            if not response.choices:
                logger.error("No choices returned from API.")
                return None

            message_content = response.choices[0].message.content.strip()
            if not message_content:
                logger.error("Empty message content returned from API.")
                return None

            logger.debug(f"Raw API response content: {message_content}")
            recipe_data = json.loads(message_content)
            return RecipeOutput(**recipe_data)

        except (json.JSONDecodeError, KeyError, ValidationError) as e:
            logger.error(f"Error processing recipe: {e}")
            logger.debug(f"Raw API response content on error: {response.choices[0].message.content if response.choices else 'N/A'}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

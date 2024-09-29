import os
from typing import List, Optional
from pydantic import BaseModel, Field
from groq import Groq
import json


class Recipe(BaseModel):
    recipe_info: List[str] = Field(..., description="Complete recipe information including ingredients, instructions, serving size, and flavor profile")

    class Config:
        from_attributes = True  # This replaces the old 'orm_mode = True'
        
class GroqProcessor:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment variables.")
        self.client = Groq(api_key=self.api_key)

    def process_transcript(self, transcript: str) -> Optional[Recipe]:
        prompt_template = """
        ### INSTRUCTION ###
        You are a highly skilled chef with deep expertise in diverse cuisines and cooking techniques. Your task is to analyze a recipe transcript and provide all information in a single list format. Include the following:

        1. Start with "INGREDIENTS:" and list all ingredients with their quantities.
        2. Then add "INSTRUCTIONS:" and provide step-by-step cooking instructions.
        3. Add "SERVES:" and state how many people the recipe serves. If not specified, state "No serving size provided."
        4. Finally, add "FLAVOR PROFILE:" and describe the overall flavor of the dish.

        ### FORMAT INSTRUCTIONS ###
        Provide the output as a JSON array of strings, where each string is a separate piece of information. For example:
        [
            "INGREDIENTS:",
            "2 cups all-purpose flour",
            "1 tsp baking powder",
            ...,
            "INSTRUCTIONS:",
            "1. Preheat the oven to 350°F (175°C).",
            "2. In a large bowl, mix the dry ingredients.",
            ...,
            "SERVES: 4 people",
            "FLAVOR PROFILE: Rich and savory with a hint of sweetness"
        ]

        DO NOT add any text before or after the JSON array.

        ### CONTEXT ###
        {transcript}
        """

        attempt = 0
        max_attempts = 3

        while attempt < max_attempts:
            attempt += 1
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert chef analyzing recipe transcripts."},
                        {"role": "user", "content": prompt_template.format(transcript=transcript)}
                    ],
                    model="mixtral-8x7b-32768",
                    temperature=0.4,
                    max_tokens=1024
                )
                recipe_data = json.loads(chat_completion.choices[0].message.content)
                
                return Recipe(recipe_info=recipe_data)
            except Exception as e:
                print(f"Attempt {attempt}: An error occurred. {str(e)} Retrying...")

        return Recipe(recipe_info=["Error: Unable to process recipe"])

# Usage
processor = GroqProcessor()
recipe = processor.process_transcript("Your recipe transcript here...")
print(json.dumps(recipe.model_dump(), indent=2))

# For Supabase storage (pseudo-code)
# supabase.table('recipes').insert({
#     'recipe_data': recipe.dict()
# })
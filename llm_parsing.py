from typing import List, Optional,Union, Dict, Any
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, Field
from groq import Groq

load_dotenv()

groq = Groq(
    # This is the default and can be omitted
    api_key=os.getenv("GROQ_API_KEY"),
)


# Data model for LLM to generate
class Ingredient(BaseModel):
    name: str
    quantity: str

class Method(BaseModel):
    step_number: int
    instructions: str



class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[Ingredient]
    method_to_prepare: List[Method]
    servings: Optional[str]=Field(default=None)




def get_recipe(transcribed_text: str)-> Recipe:
    try:
        chat_completion = groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a expert chef . You will be given the transcript of the food recipe video. You task is to extract the  recipe name, its ingredients with quantity, and the explain the method to prepare in detail like a chef. Also, provide the number for how much people can be served.\n"
                    # Pass the json schema to the model. Pretty printing improves results.
                    # f" The JSON object must use the schema: {json.dumps(Recipe.model_json_schema(), indent=2)}",
                    
                ''' Please generate a recipe in JSON format using the following structure:\n

    {
    "recipe_name": "string",
    "ingredients": [
        {
        "name": "string",
        "quantity": "string or number"
        }
    ],
    "method_to_prepare": [
        {
        "step_number": integer,
        "instructions": "string"
        }
    ],
    "servings": "number or string"
    }

    Please ensure the quantity field is either a number (for specific measurements) or a string (like 'some', 'a pinch', etc.), but it should follow a reasonable format. Also, ensure the method steps have clear step numbers and detailed instructions. if avilable give the servings as approximate number of number ina range"

    **For example:**
    {
    "recipe_name": "Pav Bhaji",
    "ingredients": [
    {"name": "Kashmiri chillies", "quantity": "6 (or as needed for color)"},
    {"name": "Garlic", "quantity": "6-7 cloves"},
    {"name": "Salt", "quantity": "a pinch (to taste)"},
    {"name": "Butter", "quantity": "1 tablespoon (or as desired)"},
    {"name": "Pav Bhaji masala", "quantity": "1/2 teaspoon"},
    {"name": "Carrots", "quantity": "1 small carrot (or as preferred)"},
    {"name": "Beetroot", "quantity": "1/2 (or as preferred)"},
    {"name": "Cauliflower", "quantity": "150 grams"},
    {"name": "Potatoes", "quantity": "3 medium-sized"},
    {"name": "Green peas", "quantity": "1/2 cup"},
    {"name": "Onions", "quantity": "2 medium-sized"},
    {"name": "Capsicum", "quantity": "1 large"},
    {"name": "Tomatoes", "quantity": "4 medium-sized"},
    {"name": "Turmeric", "quantity": "1/2 teaspoon"},
    {"name": "Chilly powder", "quantity": "1 teaspoon"},
    {"name": "Coriander powder", "quantity": "1.5 teaspoons"},
    {"name": "Coriander leaves", "quantity": "a handful (or to taste)"},
    {"name": "Lime juice", "quantity": "juice of 1 lime"},
    {"name": "Bread", "quantity": "as needed (normal or spicy)"},
    {"name": "Oil", "quantity": "1 teaspoon"}
    ],
    "method_to_prepare": [
    {"step_number": 1, "instructions": "Soak Kashmiri chillies in warm water for 3 hours. Add 1-2 spoons of this water to churn easily. Add 6-7 cloves of garlic. Add a pinch of salt and churn it smooth."},
    {"step_number": 2, "instructions": "Pressure cook the veggies. Add 1/2 teaspoon of Pav Bhaji masala, some salt and 1 cup of water. Cook till 3-4 whistles."},
    {"step_number": 3, "instructions": "Heat 1 tablespoon of butter in a pan. Add 1 teaspoon oil to avoid butter from burning. Add 1 teaspoon cumin, dried fenugreek leaves, and fry for 1 minute. Add finely chopped onions and fry for 2 minutes. Add capsicum and fry for 1 minute."},
    {"step_number": 4, "instructions": "Add 1/2 teaspoon turmeric, 1 teaspoon chilly powder, 1.5 teaspoons coriander powder, and 1 teaspoon Pav Bhaji masala. Add some salt and mix well."},
    {"step_number": 5, "instructions": "Add the chutney made earlier and mix well. Cook on medium flame for 5 minutes."},
    {"step_number": 6, "instructions": "Mash the cooked veggies and add them to the tomato base. Mix well and cook for 5 minutes more."},
    {"step_number": 7, "instructions": "Add 1/2 cup water to the Bhaji and cook for 5 minutes more. Add coriander leaves and lime juice. Mix well and turn off heat."}
    ],
    "servings": 1
    }'''

                },
                {
                    "role": "user",
                    "content": f"Give recipe in given structured format from the transcribed text:  {transcribed_text}",
                },
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            # Streaming is not supported in JSON mode
            stream=False,
            # Enable JSON mode by setting the response format
            response_format={"type": "json_object"},
        )

        raw_response = chat_completion.choices[0].message.content
        response_dict = json.loads(raw_response)
        if "servings" not in response_dict:
            response_dict["servings"] = None
        return Recipe.parse_obj(response_dict)
        
        # response_dict: Dict[str, Any] = json.loads(raw_response)
        # print("response_dict",response_dict)
        # print( Recipe.parse_obj(response_dict))
    
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    


def print_recipe(recipe: Recipe):
    print("Recipe:", recipe.recipe_name)

    print("\nIngredients:")
    for ingredient in recipe.ingredients:
        print(
            f"- {ingredient.name}: {ingredient.quantity}"
        )
    print("\nMethod:")
    for  method in recipe.method_to_prepare:
        print(f"{method.step_number}. {method.instructions}")   

    print("\nServings:", recipe.servings)     

# print(json.dumps(Recipe.model_json_schema(), indent=2))

# text='''Like Vada Pav is famous in Mumbai, in the same way is Pav Bhaji. Sometimes we feel making Pav Bhaji is very difficult & its a long process. But trust me its not like that, I am making Pav Bhaji today, that too in a quick way It will be ready in 15 mins. I am starting to make Pav Bhaji & in this there are basically 3 steps. In the first step, I will be making Garlic Chutney. Second step is to  pressure cook the veggies. Finally I will make Pav Bhaji. For making Garlic Chutney we just need 3 ingredients. Here I have taken Kashmiri chillies, & soaked it in warm water for 3 hrs. Here I have garlic. I have taken 6 Kashmiri chillies. This will give a good colour to the Pav Bhaji. I am adding about 1-2 spoons of this water to churn easily. I am adding 6-7 cloves of garlic. Add little salt & churn it smooth. Chutney has churned. You can see it has got a nice bright red colour. I will transfer this into a plate. Now its time for the 2nd step. This is to boil veggies. Here I have approx 150 gms cauliflower,  a small carrot, & half beetroot. I have cut all the veggies into small pieces. This is 3 medium sized potatoes. I have peeled & cut it & finally add 1/2 cup green peas. Here I am using frozen but if you have fresh you can use them too. When boiling veggies, I am adding about 1/2 spoon of Pav Bhaji masala. This gives a very good flavour to the veggies. So add 1/2 tsp Pav Bhaji masala. But you can boil the veggies even without it. Add some salt too. Add about 1 cup of water. And cook till 3-4 whistles. Close the lid, keep on medium flame and cook till 3-4 whistles. Pav Bhaji tastes best in butter so veggies quantity I have taken, I am taking 1 tbsp butter. Add about 1 tsp oil to avoid butter from burning. On heating add 1 tsp cumin. Add dried fenugreek leaves in butter. This gives good aroma to the Pav Bhaji. And it tastes good when eating too. Here you can see I have finely chopped onions. I have taken 2 medium sized onions. First I will fry them.  After frying onions for just 2 mins add capsicum, I have taken 1 very big sized capsicum. When making Pav Bhaji never avoid capsicum, it tastes good in Pav Bhaji. Here I have 1/2 tsp turmeric, 1 tsp chilly powder & 1.5 tsp coriander powder. Again I am adding about 1 tsp Pav Bhaji masala. Add some salt, make sure to add little salt as we have added in veggies & chutney too. Onion and capsicum are soft, time to add tomatoes. I have taken medium size 4 tomatoes finely chopped. Now add the chutney we had made. Mix well and cook on medium flame for 5 mnts. Pav Bhaji is ready. Lets check the cooker. With the help of a masher, mash the veggies before adding in the pan. Now add this mashed veggies in tomato base. Lets mash Pav Bhaji well as it tastes good when all ingredients are mixed & with smooth mushy texture. If there are whole veggies like capsicum, onion, tomato or peas, it doesnt taste good. And water stays separated if veggies are whole and not mushy. Its smelling so good, I feel to eat right away. Pav Bhaji is almost ready, but its consistency is thick. So add 1/2 cup water. And let it cook again for 5 mnts more. Its been 5 mnts and Bhaji is ready. Lastly add lots of coriander leaves. Turn off heat and add 1 lime juice. Mix well. Now its time to toast the bread. Take butter in a pan. You can enjoy this tasty Bhaji with normal bread. But if you get spicy bread, then it tastes really good. Now sprinkle 1/2 tsp Pav Bhaji masala when butter melts. Add some coriander leaves. Take 2 Pav and cut in centre like this. Place it on the butter and press gently. Lets plate hot Bhaji. Also place spicy Pav and chopped onion on the side. Because Pav Bhaji doesnt taste good wihtout onion. Garnish with finely chopped onion and some coriander leaves on the Bhaji .
# S
# 57
# 00:07:08,000 --> 00:07:10,000
# Lastly place butter. Its so delicious and tasty. Must, Must, Must Try recipe is this.'''
# print(get_recipe(text))
# print_recipe(recipe)


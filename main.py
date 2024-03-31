from fastapi import FastAPI, HTTPException
import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Initialize the client once
clientTogether = openai.OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=os.environ['TOGETHER_API_KEY'],
)
tools = [
  {
    "type": "function",
    "function": {
      "name": "analyze_property",
      "description": "Analyze and extract information from a real estate listing description",
      "parameters": {
        "type": "object",
         "properties": {
        "RenovatedRecently": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Has the property undergone any significant recent renovations?"},
        "NewBuild": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Is the property described as being newly built (within the last 5 years)?"},
        "ModernAppliances": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property listing mention a modern kitchen with contemporary design and up-to-date appliances?"},
        "ExtraSpaces": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property contain additional spaces, such as a home office, gym, or finished basement?"},
        "OutdoorAmenities": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Are there any details about outdoor features such as a deck, pool, or garden?"},
        "InvestorReady": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property suggest it could generate income or potentially be a good investment opportunity?"},
        "ModernKitchen": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property mention a kitchen with modern features?"},
        "UltraLuxuriousRenovation": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Are there references to high-end renovations, use of premium materials, or unique design features?"},
        "PrivateFeatures": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property mention private features like a fenced yard or ensuite bathrooms?"},
        "EcoFriendly": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Is there any mention of eco-friendly or energy-efficient features?"},
        "MoveInReady": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Is the property described as ready to move into without needing immediate renovations or improvements?"},
        "FixerUpper": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property suggest that it's a fixer-upper or mention the need for renovations or improvements?"},
        "AsIs": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Is the property being sold 'as is', implying that future repairs or improvements may be necessary?"},
        "OutdoorSpace": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property mention features like a balcony, terrace, or similar outdoor areas?"},
        "LuxuryFeatures": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Are luxury features such as a wine fridge, hot tub, or custom cabinetry mentioned?"},
        "NearbyAmenities": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property mention proximity to local amenities like shops, restaurants, or other facilities?"},
        "ConvenientLocation": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Is the property described as being in a convenient location with easy access to public transport or main roads?"},
        "LargeGarage": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Does the property have a garage that can accommodate multiple cars?"},
        "FirstTimeBuyerFriendly": {"type": "string", "enum": ["yes", "no", "maybe"], "description": "Is the property described in a way that suggests it would be suitable for first-time home buyers?"}
    },
    "required": [
        "RenovatedRecently", "NewBuild", "ModernAppliances", "ExtraSpaces",
        "OutdoorAmenities", "InvestorReady", "ModernKitchen", "UltraLuxuriousRenovation",
        "PrivateFeatures", "EcoFriendly", "MoveInReady", "FixerUpper", "AsIs",
        "OutdoorSpace", "LuxuryFeatures", "NearbyAmenities", "ConvenientLocation",
        "LargeGarage", "FirstTimeBuyerFriendly"
    ]      },
    }
  }
] 

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to SmartBids server!"}


@app.post("/analyze-property/")
async def analyze_property(description: str):
    try:
        messages = [{"role": "system", "content": "You are an assistant specialized in analyzing and extracting data from residential property listing descriptions."},
                    {"role": "user", "content": f"Analyze the provided residential property listing description and provide info about the property. You may respond with either yes, no or maybe. If you are unsure, respond with maybe. \nListing Description:\n{description}\n"}]
        response = clientTogether.chat.completions.create(
                    model='mistralai/Mixtral-8x7B-Instruct-v0.1',
                    messages=messages,
                    temperature=0.0,
                    tool_choice={"type": "function", "function": {"name": "analyze_property"}})
        out = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
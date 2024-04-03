system = """You are a helpful assistant specialized in analyzing residential property listing descriptions. You represent the typical preferences and standards of the average Western consumer in 2024. Analyze the provided residential property listing description and provide information based on the specific questions asked by the user in valid JSON format (pretty printed). Think critically before providing a final answer. Only respond in this valid JSON format:
{
  "RenovatedRecently": {
    "reasoning": "The listing does not mention any recent renovations.",
    "answer": "no"
  },
  ...
  "FirstTimeBuyerFriendly": {
    "reasoning": "The listing mentions that the property is suitable for first-time home buyers.",
    "answer": "yes"
  }
}
"""

def make_prompt(desc):
  prompt = f"""Real Estate Listing Description:
{desc}

Questions:
RenovatedRecently: Has the property undergone any significant recent renovations?
NewBuild: Is the property described as being newly built within the last 5 years (as of 2024)?
ModernAppliances: Does the property mention having modern kitchen appliances?
ExtraSpaces: Does the property contain additional spaces, such as a home office, gym, or finished basement?
OutdoorAmenities: Are there details about outdoor features like a deck, pool, or garden?
InvestorReady: Does the property suggest it could generate income or be a good investment opportunity?
ModernKitchen: Does the property mention a kitchen with modern features such as updated appliances, contemporary design, or ample storage space?
UltraLuxuriousRenovation: Are there references to high-end renovations, use of premium materials, or unique design features?
PrivateFeatures: Does the property mention private features like a fenced yard or ensuite bathrooms?
EcoFriendly: Is there any mention of eco-friendly or energy-efficient features?
MoveInReady: Is the property described as ready to move into without needing immediate renovations or improvements?
FixerUpper: Does the property suggest that it's a fixer-upper or mention the need for renovations or improvements?
AsIs: Is the property being sold 'as is', meaning the buyer accepts the property in its current condition without guarantees?
OutdoorSpace: Does the property mention features like a balcony, terrace, or similar outdoor areas?
LuxuryFeatures: Are luxury features such as a wine fridge, hot tub, custom cabinetry, or other high-end amenities mentioned in the listing?
NearbyAmenities: Does the property mention proximity to local amenities like shops, restaurants, or other facilities?
ConvenientLocation: Is the property described as being in a convenient location with easy access to public transport or main roads?
LargeGarage: Does the property have a garage that can accommodate 2 or more cars?
FirstTimeBuyerFriendly: Is the property described in a way that suggests it would be suitable for first-time home buyers?

Instructions:
Your task is to analyze the provided real estate listing description and answer a series of questions based on the information given. For each question, it is crucial to engage in careful reasoning and analysis of the listing description before providing your answer. Your responses should be based solely on the details mentioned in the listing description.

For each question, select "yes," "no," or "maybe" as your answer. Provide a brief explanation (1-2 sentences) for your choice, demonstrating your thought process and how you arrived at your conclusion. If the description does not provide enough information for a definitive answer, or if the details are ambiguous, respond with "maybe."

Response Output Format Guide:
Format your responses in valid, pretty-printed JSON. Each question should correspond to a JSON object containing two keys: "reasoning" and "answer." The "reasoning" key should contain your brief explanation, highlighting your critical thinking process, and the "answer" key should contain your final answer ("yes," "no," or "maybe").

Example output:
{{
  "RenovatedRecently": {{
    "reasoning": "The listing mentions some recent repairs and updates, but it's unclear if these qualify as significant renovations.",
    "answer": "maybe"
  }},
  "NewBuild": {{
    "reasoning": "The build year of the property is 2023, so it's a new build.",
    "answer": "yes"
  }},
  ...
  "FirstTimeBuyerFriendly": {{
    "reasoning": "The property is ultraluxurious and expensive and is not suitable for first-time buyers.",
    "answer": "no"
  }}
}}
"""
  return prompt


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
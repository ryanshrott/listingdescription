from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
import json
load_dotenv()
from pydantic import BaseModel
from prompts import tools, system, make_prompt
from groq import Groq

app = FastAPI()

# Initialize the client once
clientTogether = openai.OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=os.environ['TOGETHER_API_KEY'],
)
clientGroq = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to SmartBids server!"}

# Define the request model
class PropertyDescription(BaseModel):
    description: str

# Security scheme for bearer token
security = HTTPBearer()

def validate_token(auth: HTTPAuthorizationCredentials = Security(security)):
    if auth.scheme != "Bearer" or auth.credentials != os.getenv("BEARER_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return

def make_groq_request(description):
    response = clientGroq.chat.completions.create(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": make_prompt(description)}
        ],
        model="mixtral-8x7b-32768",
        temperature=0.0,
        max_tokens=3000,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

@app.post("/analyze-description/")
async def analyze_description(request: PropertyDescription, token: str = Depends(validate_token)):
    try:
        groq_output = make_groq_request(request.description)
        try:
            parsed_output = json.loads(groq_output.choices[0].message.content)
            return parsed_output
        except json.JSONDecodeError as json_error:
            return {"error": "Invalid JSON response from Groq", "response": groq_output.choices[0].message.content, "json_error": str(json_error)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-property-simple/")
async def analyze_property_simple(request: PropertyDescription, token: str = Depends(validate_token)):
    try:
        messages = [{"role": "system", "content": "You are an assistant specialized in analyzing and extracting data from residential property listing descriptions."},
                    {"role": "user", "content": f"Analyze the provided residential property listing description and provide info about the property. You may respond with either yes, no or maybe. If you are unsure, respond with maybe. \nListing Description:\n{request.description}\n"}]
        response = clientTogether.chat.completions.create(
                    model='mistralai/Mixtral-8x7B-Instruct-v0.1',
                    messages=messages,
                    temperature=0.0,
                    tools=tools,
                    tool_choice={"type": "function", "function": {"name": "analyze_property"}})
        try:
            out = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
            return out
        except json.JSONDecodeError as json_error:
            return {"error": "Invalid JSON response from Together", "response": response.choices[0].message.tool_calls[0].function.arguments, "json_error": str(json_error)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


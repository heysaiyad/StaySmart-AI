import os
from langchain_google_genai import ChatGoogleGenerativeAI
from google.ai.generativelanguage_v1beta.services.model_service import ModelServiceClient
from google.ai.generativelanguage_v1beta.types import ListModelsRequest

# Google Cloud Initialization
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\saiya\JUMBAYA\hotel-room-analysis\backend\keys\google_cloud_key.json"

# List available models
client = ModelServiceClient()
request = ListModelsRequest()
response = client.list_models(request=request)
print("Available models:")
for model in response.models:
    print(model.name)

# Initialize with a valid model
gemini_llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-002") 

# Test Prompt
response = gemini_llm.invoke("Which are the best budget hotels in Powai?")
print(response)
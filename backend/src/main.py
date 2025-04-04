import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get paths from environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
DATA_FILE_PATH = os.getenv("DATA_FILE_PATH")

# Load cleaned hotel data
with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
    hotel_data = json.load(file)

# Initialize Gemini AI model
gemini_llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-002")

# Get user input
print("Welcome to StaySmart AI Hotel Recommender!")
print("Please describe your hotel requirements (e.g., budget, location, amenities, etc.):")
user_input = input("Your requirements: ")

# Prepare the prompt for Gemini AI
prompt = f"""
You are an AI assistant. Use the following hotel data to find the best match for the user's request:
{json.dumps(hotel_data, ensure_ascii=False, indent=2)}

User Request: {user_input}

Instructions:
1. Analyze the user's request to understand their requirements (e.g., budget, location, amenities, etc.).
2. Filter the hotels from the provided data based on the user's requirements.
3. Analyze reviews to determine if the hotels meet subjective criteria like cleanliness, family-friendliness, or other preferences mentioned in the request.
4. Prioritize hotels that best match the user's criteria (e.g., budget, location, specific amenities).
5. Present the best-matched results in an easy-to-understand format.
6. Do not include booking links in your response, they will be added separately.
7. If no hotels match the criteria, respond with: "Sorry, no hotels match your criteria."
"""

# Invoke Gemini AI with the prompt
response = gemini_llm.invoke(prompt)

# Access the text content of the response
response_text = response.content if hasattr(response, "content") else str(response)

# Display the response
if response_text.strip():  # Check if the response text is not empty
    try:
        # Try to parse the response as JSON
        response_data = json.loads(response_text)
        recommendations = response_data.get("recommendations", [])
        if recommendations:
            print("\nBest-matched hotels:")
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['hotel_name']}")
                print("   Matched Hotel Data:")
                # Find the matching hotel in the provided data
                matched_hotel = next((hotel for hotel in hotel_data["hotels"] if hotel["name"] == rec["hotel_name"]), None)
                if matched_hotel:
                    for key, value in matched_hotel.items():
                        if key.lower() == "link":
                            continue
                        print(f"   {key.capitalize()}: {value}")
                else:
                    print("   No detailed data available for this hotel.")
                print(f"   Match Reason: {rec.get('match_reason', 'No match reason provided')}")
        else:
            print("❌ Sorry, no hotels match your criteria.")
    except json.JSONDecodeError:
        # If response is not JSON, display it in a formatted way
        print("\nBest-matched hotels:")
        print(response_text.strip())
        # Add links from the hotel_data
        print("\nBooking Links:")
        for hotel in hotel_data["hotels"]:
            if any(hotel["name"] in line for line in response_text.split("\n")):
                print(f"\n{hotel['name']}:")
                print(f"{hotel['link']}")
else:
    print("❌ Sorry, no hotels match your criteria.")
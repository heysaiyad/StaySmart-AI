import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI

# Google Cloud Initialization
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\saiya\JUMBAYA\hotel-room-analysis\backend\keys\google_cloud_key.json"

# Load cleaned hotel data
data_file_path = r"C:\Users\saiya\JUMBAYA\hotel-room-analysis\backend\data\cleaned_powai_hotels.json"
with open(data_file_path, "r", encoding="utf-8") as file:
    hotel_data = json.load(file)

# Initialize Gemini AI model
gemini_llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-002")

def get_user_input():
    """Collect user requirements interactively."""
    print("\nAapki requirements batayein (e.g., '₹5000 se kam wala hotel with pool in Powai'):")
    return input(">> ").strip()

def prepare_prompt(user_input):
    """Prepare the prompt for Gemini AI."""
    return f"""
    You are an AI assistant. Use the following hotel data to find the best match for the user's request:
    {json.dumps(hotel_data, ensure_ascii=False, indent=2)}

    User Request: {user_input}

    Instructions:
    1. Analyze the user's request to understand their requirements (e.g., budget, location, amenities, etc.).
    2. Filter the hotels from the provided data based on the user's requirements.
    3. Analyze reviews to determine if the hotels meet subjective criteria like cleanliness, family-friendliness, or other preferences mentioned in the request.
    4. Prioritize hotels that best match the user's criteria (e.g., budget, location, specific amenities).
    5. Present the best-matched results in an easy-to-understand format.
    6. If no hotels match the criteria, respond with: "Sorry, no hotels match your criteria."
    """

def display_response(response_text):
    """Display the AI's response."""
    if response_text.strip():
        print("\nGemini ka Analysis:")
        print(response_text)
    else:
        print("\n❌ Aapki requirements ke hisab se koi hotels nahi mil rahe hain.")

def main():
    """Main function to run the interactive hotel recommendation system."""
    print("Welcome to Powai Hotel Recommendation System!")
    print("===========================================")

    while True:
        print("\nOptions:")
        print("1. Hotels dhoondo")
        print("2. Exit")
        choice = input("\nAapka choice (1-2): ").strip()

        if choice == "1":
            user_input = get_user_input()
            prompt = prepare_prompt(user_input)
            response = gemini_llm.invoke(prompt)
            response_text = response.content if hasattr(response, "content") else str(response)
            display_response(response_text)
        elif choice == "2":
            print("\nThank you for using Powai Hotel Recommendation System!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
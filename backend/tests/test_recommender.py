import json
import os
from typing import Dict, List, Any
from langchain_google_genai import ChatGoogleGenerativeAI

class HotelRecommender:
    def __init__(self):
        self.hotels = []
        self.load_hotels()
        self.setup_gemini()

    def setup_gemini(self):
        """Setup Gemini API"""
        try:
            # Set Google Cloud credentials
            os.environ["GOOGLE_CLOUD_PROJECT"] = r"C:\Users\saiya\OneDrive\Desktop\cursor testing\config\google_cloud_key.json"
            
            # Initialize Gemini
            self.gemini_llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-002")
            print("✅ Gemini API successfully connect ho gaya hai")
        except Exception as e:
            print(f"❌ Gemini API connect karne mein error aaya hai: {str(e)}")
            exit(1)

    def load_hotels(self):
        """Load hotels from the cleaned JSON file"""
        try:
            with open('data/cleaned_powai_hotels.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.hotels = data['hotels']
                print(f"✅ {len(self.hotels)} hotels data/cleaned_powai_hotels.json se load ho gaye hain")
        except FileNotFoundError:
            print("❌ Error: data/cleaned_powai_hotels.json file nahi mil rahi hai. Please check karein.")
            exit(1)

    def get_recommendations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get hotel recommendations based on user query using Gemini API"""
        try:
            # Create a prompt with all hotel data
            hotel_data = json.dumps(self.hotels, indent=2)
            prompt = f"""You are a hotel recommendation expert. Based on the following hotel data and user query, recommend the most suitable hotels.

User Query: "{query}"

Hotel Data:
{hotel_data}

Please analyze the hotels and recommend only those that match the user's requirements. Consider:
1. Price range (if specified)
2. Location and views
3. Amenities
4. Reviews and ratings
5. Family-friendliness (if mentioned)
6. Cleanliness (if mentioned)

Your response should be in this exact JSON format:
{{
    "recommendations": [
        {{
            "hotel_name": "Hotel Name",
            "match_reason": "Detailed explanation why this hotel matches the requirements",
            "price": "Hotel price",
            "rating": "Hotel rating",
            "amenities": ["List of relevant amenities"]
        }}
    ]
}}

Only include hotels that truly match the user's requirements. If no hotels match, return an empty recommendations array."""

            # Get recommendations from Gemini
            response = self.gemini_llm.invoke(prompt)
            print("\nGemini ka Analysis:")
            print(response)

            # Parse Gemini's response and get hotel details
            recommendations = []
            try:
                # Extract content from response
                response_text = str(response)
                if hasattr(response, 'content'):
                    response_text = response.content
                
                # Handle markdown code blocks
                if '```json' in response_text:
                    # Extract content between ```json and ```
                    json_content = response_text.split('```json')[1].split('```')[0].strip()
                    response_data = json.loads(json_content)
                else:
                    # Try to parse the entire response as JSON
                    response_data = json.loads(response_text)
                
                for rec in response_data.get('recommendations', []):
                    hotel = next((h for h in self.hotels if h['name'] == rec['hotel_name']), None)
                    if hotel:
                        recommendations.append((hotel, rec['match_reason']))
            except json.JSONDecodeError as e:
                print(f"Gemini ka response parse nahi kar paye. Error: {str(e)}")
                print(f"Response text: {response_text}")
            except Exception as e:
                print(f"Unexpected error while parsing response: {str(e)}")
                print(f"Response text: {response_text}")

            return recommendations[:limit]

        except Exception as e:
            print(f"Gemini recommendations mein error aaya hai: {str(e)}")
            return []

    def display_recommendations(self, recommendations: List[tuple]):
        """Display hotel recommendations with details"""
        if not recommendations:
            print("\n❌ Aapki requirements ke hisab se koi hotels nahi mil rahe hain.")
            return

        print("\nRecommended Hotels:")
        for i, (hotel, match_reason) in enumerate(recommendations, 1):
            print(f"\n{i}. {hotel['name']}")
            print(f"   Address: {hotel['location']}")
            print(f"   Price: {hotel['price']}")
            print(f"   Rating: {hotel['rating']}")
            print(f"   Amenities: {', '.join(hotel['amenities'])}")
            print(f"   Match Reason: {match_reason}")

def main():
    # Initialize the recommender
    recommender = HotelRecommender()
    
    print("Welcome to Powai Hotel Recommendation System!")
    print("===========================================")
    
    while True:
        print("\nOptions:")
        print("1. Hotels dhoondo")
        print("2. Exit")
        
        choice = input("\nAapka choice (1-2): ")
        
        if choice == "1":
            query = input("\nAapki requirements batayein (e.g., '₹5000 se kam wala hotel with pool in Powai'): ")
            print("=" * 80)
            recommendations = recommender.get_recommendations(query)
            recommender.display_recommendations(recommendations)
        
        elif choice == "2":
            print("\nThank you for using Powai Hotel Recommendation System!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 
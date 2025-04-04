import json

# filepath: c:\Users\saiya\JUMBAYA\hotel-room-analysis\backend\data\powai_hotels.json
# Load the original JSON data
with open("../data/powai_hotels.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize the structured data
structured_data = {"hotels": []}

# Function to extract reviews
def extract_reviews(reviews):
    return [review.get("pros", "") or review.get("cons", "") for review in reviews if "pros" in review or "cons" in review]

# Process each hotel in the original data
for hotel in data:
    structured_hotel = {
        "name": hotel.get("Hotel Name", "Unknown"),
        "location": hotel.get("Address", "Unknown"),
        "rating": f"{hotel.get('Rating', 'N/A')}/10",
        "price": hotel.get("Price", "Information not available"),
        "amenities": hotel.get("Amenities", []),
        "reviews": extract_reviews(hotel.get("Reviews", []))
    }
    structured_data["hotels"].append(structured_hotel)

# Save the structured data to a new JSON file
with open("structured_powai_hotels.json", "w", encoding="utf-8") as file:
    json.dump(structured_data, file, indent=4, ensure_ascii=False)

print("Data has been structured and saved to 'structured_powai_hotels.json'.")
import json

# Load the structured JSON data
with open("structured_powai_hotels.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Function to remove duplicate reviews
def remove_duplicates(hotels):
    for hotel in hotels:
        if "reviews" in hotel:
            # Remove duplicates while preserving order
            hotel["reviews"] = list(dict.fromkeys(hotel["reviews"]))
    return hotels

# Clean the data
data["hotels"] = remove_duplicates(data["hotels"])

# Save the cleaned data back to the file
with open("cleaned_powai_hotels.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Duplicate reviews removed and data saved to 'cleaned_powai_hotels.json'.")
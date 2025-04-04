# StaySmart AI  

StaySmart AI is a hotel recommendation system designed to provide personalized hotel suggestions based on user preferences. It leverages Gemini AI for natural language understanding and analysis of hotel data.  

## Features  
- **Interactive Hotel Search**: Users can input their preferences (e.g., budget, location, amenities) to find the best-matched hotels.  
- **AI-Powered Recommendations**: Uses Gemini AI to analyze user queries and hotel data for accurate recommendations.  
- **Comprehensive Hotel Data**: Includes detailed reviews, ratings, pros, and cons for hotels in Powai.  
- **Multi-Language Support**: Provides responses in English and Hindi for better user accessibility.  

## Project Structure  
```plaintext  
backend/  
├── data/  
│   └── powai_hotels.json          # Raw hotel data with reviews and ratings  
├── src/  
│   └── main.py                    # Main application logic  
├── tests/  
│   ├── test_main.py               # Tests for main application logic  
│   └── test_recommender.py        # Tests for hotel recommender module  
└── keys/  
    └── google_cloud_key.json      # Google Cloud credentials for Gemini AI  
```  

## How to Run  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-repo/StaySmart-AI.git  
   cd StaySmart-AI/backend  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Set up Google Cloud credentials:  
   - Place your `google_cloud_key.json` file in the `keys/` directory.  

4. Run the application:  
   ```bash  
   python src/main.py  
   ```  

5. Follow the interactive prompts to get hotel recommendations.  

## Testing  
Run the test suite to ensure everything is working as expected:  
```bash  
pytest tests/  
```  

## Contributing  
Contributions are welcome! Please fork the repository and submit a pull request.  

## License  
This project is licensed under the MIT License.  

---  


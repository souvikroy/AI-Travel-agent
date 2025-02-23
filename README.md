# TRAVEL ai AGENT

Pretext : Do you believe AI can revolutionize travel accessibility, affordability & experience ?

It is an AI-powered tour planning system that generates personalized tour packages based on user preferences. The system uses OpenAI's GPT-4 and Streamlit to create detailed tour plans similar to professional travel agency packages.

https://www.loom.com/share/2b50a8727b96457ebd6a9f9dc6bf8b1e?sid=838f2efc-442b-45b6-ae92-75cb10b5b915

## Features

- Multiple travel categories (honeymoon, family, adventure, etc.)
- Domestic and international destination options
- Flexible budget ranges
- Customizable trip duration
- Activity preferences
- Generates 5 detailed tour plans per request
- Professional tour package format with all necessary details

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. Select your preferred travel category
2. Choose destination type (India or International)
3. Select your budget range per person
4. Choose trip duration
5. Select preferred activities
6. Click "Generate Tour Plans" to get 5 personalized tour packages

## Tour Package Format

Each generated tour package includes:
- Tour Title with Duration
- Overview & Highlights
- Detailed Day-by-Day Itinerary
- Activities and Experiences
- Accommodation Details
- Transportation Details
- Meal Plan
- Package Inclusions and Exclusions
- Best Time to Visit
- Additional Notes & Tips
- Approximate Cost Per Person
- Booking Terms & Conditions

## Note

Make sure you have a valid OpenAI API key with access to GPT-4 to use this application.

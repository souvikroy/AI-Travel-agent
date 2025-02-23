import streamlit as st
import json
import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import markdown2
from serpapi import GoogleSearch
import requests

# Load environment variables
load_dotenv()

# Initialize OpenAI client
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
)

# Function to extract JSON from metadata string
def extract_json_from_string(content):
    try:
        # Try to parse the entire content as JSON first
        try:
            return json.loads(content)
        except:
            pass

        # Look for JSON-like structure
        start = content.find('{')
        if start == -1:
            st.error("Could not find JSON data in the response")
            return None
            
        content = content[start:]
        brace_count = 0
        end = 0
        for i, char in enumerate(content):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    break
        
        if end == 0:
            st.error("Could not find complete JSON structure")
            return None
            
        json_str = content[:end]
        return json.loads(json_str)
    except Exception as e:
        st.error(f"Error parsing JSON: {str(e)}")
        return None

# Function to get a relevant image for a location
def get_location_image(location, activity):
    try:
        # Create a search query
        search_query = f"{location} {activity} tourist attraction landmark"
        
        # Search for images using SerpApi
        search = GoogleSearch({
            "q": search_query,
            "tbm": "isch",  # Image search
            "num": 1,  # Number of results
            "api_key": os.getenv("SERPAPI_API_KEY")
        })
        results = search.get_dict()
        
        # Extract image URL from results
        if results.get("images_results") and len(results["images_results"]) > 0:
            return results["images_results"][0]["original"]
            
        # Fallback to a curated list of beautiful travel images
        fallback_images = [
            "https://source.unsplash.com/1600x900/?travel,landmark",
            "https://source.unsplash.com/1600x900/?tourism,architecture",
            "https://source.unsplash.com/1600x900/?vacation,destination",
            "https://source.unsplash.com/1600x900/?wanderlust,explore"
        ]
        import random
        return random.choice(fallback_images)
        
    except Exception as e:
        st.error(f"Error fetching image: {str(e)}")
        # Return a random travel-themed image from Unsplash
        return "https://source.unsplash.com/1600x900/?travel,landmark"

# Set up the main page
st.set_page_config(
    page_title="AI Tour Planner",
    page_icon="🌍",
    layout="wide"
)

st.title("AI Tour Planner 🌍")
st.write("Let me help you plan your perfect trip!")

# Create form for user input
with st.form("tour_form"):
    destination = st.text_input("Where would you like to go?")
    duration = st.number_input("How many days is your trip?", min_value=1, max_value=30, value=3)
    interests = st.text_area("What are your interests? (e.g., history, food, nature)")
    budget = st.selectbox("What's your budget level?", ["Budget", "Moderate", "Luxury"])
    submit_button = st.form_submit_button("Generate Plans")

# Handle form submission
if submit_button:
    if not destination or not interests:
        st.warning("Please fill in all required fields.")
    else:
        try:
            with st.spinner("Crafting your dream vacation..."):
                # Create the prompt template with emphasis on catchy headlines
                prompt = PromptTemplate(
                    input_variables=["destination", "duration", "interests", "budget"],
                    template="""As an expert travel planner and creative copywriter, create a detailed {duration}-day itinerary for {destination}. 
                    The traveler is interested in: {interests}
                    Budget level: {budget}
                    
                    Create an EXTREMELY catchy and engaging headline that makes this trip sound irresistible!
                    
                    Please provide the itinerary in the following JSON format:
                    {{
                        "headline": "Your super catchy headline here",
                        "destination": "city name",
                        "duration": "number of days",
                        "daily_plans": [
                            {{
                                "day": 1,
                                "tagline": "Catchy tagline for this day's activities",
                                "activities": [
                                    {{
                                        "time": "morning/afternoon/evening",
                                        "activity": "description",
                                        "location": "specific place name",
                                        "notes": "additional information"
                                    }}
                                ]
                            }}
                        ],
                        "estimated_budget": "range in USD",
                        "travel_tips": ["tip1", "tip2"]
                    }}
                    
                    Make the headline and daily taglines extremely engaging, using powerful words, alliteration, or clever wordplay.
                    Be specific with location names for better image matching.
                    """
                )

                # Create and run the chain
                chain = LLMChain(llm=llm, prompt=prompt)
                result = chain.invoke({
                    "destination": destination,
                    "duration": duration,
                    "interests": interests,
                    "budget": budget
                })

                # Extract JSON from the response
                travel_plan = extract_json_from_string(result['text'])
                
                if travel_plan:
                    # Display the travel plan in a structured way
                    st.success("Your dream vacation is ready! 🎉")
                    
                    # Display the catchy headline
                    st.title(f"✨ {travel_plan['headline']}")
                    
                    # Display destination and duration
                    st.header(f"📍 {travel_plan['destination']} - {travel_plan['duration']} Days")
                    st.write(f"💰 Estimated Budget: {travel_plan['estimated_budget']}")
                    
                    # Display daily plans with images
                    for day in travel_plan['daily_plans']:
                        st.subheader(f"Day {day['day']} - {day['tagline']} 📅")
                        
                        # Create columns for each activity to show image and details side by side
                        for activity in day['activities']:
                            col1, col2 = st.columns([1, 2])
                            
                            # Get and display image in the first column
                            image_url = get_location_image(activity['location'], activity['activity'])
                            with col1:
                                st.image(image_url, caption=activity['location'], use_column_width=True)
                            
                            # Display activity details in the second column
                            with col2:
                                st.markdown(f"""
                                **{activity['time'].title()}**: {activity['activity']}  
                                🏠 *Location*: {activity['location']}  
                                📝 *Notes*: {activity['notes']}
                                """)
                    
                    # Display travel tips
                    st.subheader("✨ Pro Travel Tips")
                    for tip in travel_plan['travel_tips']:
                        st.markdown(f"- {tip}")
                else:
                    st.error("Sorry, there was an error generating your travel plan. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

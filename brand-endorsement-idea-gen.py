import streamlit as st
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key="AIzaSyDODWuZj0Xd8RK4QFPqP4Wttze7Zoyyx6g")  

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(history=[])
st.set_page_config(page_title="Content Idea Generator")
# Function to get Gemini response
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")


# Initialize Streamlit app

st.header("Get Your Own Unique Idea Crafted For Any Brand Endorsement")

# Ask for brand name
brand_name = st.text_input("Which brand are you promoting?")

# Ask for content format
content_format = st.selectbox("Select content format:", ["Reel", "Post", "Ads"])

# Generate content ideas
if st.button("Generate Ideas"):
    if brand_name and content_format:
        st.subheader(f"Ideas for promoting {brand_name} using {content_format}:")
        for _ in range(5):
            user_input = f"Idea for promoting {brand_name} using {content_format}"
            response = get_gemini_response(user_input)
            if response:
                idea = ""
                for chunk in response:
                    idea += chunk.text
                st.write(f"- {idea}")
            else:
                st.error("Failed to generate ideas. Please try again later.")
    else:
        st.warning("Please provide the brand name and select a content format before generating ideas.")

import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
# Configure generative model with API key
genai.configure(api_key="AIzaSyDl2nIaYT9ef8vJ6NDhXnIOUj-Z_UmYfXU")  

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(history=[])

def get_gemini_response(caption):
    try:
        prompt = f"Generate relevant 50 hashtags for the following caption: '{caption}'"
        response = chat.send_message(prompt, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")

# Initialize Streamlit app
st.set_page_config(page_title="Hastags GEN")
st.header("Generate Hastags")

user_input = st.text_input("Enter your caption or tweet: ", key="user_input")
submit = st.button("Generate Hashtags")

if submit and user_input:
    response = get_gemini_response(user_input)
    if response:
        st.subheader("Generated Hashtags:")
        hashtags = []
        for chunk in response:
            hashtags.append(chunk.text)
        st.write(", ".join(hashtags))
    else:
        st.error("Failed to get a response. Please try again later.")
elif submit and not user_input:
    st.warning("Please input a caption or tweet before submitting.")
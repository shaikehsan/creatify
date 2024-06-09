import streamlit as st
import google.generativeai as genai

# Configure the Google Generative AI with your API key
genai.configure(api_key="AIzaSyDl2nIaYT9ef8vJ6NDhXnIOUj-Z_UmYfXU")  

# Function to load the Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(history=[])

def get_gemini_response(prompt_type, user_input):
    try:
        question = f"Generate a {prompt_type} on: {user_input} make it very evident that it's a {user_input} and also give the heading as 'BLOG ON {user_input}'"
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")

# Initialize Streamlit app
st.set_page_config(page_title="WRITER.AI")
st.header("WRITER.AI")

# User input for type of content
content_type = st.selectbox("Select the type of content:", ["Blog", "Article"])

# User input for the content topic
user_input = st.text_input("Input: ", key="user_input")
submit = st.button("Generate")

if submit and user_input:
    response = get_gemini_response(content_type, user_input)
    if response:
        st.subheader("Generated Content")
        for chunk in response:
            st.write(chunk.text)
    else:
        st.error("Failed to get a response. Please try again later.")
elif submit and not user_input:
    st.warning("Please input a topic before submitting.")

import streamlit as st
import json
import requests
import time
from newspaper import Article
import base64

# Function to set background image
def set_background_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/avif;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        st.write(f"Error setting background image: {e}")

# Set the background image
set_background_image("sum back.avif")

# Page title layout
c1, c2 = st.columns([0.32, 2])

with c1:
    st.image("images/newspaper.png", width=85)

with c2:
    st.title("Article & Blog Summarizer")

# Sidebar content
st.sidebar.subheader("About the app")
st.sidebar.markdown("Welcome to Article & Blog Summarizer, an efficient tool designed to provide quick and accurate summaries of news articles and blog posts. This model is specifically fine-tuned on the CNN/DailyMail dataset, to generate abstractive summaries.")
st.sidebar.divider()
st.sidebar.write("Please make sure your article is in English")
st.sidebar.write("\n\n")
st.sidebar.divider()
st.sidebar.caption("Created by SYNC SQUAD using [Streamlit](https://streamlit.io/)🎈.")

# Inputs 
st.subheader("Enter the URL of the article you want to summarize")
default_url = "https://"
url = st.text_input("URL:", default_url)

headers_ = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

fetch_button = st.button("Fetch article")

if fetch_button:
    article_url = url
    session = requests.Session()

    try:
        response_ = session.get(article_url, headers=headers_, timeout=10)
    
        if response_.status_code == 200:
            with st.spinner('Fetching your article...'):
                time.sleep(3)
                st.success('Your article is ready for summarization!')
        else:
            st.write("Error occurred while fetching article.")
    except Exception as e:
        st.write(f"Error occurred while fetching article: {e}")

# HuggingFace API KEY input
API_KEY = st.text_input("Enter your HuggingFace API key", type="password")

# HuggingFace API inference URL.
API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"

headers = {"Authorization": f"Bearer {API_KEY}"}

submit_button = st.button("Submit")

# Download and parse the article
if submit_button:
    article = Article(url)
    article.download()
    article.parse()

    title = article.title
    text = article.text

    # HuggingFace API request function
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    with st.spinner('Doing some AI magic, please wait...'):
        time.sleep(1)

        # Query the API
        output = query({
            "inputs": text, 
            "parameters": {"truncation": "only_first"},
        })

        # Print output for debugging
        st.write("API Response:", output)

        # Check if 'summary_text' key is in the response
        if 'error' in output:
            st.write(f"Error from the API: {output['error']}")
        elif output and isinstance(output, list) and "summary_text" in output[0]:
            summary = output[0]["summary_text"].replace("<n>", " ")
            st.divider()
            st.subheader("Summary")
            st.write(f"Your article: **{title}**")
            st.write(f"**{summary}**")
        else:
            st.write("Error: The API response does not contain 'summary_text'.")

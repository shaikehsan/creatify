import streamlit as st
import base64
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyDl2nIaYT9ef8vJ6NDhXnIOUj-Z_UmYfXU")

# Function to get response from Gemini API
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.0-pro")
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt, stream=True)
        response.resolve()
        
        # Accumulate response parts
        generated_text = "".join([part.text for part in response.parts])
        return generated_text.strip()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to set background image using base64 encoding
def set_background_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Background image not found at: {image_path}")

# Set background image
set_background_image("stbg.png")

# Streamlit app
def main():
    st.title("Story Style Transfer")

    # User input for original story
    original_story = st.text_area("Enter the original story:")

    # Select target style for transfer
    st.subheader("Select Target Style:")
    style_options = ["Shakespeare", "Charles Dickens", "Jane Austen", "Ernest Hemingway"]
    selected_style = st.selectbox("Choose a style:", style_options)

    if st.button("Transfer Style"):
        if original_story:
            # Generate prompt for style transfer
            prompt = f"Rewrite the following story in the style of {selected_style}:\n\n{original_story}\n\nThe story should have a proper start and a proper end."
            styled_story = get_gemini_response(prompt)
            if styled_story:
                # Display styled story
                st.subheader("Styled Story:")
                st.write(styled_story)

if __name__ == "__main__":
    main()

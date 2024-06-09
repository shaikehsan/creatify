import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyDODWuZj0Xd8RK4QFPqP4Wttze7Zoyyx6g")

# Function to interact with Gemini for story generation
def generate_story(genre, theme, writing_style, prompt, additional_prompt):
    try:
        model = genai.GenerativeModel("gemini-1.0-pro")
        chat = model.start_chat(history=[])
        
        response = chat.send_message(f"Genre: {genre}\nTheme: {theme}\nWriting Style: {writing_style}\n\n{prompt}\n{additional_prompt}", stream=True)
        
        # Resolve response to complete iteration
        response.resolve()
        
        # Accumulate response parts into generated story
        generated_story = ""
        for part in response.parts:
            generated_story += part.text + "\n"
        
        # Post-process generated story to ensure it meets criteria
        generated_story = post_process_story(generated_story)
        
        return generated_story.strip()
    except Exception as e:
        st.error(f"Error generating story: {str(e)}")
        return None

# Function to post-process the generated story
def post_process_story(story):
    # Trim the story to 200 words
    story = " ".join(story.split()[:200])
    # Add a proper ending if not present
    if not story.endswith((".", "!", "?")):
        story += "."
    return story

# Streamlit app
def main():
    st.title("Story Writer")

    # User input options
    genre_options = ["Mystery/Thriller", "Inspirational", "Romance", "Comedy"]
    selected_genre = st.selectbox("Select Genre:", genre_options)

    theme_options = ["Tolerance and Acceptance", "Body-Image and Self-Image", "Identity and Self-Worth", "Problem-Solving"]
    selected_theme = st.selectbox("Select Theme:", theme_options)

    writing_style_options = ["Poetic and Descriptive", "Fast-Paced and Action-Packed", "Witty and Humorous", "Narrative and Creative"]
    selected_writing_style = st.selectbox("Select Writing Style:", writing_style_options)

    # User input for story prompt
    story_prompt = st.text_area("Enter the beginning of your story:")
    
    # Additional prompt provided by the user
    additional_prompt = "The story should have a proper start and a proper end. Write it in 200 words"

    if st.button("Generate Story"):
        if story_prompt:
            generated_story = generate_story(selected_genre, selected_theme, selected_writing_style, story_prompt, additional_prompt)
            if generated_story:
                # Display generated story
                st.subheader("Generated Story:")
                st.write(generated_story)

if __name__ == "__main__":
    main()

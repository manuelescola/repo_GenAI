import streamlit as st
import os
import google.generativeai as genai

from apikey import google_gemini_api_key, openai_api_key
from safety_settings import kids_safety_settings

from openai import OpenAI
genai.configure(api_key=google_gemini_api_key)
client = OpenAI(api_key=openai_api_key)

# Create the model

safety_settings = kids_safety_settings

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-pro",
  generation_config=generation_config,
  safety_settings = safety_settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Set app to wide mode
st.set_page_config(layout='wide')



# Sidebar for user input

with st.sidebar:
    st.title("Input Your Blog Details")
    st.subheader("Enter Details of the Blog You Want to Generate")

    blog_title = st.text_input("Story Title")

    keywords = st.text_area("Keywords (comma-separated)")

    moral = st.text_area("Moral you want to teach the kids")

    # num_minutes = st.slider("Time to read", min_value = 1, max_value = 5, step = 1)

    prompt_parts = [
        f"""
        Generate a very long story for kids considering the title \"{blog_title}\". 
        The story must be divided in 6 long paragraphs: exposition, conflict, rising action, climax, falling action, and resolution.
        The story should consider the keywords \"{keywords}\".
        The story must be written in the language of the title and the keywords.
        The story must start with "Once upon a time" or the equivalent in the language you are writing the rest of the text. 

        At the end, write a separate paragraph with a moral. The moral is {moral}.   
        Do not return the title of the story. Return the story directly.
        """
        ]
    
    submit_button = st.button("Generate Story")

if not submit_button:
    # title of our app
    st.title('✍️ Once Upon AI Time: the story teller!')

    # create a subheader
    st.subheader('\nYou can create any story in seconds! \n Just complete the questionaire on the left side of the page and click on "Generate Story"')

if submit_button:

    # title of our app
    st.title('📖📚 You can read your story below.')
    
    response_text = model.generate_content(prompt_parts)
    st.title(blog_title)

    # Split the text into words
    words = response_text.text.split()
    
    # Find the halfway point based on the number of words
    len_words = len(words) // 2
    
    # Join the first half of the words back into a string
    raw_text = ' '.join(words[:len_words])
    
    # Write the first half of the text (first half of the words)
    st.write(raw_text)

    #################################################### Image generation part ####################################################
    # response_image = client.images.generate(
    # model="dall-e-3",
    # prompt=f"Create a picture to include within a book for a book for kids about {blog_title}.",
    # size="1024x1024",
    # quality="standard",
    # n=1,
    # )

    # image_url = response_image.data[0].url

    # st.image(image_url, caption="Generated Image")
    ################################################################################################################################
    # Write the second half of the text (second half of the words)
    st.write(' '.join(words[len_words:]))
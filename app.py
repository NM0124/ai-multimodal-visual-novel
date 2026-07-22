import streamlit as st
import os
import json
import urllib.parse
import requests
from gtts import gTTS
from dotenv import load_dotenv
from google import genai

load_dotenv()

# page config
st.set_page_config(page_title="AI Visual Novel", page_icon="🎮", layout="wide")

# gemini
@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

# sidebar
st.sidebar.title("Story Settings")

genre = st.sidebar.selectbox("Story Genre", ["Fantasy", "Sci-Fi", "Mystery", "Horror", "Adventure"])

art_style = st.sidebar.selectbox("Art Style", ["Realistic", "Anime", "Oil Painting", "Pixel Art", "Cyberpunk"])

if st.sidebar.button("Restart Story"):
    st.session_state.clear()
    st.rerun()

# session state
if "started" not in st.session_state:
    st.session_state.started = False

if "history" not in st.session_state:
    st.session_state.history = []

if "options" not in st.session_state:
    st.session_state.options = []

if "chat" not in st.session_state:
    system_prompt = f"""You are an AI Visual Novel Engine.
                        Genre: {genre}, Art Style: {art_style}.
                        Always reply ONLY in valid JSON. Never use markdown. Never use ```.
                        Output format:
                    {{
                        "story_text":"...",
                        "image_prompt":"...",
                        "options":[
                        "...",
                        "...",
                        "..."
                        ]
                    }}
                    Rules:
                    Continue the story naturally. The image_prompt should be detailed and cinematic. Return only JSON."""

    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": system_prompt
        }
    )

# functions for different features
def generate_story(user_input):
    response = st.session_state.chat.send_message(user_input)
    text = response.text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return json.loads(text)


def generate_image(prompt):
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}"
    response = requests.get(url, timeout=30)
    return response.content

def generate_audio(text):
    tts = gTTS(text)
    filename = "story.mp3"
    tts.save(filename)
    return filename

def add_scene(scene):
    st.session_state.history.append(scene)
    st.session_state.options = scene["options"]

# title
st.title("AI Multi-Modal Visual Novel")

st.write("Create your own adventure with AI!")

# start
if not st.session_state.started:
    if st.button("Start Story"):

        with st.spinner("Creating story..."):
            try:
                scene = generate_story(f"Begin a {genre} adventure.")

                image = None
                try:
                    image = generate_image(scene["image_prompt"])
                except Exception:
                    st.toast("Image server busy. Continuing without image.")

                audio = None
                try:
                    audio = generate_audio(scene["story_text"])

                except Exception:
                    st.toast("Audio generation failed.")

                add_scene(
                    {
                        "story": scene["story_text"],
                        "image": image,
                        "audio": audio,
                        "options": scene["options"]
                    }
                )

                st.session_state.started = True
                st.rerun()

            except Exception as e:
                st.error(e)

# display history
for i, scene in enumerate(st.session_state.history):
    st.markdown("---")
    left, right = st.columns([1,1])

    with left:
        st.subheader(f"Chapter {i+1}")
        st.write(scene["story"])
        if scene["audio"]:
            st.audio(scene["audio"])

    with right:
        if scene["image"]:
            st.image(scene["image"], use_container_width=True)

# options
if st.session_state.started:

    st.markdown("---")
    st.subheader("Choose Your Next Move")
    for option in st.session_state.options:
        if st.button(option):
            with st.spinner("Continuing story..."):
                try:
                    scene = generate_story(option)
                    
                    image = None
                    try:
                        image = generate_image(scene["image_prompt"])
                    except Exception:
                        st.toast("Image server busy.")

                    audio = None
                    try:
                        audio = generate_audio(scene["story_text"])
                    except Exception:
                        st.toast("Audio generation failed.")

                    add_scene(
                        {
                            "story": scene["story_text"],
                            "image": image,
                            "audio": audio,
                            "options": scene["options"]
                        }
                    )

                    st.rerun()

                except Exception as e:
                    st.error(e)

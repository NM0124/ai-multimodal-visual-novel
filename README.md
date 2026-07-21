# AI Multi-Modal Visual Novel

An AI-powered **Choose Your Own Adventure** game built with **Streamlit**, where every decision changes the story. The application combines text generation, AI-generated visuals, and text-to-speech narration to create an interactive storytelling experience.

## Features

* AI-generated branching story using **Google Gemini**
* Scene illustrations generated with the **Pollinations API**
* AI narration using **Google Text-to-Speech (gTTS)**
* Dynamic choice buttons generated from AI responses
* Stateful gameplay using `st.session_state`
* Structured JSON parsing for reliable AI output
* Configurable story genre and art style
* Graceful error handling with `try...except`

## Tech Stack

* Python
* Streamlit
* Google Gemini API
* Pollinations AI
* gTTS (Google Text-to-Speech)
* Requests
* Pillow
* JSON
* python-dotenv

## How It Works

1. Select a **Story Genre** and **Art Style**.
2. Start a new adventure.
3. Gemini generates:

   * Story narration
   * Image prompt
   * Multiple choices for the next action
4. The image prompt is sent to Pollinations to generate a scene illustration.
5. The narration is converted into speech using gTTS.
6. Choose your next action to continue the story, creating a unique adventure every time.

## Project Structure

```text
.
├── app.py
├── .env
├── requirements.txt
├── story.mp3
└── README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/NM0124/ai-multimodal-visual-novel
cd ai-multimodal-visual-novel

pip install -r requirements.txt

streamlit run app.py
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

## Future Improvements

* Character avatars
* Background music and sound effects
* Save and load story progress
* Multiple endings
* Inventory and player stats
* Animated scene transitions
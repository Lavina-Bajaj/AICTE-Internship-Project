import streamlit as st
import requests
import base64

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📘",
    layout="centered"
)

# -----------------------------
# Session State (History)
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

# -----------------------------
# Background Image Function
# -----------------------------
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Glass card effect */
    .block-container {{
        background: rgba(255,255,255,0.85);
        padding: 2rem;
        border-radius: 15px;
    }}

    /* Button styling */
    div.stButton > button {{
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# Apply Background
set_background("Background img.webp")

# -----------------------------
# Sidebar History
# -----------------------------
st.sidebar.title("📜 Previous Questions")

if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history)):
        if st.sidebar.button(item, key=f"history_{i}"):
            st.session_state.selected_question = item
else:
    st.sidebar.write("No history yet.")

# -----------------------------
# Hugging Face Settings
# -----------------------------
API_URL = "https://router.huggingface.co/v1/chat/completions"

HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# -----------------------------
# AI Function
# -----------------------------
def ask_ai(prompt):

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

# -----------------------------
# UI
# -----------------------------
st.title("📘 AI Study Buddy")
st.write("### Your Smart AI Learning Assistant")

mode = st.selectbox(
    "Choose Study Mode",
    [
        "Explain Topic",
        "Summarize Notes",
        "Exam Ready Answer (5 Marks)",
        "Generate Viva Questions"
    ]
)

user_input = st.text_area(
    "Enter topic or paste your notes",
    value=st.session_state.selected_question
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate"):

    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:

        # Save question to history
        if user_input not in st.session_state.history:
            st.session_state.history.append(user_input)

        with st.spinner("AI is thinking... 🤖"):

            # Explain Mode
            if mode == "Explain Topic":
                prompt = f"""
Explain {user_input} in simple words for a BTech student.

Include:
1. Definition
2. Working
3. Key Points
4. Real-life example
"""

            # Summary Mode
            elif mode == "Summarize Notes":
                prompt = f"""
Summarize the following into short bullet-point study notes:

{user_input}
"""

            # Exam Answer Mode
            elif mode == "Exam Ready Answer (5 Marks)":
                prompt = f"""
Write a 5-mark exam-ready answer on:

{user_input}

Include definition, explanation, key points and conclusion.
Keep it concise and well structured.
"""

            # Viva Mode
            elif mode == "Generate Viva Questions":
                prompt = f"""
Create 5 viva questions with short answers about:

{user_input}
"""

            answer = ask_ai(prompt)

            st.markdown("### ✅ Result")
            st.write(answer)
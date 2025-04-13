import streamlit as st
import requests
import os
import textwrap
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="🧠 Math Solver", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f5f5;
        color: #333333;
    }
    .main {
        padding-top: 30px;
    }
    .stTextInput>div>div>input {
        padding: 12px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
    }
    .stSelectbox>div>div {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 Engineering Math Problem Solver")
st.markdown("""
Type any engineering math problem below and get a solution using AI. 
Choose whether you want a **step-by-step explanation** or just the **direct answer**.
""")

# Input area
question = st.text_area("Enter your math problem:", height=150, placeholder="e.g. Solve the differential equation dy/dx + y = e^x")
mode = st.selectbox("Solution Type:", ["Step-by-Step", "Direct Answer"])

# API info
api_key = os.getenv("OPENROUTER_API_KEY")  # Ensure this is set in your environment
model = "mistralai/mixtral-8x7b-instruct"

headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "your-app-id-on-openrouter",  # Replace with your actual referrer if needed
    "Content-Type": "application/json"
}

# Prompt formatting
if mode == "Step-by-Step":
    prompt_prefix = "Solve this engineering math problem step-by-step:"
else:
    prompt_prefix = "Give a direct concise answer to this engineering math problem:"

# Submit button
if st.button("🔍 Solve"):
    if not question.strip():
        st.warning("⚠️ Please enter a math problem before clicking Solve.")
    elif not api_key:
        st.error("❌ API key is missing. Please set the OPENROUTER_API_KEY environment variable.")
    else:
        with st.spinner("Solving..."):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model,
                        "messages": [
                            {"role": "user", "content": f"{prompt_prefix} {question}"}
                        ]
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    answer_wrapped = "\n\n".join(textwrap.wrap(answer, width=100))
                    st.markdown("### ✅ Solution")
                    st.markdown(f"""<div style='white-space: pre-wrap;'>{answer_wrapped}</div>""", unsafe_allow_html=True)
                else:
                    st.error(f"⚠️ API Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {str(e)}")

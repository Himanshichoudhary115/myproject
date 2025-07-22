import streamlit as st
import json
from streamlit_lottie import st_lottie

def load_lottie_json(path: str):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except:
        return None

lottie_idle = load_lottie_json("idle_animation.json")

st.title("🏠 Welcome to RPS Game")
st.markdown("""
Use your **hand gestures** to play:
- ✊ Rock  
- ✋ Paper  
- ✌️ Scissors

You will play against the **Computer**. Good luck! 🍀
""")

if lottie_idle:
    st_lottie(lottie_idle, height=300)
else:
    st.warning("⚠️ Could not load idle animation.")

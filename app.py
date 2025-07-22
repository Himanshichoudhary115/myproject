import streamlit as st
import json
from streamlit_lottie import st_lottie

# ------------------------ Page Config ------------------------
st.set_page_config(
    page_title="Rock Paper Scissors Game",
    page_icon="✊",
    layout="centered"
)

# ------------------------ Load Lottie Animation ------------------------
def load_lottie_json(path: str):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except:
        return None

lottie_idle = load_lottie_json("idle_animation.json")

# ------------------------ Main Page ------------------------
st.markdown("<h1 style='text-align: center;'>✊ Rock Paper Scissors</h1>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 18px;">
Use your hand gestures to play the classic game of<br><b>Rock ✊, Paper ✋, and Scissors ✌️</b><br>
against the computer in real time!
</div>
""", unsafe_allow_html=True)

# ------------------------ Lottie Animation ------------------------
if lottie_idle:
    st_lottie(lottie_idle, height=300)
else:
    st.warning("⚠️ Could not load idle animation. Please check the file path.")

# ------------------------ Instructions ------------------------
with st.expander("📝 How to Play"):
    st.markdown("""
    1. Go to the **Play Game** page using the sidebar.
    2. Allow webcam access.
    3. Show your hand gesture:
       - ✊ **Rock**
       - ✋ **Paper**
       - ✌️ **Scissors**
    4. The AI will detect your move and play against you!
    5. Check the **Scoreboard** page to track wins & losses.

    Have fun! 🎉
    """)

# ------------------------ Credits ------------------------
st.markdown("""
---
Made with ❤️ by **[Himanshi Choudhary]**  
Powered by **Streamlit**, **MediaPipe**, and **OpenCV**
""")

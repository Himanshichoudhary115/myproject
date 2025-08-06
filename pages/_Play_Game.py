import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import tensorflow as tf
from keras.models import load_model
import time
import json
import requests
from streamlit_lottie import st_lottie

# Load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_puciaact.json")
lottie_win = load_lottieurl("https://assets10.lottiefiles.com/private_files/lf30_cgfdhxgx.json")
lottie_lose = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_editor_bbhpwtvy.json")
lottie_draw = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_x62chJ.json")

# Load the model
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

# WebRTC configuration
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Video Processor
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.result = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_resized = cv2.resize(img, (224, 224))
        img_normalized = (img_resized.astype(np.float32) / 127.5) - 1
        img_reshaped = np.expand_dims(img_normalized, axis=0)

        predictions = model.predict(img_reshaped, verbose=0)
        class_index = np.argmax(predictions)
        confidence_score = predictions[0][class_index]

        if confidence_score > 0.85:
            label = class_names[class_index].strip()
            if label in ["rock", "paper", "scissors"]:
                st.session_state.player_move = label

        return img

# Streamlit App UI
st.set_page_config(page_title="Rock Paper Scissors Game", page_icon="✊", layout="centered")

st.title("✊ Rock Paper Scissors Game")
st.write("🧠 Powered by Machine Learning + Live Video")

# Initialize session variables
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "player_move" not in st.session_state:
    st.session_state.player_move = None
if "result_shown" not in st.session_state:
    st.session_state.result_shown = False

# Live camera stream
st.markdown("### 🎥 Live Feed")
ctx = webrtc_streamer(
    key="game",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration=RTC_CONFIGURATION,
    async_processing=True,
)

# Game Play
if ctx.state.playing:
    if st.button("🚀 Start Game"):
        st.session_state.result_shown = False
        st.session_state.player_move = None

        # Give user 7 seconds to show their hand
        time.sleep(7)

        player_move = st.session_state.player_move
        options = ["rock", "paper", "scissors"]

        if player_move is None:
            st.error("🙁 Could not detect your move. Try again!")
        else:
            computer_move = np.random.choice(options)
            st.markdown(f"🧍 You chose: **{player_move.capitalize()}**")
            st.markdown(f"💻 Computer chose: **{computer_move.capitalize()}**")

            if player_move == computer_move:
                if lottie_draw:
                    st_lottie(lottie_draw, height=300)
                st.info("🤝 It's a Draw!")
            elif (
                (player_move == "rock" and computer_move == "scissors") or
                (player_move == "paper" and computer_move == "rock") or
                (player_move == "scissors" and computer_move == "paper")
            ):
                st.session_state.player_score += 1
                if lottie_win:
                    st_lottie(lottie_win, height=300)
                st.success("🎉 You Win!")
            else:
                st.session_state.computer_score += 1
                if lottie_lose:
                    st_lottie(lottie_lose, height=300)
                st.error("😢 You Lose!")

            st.markdown("---")
            st.markdown(f"### 🔢 Current Score")
            st.markdown(f"🧍 You: **{st.session_state.player_score}** &nbsp;&nbsp;&nbsp;&nbsp; 💻 Computer: **{st.session_state.computer_score}**")

# Reset button
if st.button("🔁 Reset Scores"):
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.success("✅ Scores reset!")

# Footer animation
st.markdown("---")
st_lottie(lottie_hello, height=100)

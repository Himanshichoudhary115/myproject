import streamlit as st
import pickle
import numpy as np
import mediapipe as mp
import time
import json
from streamlit_lottie import st_lottie
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

# ------------------------ Page Config ------------------------
st.set_page_config(page_title="Play Game", page_icon="🎮")

# ------------------------ Utility: Load Lottie ------------------------
def load_lottie_json(path: str):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except:
        return None

# ------------------------ Load Animations ------------------------
lottie_win = load_lottie_json("win_animation.json")
lottie_lose = load_lottie_json("lose_animation.json")
lottie_draw = load_lottie_json("draw_animation.json")

# ------------------------ Load Model ------------------------
model = pickle.load(open("gesture_model.pkl", "rb"))

# ------------------------ MediaPipe Setup ------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# ------------------------ Init Session State ------------------------
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "player_move" not in st.session_state:
    st.session_state.player_move = None
if "result_shown" not in st.session_state:
    st.session_state.result_shown = False

# ------------------------ Title ------------------------
st.title("🎮 Let's Play!")
st.markdown("Make a gesture in front of your webcam (✊, ✋, ✌️) to play against the computer.")

# ------------------------ Video Processor Class ------------------------
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        self.last_prediction_time = time.time()
        self.detected_move = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks and not st.session_state.result_shown:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            data = [lm.x for lm in hand_landmarks.landmark] + \
                   [lm.y for lm in hand_landmarks.landmark] + \
                   [lm.z for lm in hand_landmarks.landmark]
            prediction = model.predict([data])[0]
            self.detected_move = prediction.lower()

            cv2.putText(img, f"You: {self.detected_move}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            # Save prediction after a few seconds
            if time.time() - self.last_prediction_time > 5 and not st.session_state.result_shown:
                st.session_state.player_move = self.detected_move
                st.session_state.result_shown = True

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ------------------------ Game Logic ------------------------
if st.button("🚀 Start Game"):
    st.session_state.result_shown = False
    st.session_state.player_move = None

    webrtc_streamer(
        key="game",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    # Wait and then show result
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

        # Display updated scores
        st.markdown("---")
        st.markdown(f"### 🔢 Current Score")
        st.markdown(f"🧍 You: **{st.session_state.player_score}** &nbsp;&nbsp;&nbsp;&nbsp; 💻 Computer: **{st.session_state.computer_score}**")

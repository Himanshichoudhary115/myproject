import streamlit as st
import pickle
import cv2
import numpy as np
import mediapipe as mp
import time
import json
from streamlit_lottie import st_lottie

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
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# ------------------------ Init Session State ------------------------
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0

# ------------------------ Game Page ------------------------
st.title("🎮 Let's Play!")
st.markdown("Make a gesture in front of your webcam (✊, ✋, ✌️) to play against the computer.")

# ------------------------ Start Game ------------------------
if st.button("🚀 Start Game"):
    cap = cv2.VideoCapture(0)
    options = ["rock", "paper", "scissors"]
    player_move = None

    stframe = st.empty()
    result_text = st.empty()
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            landmarks = results.multi_hand_landmarks[0].landmark
            data = [lm.x for lm in landmarks] + [lm.y for lm in landmarks] + [lm.z for lm in landmarks]
            prediction = model.predict([data])[0]
            player_move = prediction.lower()

            cv2.putText(frame, f"You: {player_move}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        stframe.image(frame, channels="BGR", use_container_width=True)

        if time.time() - start_time > 7:
            break

    cap.release()
    cv2.destroyAllWindows()

    # ------------------------ Result Section ------------------------
    if player_move is None:
        result_text.error("🙁 Could not detect your move. Try again!")
    else:
        computer_move = np.random.choice(options)
        result_text.markdown(f"🧍 You chose: **{player_move.capitalize()}**")
        result_text.markdown(f"💻 Computer chose: **{computer_move.capitalize()}**")

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

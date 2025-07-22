import streamlit as st

st.title("📊 Scoreboard")

# Initialize scores if not set
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0

# Display current score
st.metric("🧍 You", st.session_state.player_score)
st.metric("💻 Computer", st.session_state.computer_score)

# Reset button
if st.button("🔄 Reset Scores"):
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.success("Scores reset!")

import cv2
import mediapipe as mp
import numpy as np
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

gesture = input("Enter gesture label (rock/paper/scissors): ")

cap = cv2.VideoCapture(0)

data = []

print("Collecting data... Press 'q' to quit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            features = []
            for lm in hand_landmarks.landmark:
                features.extend([lm.x, lm.y, lm.z])
            data.append(features + [gesture])

    cv2.imshow("Data Collection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save to CSV
with open('gesture_data.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

print(f"Saved {len(data)} samples for gesture: {gesture}")

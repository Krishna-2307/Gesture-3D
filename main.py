import cv2
import mediapipe as mp
import numpy as np
import math

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Circle object
circle_pos = [300, 300]
circle_radius = 40
dragging = False

def distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get thumb tip and index tip
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_point = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_point = (int(index_tip.x * w), int(index_tip.y * h))

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw pinch line
            cv2.line(frame, thumb_point, index_point, (0, 255, 0), 2)

            # Detect pinch
            dist = distance(thumb_point, index_point)
            is_pinching = dist < 40  # Threshold

            # If pinching and finger over object, enable dragging
            if is_pinching:
                avg_x = int((thumb_point[0] + index_point[0]) / 2)
                avg_y = int((thumb_point[1] + index_point[1]) / 2)

                if not dragging:
                    # Check if pinch is inside the circle
                    if distance((avg_x, avg_y), circle_pos) < circle_radius:
                        dragging = True

                if dragging:
                    circle_pos = [avg_x, avg_y]
            else:
                dragging = False

    # Draw virtual object (replace with OpenGL cube later)
    cv2.circle(frame, tuple(circle_pos), circle_radius, (255, 0, 0), -1)

    # Display
    cv2.putText(frame, 'Pinch to Drag the Object', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Hand Tracking - Pinch to Move", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

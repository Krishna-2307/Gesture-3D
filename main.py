import cv2
import mediapipe as mp
import numpy as np
import math

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2,  # Allow up to 2 hands
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Draggable circle object
circle_pos = [300, 300]
circle_radius = 40
dragging = False

# UI state for start menu (glassmorphic UI as previously set up)
start_menu_open = False
finger_over_start = False

# UI Dimensions for taskbar and start button
taskbar_height = 50
start_btn_rect = (20, -taskbar_height + 10, 40, 40)  # (x, y-from-bottom, width, height)

def distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

def point_in_rect(point, rect, frame_height):
    x, y, w, h = rect
    # Convert y-from-bottom to actual top-left coordinates
    rect_top_left = (x, frame_height + y)
    rect_bottom_right = (x + w, frame_height + y + h)
    return (rect_top_left[0] <= point[0] <= rect_bottom_right[0] and
            rect_top_left[1] <= point[1] <= rect_bottom_right[1])

# Start webcam and set to full screen
cap = cv2.VideoCapture(0)
cv2.namedWindow("Hand Tracking - Pinch to Move", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Hand Tracking - Pinch to Move", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip and get frame dimensions
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # List to accumulate all active pinch centers from both hands
    active_pinches = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get thumb and index fingertip positions
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_point = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_point = (int(index_tip.x * w), int(index_tip.y * h))

            # Draw landmarks and pinch line
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.line(frame, thumb_point, index_point, (0, 255, 0), 2)

            # Determine if this hand is pinching
            dist = distance(thumb_point, index_point)
            is_pinching = dist < 40  # pinch threshold

            if is_pinching:
                # Calculate the midpoint between the thumb and index finger
                avg_x = int((thumb_point[0] + index_point[0]) / 2)
                avg_y = int((thumb_point[1] + index_point[1]) / 2)
                active_pinches.append((avg_x, avg_y))

    # If at least one hand is pinching, update dragging
    if active_pinches:
        # If not already dragging, check if any pinch is inside the circle
        if not dragging:
            for pinch_center in active_pinches:
                if distance(pinch_center, circle_pos) < circle_radius:
                    dragging = True
                    break

        # While dragging, update circle position as the average of all active pinch centers
        if dragging:
            avg_x = int(sum(p[0] for p in active_pinches) / len(active_pinches))
            avg_y = int(sum(p[1] for p in active_pinches) / len(active_pinches))
            circle_pos = [avg_x, avg_y]
    else:
        dragging = False  # No pinch active on any hand, stop dragging

    # Draw the draggable circle
    cv2.circle(frame, tuple(circle_pos), circle_radius, (255, 0, 0), -1)

    # --- Glassmorphic Taskbar Overlay ---
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - taskbar_height), (w, h), (255, 255, 255), -1)
    frame = cv2.addWeighted(overlay, 0.15, frame, 0.85, 0)

    # --- Rounded Start Button (Translucent White with Curved Edges) ---
    btn_x, btn_y, btn_w, btn_h = start_btn_rect
    btn_top_left = (btn_x, h + btn_y)
    btn_bottom_right = (btn_x + btn_w, h + btn_y + btn_h)
    center = (btn_top_left[0] + btn_w // 2, btn_top_left[1] + btn_h // 2)

    btn_overlay = frame.copy()
    cv2.rectangle(btn_overlay, btn_top_left, btn_bottom_right, (255, 255, 255), -1)
    cv2.circle(btn_overlay, center, btn_w // 2, (255, 255, 255), -1)
    frame = cv2.addWeighted(btn_overlay, 0.4, frame, 0.6, 0)

    # --- Start Button Hover Toggle with Debounce ---
    if active_pinches and not dragging:
        # Use the first pinch point for button detection (could also average if needed)
        test_point = active_pinches[0]
        currently_over = point_in_rect(test_point, start_btn_rect, h)
        if currently_over and not finger_over_start:
            start_menu_open = not start_menu_open
            finger_over_start = True
        elif not currently_over:
            finger_over_start = False

    # --- Start Menu (Simple Translucent Box) ---
    if start_menu_open:
        menu_width, menu_height = 280, 350
        menu_top_left = (btn_top_left[0], btn_top_left[1] - menu_height)
        menu_bottom_right = (menu_top_left[0] + menu_width, btn_top_left[1])
        menu_overlay = frame.copy()
        cv2.rectangle(menu_overlay, menu_top_left, menu_bottom_right, (150, 200, 255), -1)
        frame = cv2.addWeighted(menu_overlay, 0.25, frame, 0.75, 0)

        # Close menu if finger taps outside the menu and start button areas
        if active_pinches:
            test_point = active_pinches[0]
            in_menu = point_in_rect(test_point, (menu_top_left[0], menu_top_left[1], menu_width, menu_height), 0)
            in_button = point_in_rect(test_point, start_btn_rect, h)
            if not in_menu and not in_button:
                start_menu_open = False

    # Instructional text
    cv2.putText(frame, 'Pinch to Drag the Object', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Hand Tracking - Pinch to Move", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

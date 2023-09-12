import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

gesture_threshold = 0.1
prev_gesture = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            index_finger = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]

            x_index = int(index_finger.x * screen_width)
            y_index = int(index_finger.y * screen_height)
            x_middle = int(middle_finger.x * screen_width)
            y_middle = int(middle_finger.y * screen_height)
            x_ring = int(ring_finger.x * screen_width)
            y_ring = int(ring_finger.y * screen_height)

            # Calculate distance between fingers
            distance = ((x_middle - x_index) ** 2 + (y_middle - y_index) ** 2) ** 0.5

            # Left-click gesture: Index and middle fingers close
            if index_thumb_distance < gesture_threshold * screen_width and middle_thumb_distance < gesture_threshold * screen_width:
                if prev_gesture != "left_click":
                    pyautogui.click()
                    prev_gesture = "left_click"

            # Double-click gesture: Index finger tip near ring finger tip
            if ((x_ring - x_index) ** 2 + (y_ring - y_index) ** 2) ** 0.5 < gesture_threshold * screen_width:
                if prev_gesture != "double_click":
                    pyautogui.doubleClick()
                    prev_gesture = "double_click"

            # Scrolling gestures: Ring finger down (scroll down) or up (scroll up)
            if y_ring > y_index:
                if prev_gesture != "scroll_down":
                    pyautogui.scroll(-1)
                    prev_gesture = "scroll_down"
            else:
                if prev_gesture != "scroll_up":
                    pyautogui.scroll(1)
                    prev_gesture = "scroll_up"

            # Zoom gestures: Middle finger down (zoom out) or up (zoom in)
            if y_middle > y_index:
                if prev_gesture != "zoom_out":
                    pyautogui.keyDown('ctrl')
                    pyautogui.scroll(-1)
                    pyautogui.keyUp('ctrl')
                    prev_gesture = "zoom_out"
            else:
                if prev_gesture != "zoom_in":
                    pyautogui.keyDown('ctrl')
                    pyautogui.scroll(1)
                    pyautogui.keyUp('ctrl')
                    prev_gesture = "zoom_in"

            pyautogui.moveTo(x_middle, y_middle)

    cv2.imshow('Gesture Control Mouse', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

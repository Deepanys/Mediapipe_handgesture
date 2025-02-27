import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize MediaPipe Face Detection and Hands
mp_face_detection = mp.solutions.face_detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Function to detect visible fingers and their direction
def get_finger_directions(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    finger_mcp = [2, 5, 9, 13, 17]  # MCP joints for each finger
    fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    visible = []
    directions = {}
    
    for i, tip in enumerate(finger_tips):
        tip_x, tip_y = hand_landmarks.landmark[tip].x, hand_landmarks.landmark[tip].y
        base_x, base_y = hand_landmarks.landmark[finger_mcp[i]].x, hand_landmarks.landmark[finger_mcp[i]].y
        
        if fingers[i] == "Thumb":  # Special handling for thumb angle
            tip_x, tip_y = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
            base_x, base_y = hand_landmarks.landmark[2].x, hand_landmarks.landmark[2].y
            wrist_x, wrist_y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
            
            # Calculate the angle between the thumb and the index base using atan2
            dx1, dy1 = tip_x - base_x, tip_y - base_y
            dx2, dy2 = wrist_x - base_x, wrist_y - base_y
            angle = math.degrees(math.atan2(dy1, dx1) - math.atan2(dy2, dx2))
            
            # Normalize angle to range [-180, 180]
            angle = (angle + 360) % 360
            if angle > 180:
                angle -= 360
            
            if angle > 125 and angle < 175:
                direction = "Up"
            else:
                direction = "Down"

            # direction = f"A:{angle}"
        else:
            if tip_y < base_y:
                direction = "Up"
            elif tip_y > base_y:
                direction = "Down"
            elif tip_x > base_x:
                direction = "Right"
            else:
                direction = "Left"
        
        directions[fingers[i]] = direction
        visible.append(fingers[i])
    
    return directions if visible else {"None": "None"}

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set up face detection and hand tracking models
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection, \
     mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=1) as hands:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Convert frame to RGB (MediaPipe requires RGB input)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process face detection
        face_results = face_detection.process(frame_rgb)
        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                             int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Create a larger canvas
            canvas_width = frame.shape[1] + 300
            canvas_height = max(frame.shape[0], 500)
            canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255
            canvas[:frame.shape[0], :frame.shape[1]] = frame
            y_offset = 50  # Starting Y position for text display

            # Process hand detection
            hand_results = hands.process(frame_rgb)
            detected_left_hand = False
            
            if hand_results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                    hand_label = handedness.classification[0].label  # "Right" or "Left"
                    mp_drawing.draw_landmarks(canvas[:frame.shape[0], :frame.shape[1]], hand_landmarks, mp_hands.HAND_CONNECTIONS) 
                    if hand_label == "Left":
                        detected_left_hand = True
                        finger_directions = get_finger_directions(hand_landmarks)
                        for finger, direction in finger_directions.items():
                            if hand_label == "Left":
                                cv2.putText(canvas, f"RIGHT {finger}: {direction}", (frame.shape[1] + 10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 20), 2)
                                y_offset += 30  # Move text down for next line
                        print(f"{hand_label} Hand - Finger directions: {finger_directions}")
            
            if not detected_left_hand:
                cv2.putText(canvas, "No valid hand detected,", (frame.shape[1] + 10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(canvas, "Use RIGHT hand", (frame.shape[1] + 10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print("No valid hand detected")
            
            # Display output
            cv2.imshow("AI Face & Hand Recognition", canvas)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()

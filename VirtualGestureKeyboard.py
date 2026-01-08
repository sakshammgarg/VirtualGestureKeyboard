import cv2
import numpy as np
import mediapipe as mp
import time

# ===================== MediaPipe =====================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ===================== Keyboard Layout =====================
KEY_ROWS = [
    ["Q","W","E","R","T","Y","U","I","O","P","BACK"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Z","X","C","V","B","N","M"],
    ["SPACE"]
]

KEY_W, KEY_H = 70, 70
SPACING = 15
BACK_W = KEY_W * 2 + SPACING
SPACE_W = KEY_W * 6 + SPACING * 5

# ===================== Colors =====================
WHITE = (255,255,255)
BLACK = (0,0,0)
HOVER = (0,255,255)
PRESS = (0,255,0)
TEXT_COLOR = (255,0,0)

# ===================== Globals =====================
output_text = ""
pressed_key = None
pinch_active = False       # GLOBAL pinch lock
last_space_time = 0

# ===================== Keyboard Builder =====================
def build_keyboard(frame_w, frame_h):
    layout = []
    start_y = frame_h - 360
    row_offsets = [0, KEY_W//2, KEY_W, KEY_W*2]

    for row_idx, row in enumerate(KEY_ROWS):
        y = start_y + row_idx * (KEY_H + SPACING)
        x = (frame_w - 11 * (KEY_W + SPACING)) // 2 + row_offsets[row_idx]

        for key in row:
            w = KEY_W
            if key == "BACK":
                w = BACK_W
            elif key == "SPACE":
                w = SPACE_W

            layout.append((key, x, y, w, KEY_H))
            x += w + SPACING

    return layout

# ===================== Drawing =====================
def draw_keyboard(img, layout, hover=None, pressed=None):
    for key, x, y, w, h in layout:
        color = WHITE
        if key == hover:
            color = HOVER
        if key == pressed:
            color = PRESS

        cv2.rectangle(img, (x,y), (x+w,y+h), color, -1)
        cv2.rectangle(img, (x,y), (x+w,y+h), BLACK, 2)

        label = "SPACE BAR" if key == "SPACE" else "BACK" if key == "BACK" else key
        cv2.putText(img, label, (x+10,y+45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, BLACK, 2)

# ===================== Utils =====================
def get_key_at(x, y, layout):
    for key, kx, ky, kw, kh in layout:
        if kx <= x <= kx+kw and ky <= y <= ky+kh:
            return key
    return None

def is_pinch(hand, threshold=0.04):
    idx = hand.landmark[8]
    thumb = hand.landmark[4]
    return np.hypot(idx.x-thumb.x, idx.y-thumb.y) < threshold

def apply_key(key):
    global output_text, last_space_time
    if key == "SPACE":
        output_text += " "
        last_space_time = time.time()
    elif key == "BACK":
        output_text = output_text[:-1]
    else:
        output_text += key

# ===================== Main =====================
def main():
    global pressed_key, pinch_active

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    keyboard = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        if keyboard is None:
            keyboard = build_keyboard(w, h)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        hover_key = None
        pinch_detected_this_frame = False

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                lm = hand.landmark[8]
                cx, cy = int(lm.x * w), int(lm.y * h)
                key = get_key_at(cx, cy, keyboard)

                if key:
                    hover_key = key

                if key and is_pinch(hand):
                    pinch_detected_this_frame = True

                    if not pinch_active:
                        apply_key(key)
                        pressed_key = key
                        pinch_active = True
                        break  # prevent second hand from firing

        # Reset pinch lock ONLY when no hand is pinching
        if not pinch_detected_this_frame:
            pinch_active = False
            pressed_key = None

        draw_keyboard(frame, keyboard, hover_key, pressed_key)

        # Display text + cursor
        display_text = output_text + "|"
        cv2.putText(frame, display_text, (50, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, TEXT_COLOR, 3)

        # Space feedback
        if time.time() - last_space_time < 0.3:
            cv2.putText(frame, "[SPACE]", (50, 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.imshow("Advanced Virtual Keyboard", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
# Advanced Virtual Gesture Keyboard

A real-time gesture-controlled virtual keyboard that allows users to type using hand gestures instead of a physical keyboard. Built using MediaPipe and OpenCV, this project implements a realistic QWERTY keyboard layout with reliable pinch-based input, supporting both left and right hands while preventing accidental double presses.

---

## Features

- Gesture-based typing using thumb–index pinch
- Dual-hand support (left & right hand)
- Pinch-lock mechanism to avoid simultaneous double taps
- Accurate QWERTY keyboard layout
- Dedicated SPACE BAR and BACKSPACE
- Hover and press visual feedback
- Live cursor indicator to show spacing clearly
- Real-time performance with low latency

---

## How It Works

1. Webcam captures live video feed
2. MediaPipe detects hand landmarks (21 points per hand)
3. Index fingertip determines the hovered key
4. Thumb–index pinch confirms key selection
5. A global pinch lock ensures only one keypress per gesture
6. OpenCV renders the keyboard and typed text in real time

---

## Tech Stack

- **Python 3.10**
- **MediaPipe** – Hand landmark detection
- **OpenCV** – Video capture and rendering
- **NumPy** – Distance and geometry calculations

---

## Installation

> **Note:** This project is intended to run locally (not on Google Colab).

### 1. Create a virtual environment

```bash
python3.10 -m venv vk_env
source vk_env/bin/activate
```

### 2. Install dependencies

```bash
pip install mediapipe==0.10.x opencv-python numpy
```

---

## Running the Project

```bash
python virtual_keyboard.py
```

- Press **ESC** to exit the application
- Ensure good lighting for best hand tracking accuracy

---

## Use Cases

- Human–Computer Interaction (HCI) projects
- Gesture-based accessibility systems
- Touchless input interfaces
- Computer vision demonstrations
- Academic / final-year engineering projects

---

## Gesture Rules

| Gesture Scenario | Result |
|-----------------|--------|
| Left-hand pinch | Key registered |
| Right-hand pinch | Key registered |
| Both hands pinch together | Only one key registered |
| Holding pinch | No repeated presses |
| Release + pinch again | New key registered |

---

## ✋🎮 Gesture3D — Real-Time Hand Gesture Controlled 3D Interaction

---

### 🧠 Overview

**Gesture3D** is a Python desktop application that transforms your hand into a virtual controller. Using just a standard webcam, you can **pinch, grab, rotate, and move a 3D object on your screen** — all with natural hand gestures.

Built using [MediaPipe](https://google.github.io/mediapipe/solutions/hands.html) for AI-based hand tracking, **Gesture3D** aims to deliver an intuitive, controller-free interface for interacting with 3D virtual objects in real time.

---

### ✨ Features

* 📸 Real-time hand landmark tracking via webcam
* 🤏 Pinch gesture detection to "grab" objects
* 🧊 Move and rotate a virtual 3D cube with your hand
* 🔄 Wrist twist detection for natural object rotation
* ⚡ Responsive and lightweight — no gloves or sensors needed

---

### 📦 Tech Stack

* Python 3.8+
* MediaPipe Hands
* OpenCV
* PyOpenGL + Pygame or Vispy (for 3D rendering)
* Numpy

---

### 🚀 Getting Started

#### 1. Clone the repository

```bash
git clone https://github.com/CraigDaGama/Gesture-3D.git
cd Gesture3d
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> `requirements.txt`:

```text
mediapipe
opencv-python
numpy
PyOpenGL
pygame
```

#### 3. Run the app

```bash
python gesture3d/main.py
```

---

### 🧠 How It Works

| Gesture                   | Action               |
| ------------------------- | -------------------- |
| Pinch (thumb + index tip) | Grab the object      |
| Move hand while pinching  | Move object position |
| Twist wrist               | Rotate the 3D object |
| Release pinch             | Drop the object      |

### 📜 License

MIT License — free to use, modify, and share.

---

### 🤝 Contributing

Contributions, feedback, and ideas are welcome! Please open an issue or pull request to discuss improvements.


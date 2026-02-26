# 🚦 AI-Based Smart Traffic Control System

An AI-powered adaptive traffic signal control system that dynamically adjusts signal timing based on real-time vehicle density using YOLOv8 and OpenCV.

This project simulates a 4-road junction with multi-camera inputs and a modern Smart Traffic Command Center dashboard.

---

## 📌 Project Overview

Traditional traffic signals operate on fixed timers, which often lead to:

- Unnecessary waiting time
- Traffic congestion
- Poor traffic flow efficiency

This system solves that by:

- Detecting vehicles in real-time
- Estimating traffic density per direction
- Dynamically allocating green signal duration
- Ensuring fairness across all directions

---

## 🧠 Core Features

- 🚗 Real-time vehicle detection using YOLOv8
- 🎥 Multi-camera (4-direction) junction support
- 📊 Density-based adaptive signal timing
- ⚖ Fairness logic to prevent signal starvation
- 🖥 Modern Smart Traffic Command Center UI
- ⚙ Modular architecture (Detection, Control, UI, Config)
- 📝 Logging and configuration management
- 📦 Clean project structure

---

## 🏗 Architecture

Video Feeds
↓
YOLO Vehicle Detection
↓
Traffic Density Calculation
↓
Junction Controller (Adaptive Logic)
↓
Dashboard UI Rendering

---

## 🛠 Tech Stack

- Python 3.10+
- OpenCV
- YOLOv8 (Ultralytics)
- NumPy
- Modular OOP Architecture

---

## 📂 Project Structure
smart-traffic-ai/
│
├── detection/
│ ├── vehicle_detector.py
│ └── visualization.py
│
├── junction/
│ └── junction_controller.py
│
├── ui/
│ └── dashboard.py
│
├── video/
│ └── video_manager.py
│
├── config.py
├── main.py
├── requirements.txt
└── .gitignore

---

## ⚙ Installation

### 1️⃣ Clone the Repository
git clone https://github.com/gottampavan7-pixel/smart-traffic-ai.git
cd smart-traffic-ai


### 2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate


### 3️⃣ Install Dependencies
pip install -r requirements.txt


---

## 📥 Required Files (Not Included in Repo)

Due to size limitations, model weights and video files are not included.

### Download YOLOv8 model:
Place `yolov8n.pt` in the root directory.

### Add sample traffic videos:
Create a folder named:
videos/


Add:
- north.mp4
- east.mp4
- south.mp4
- west.mp4

---

## ▶ Run the System
python main.py


---

## 📊 System Capabilities

- Real-time vehicle counting
- Congestion classification (LOW / MEDIUM / HIGH)
- Adaptive green signal duration
- Live FPS and detection timing
- Visual signal state display

---

## 🚀 Future Improvements

- Yellow transition phase
- Object tracking (unique vehicle counting)
- GPU acceleration
- Historical traffic analytics
- Real-world hardware integration

---

## 📸 Demo

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/22279fd8-90fa-4b4d-8ccc-d29a1e9d11ac" />


---

## 📄 License

This project is developed for educational and research purposes.

---

## 👨‍💻 Author

**Pavan Gottam**  
B.Tech CSE (AI & ML)  
AI / Computer Vision Enthusiast

---

⭐ If you found this project interesting, consider starring the repository!

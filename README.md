# HeartBeat AI

<p align="center">
  <img src="https://github.com/user-attachments/assets/f49c337a-3026-4fb7-89e5-89fb607e595e" 
       alt="Gemini_Generated_Image_qfkfx6qfkfx6qfkf" 
       width="50%" />
  <br>
  <strong>A Vision-based AI fall detection and emergency response system for solo-living seniors.</strong>
</p>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#project-description">Project Description</a></li>
    <li><a href="#key-features">Key Features</a></li>
    <li><a href="#how-it-works">How it Works</a></li>
    <li><a href="#objectives">Objectives</a></li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#future-roadmap">Future Roadmap</a></li>
  </ol>
</details>

---

## Project Description

**HeartBeat AI** is an edge-computing software layer designed to identify "Critical Falls" using existing CCTV infrastructure. It addresses the **"Long Lie"**—the dangerous time gap between an undetected fall and the arrival of help. 

Unlike invasive wearables, HeartBeat uses **Pose Estimation** to process mathematical skeletal data instead of raw video, ensuring user privacy. The system transforms passive monitoring into an active response node by integrating real-time computer vision with a hands-free voice verification loop.

---

## 👁️ Key Features

* **Skeletal Detection**: Uses 2D coordinate tracking to identify fall trajectories without storing or transmitting personal visual data.
* **Protocol Interoperability**: Engineered to interface with standard IP cameras via **RTSP** and **ONVIF** protocols.
* **Verification Loop**: Minimizes false positives by initiating an automated voice dialogue to confirm the user's status.
* **Edge-First Logic**: Designed for local inference to reduce latency and comply with strict data privacy standards.

---

## 🛠️ How It Works

### 1. Stream Ingestion & Analysis 📊
The system targets raw video feeds via **RTSP/ONVIF**. The logic analyzes the vertical velocity ($\Delta y / \Delta t$) of the torso. A "fall event" is flagged when the rate of descent exceeds a calibrated threshold, followed by a static period at floor level.

### 2. Voice-Based Confirmation (STT) 🗣️
Upon detection, the system triggers a **Text-to-Speech (TTS)** query: *"Fall detected. Are you okay?"* It then opens a **Speech-to-Text (STT)** window for 60 seconds to capture specific verbal cues like "I'm fine" or "Help." 

### 3. Escalation & Alerts ⚠️
If the system registers **continued silence** (no verbal input) or a distress keyword, it bypasses the need for manual intervention. A high-priority alert is dispatched to the **Streamlit-based caregiver dashboard**, providing immediate status updates.

---

## 🎯 Objectives

* **Zero-Wearable Reliability**: Eliminate the "human error" factor of forgotten or uncharged wearable devices.
* **Universal Deployment**: Create a blueprint that works with existing $20 IP cameras as effectively as professional systems.
* **Privacy-by-Design**: Ensure that only anonymous coordinate data is used for fall analysis, never raw faces or identifiable footage.

---

## 💻 Tech Stack

| Category | Technology |
| :--- | :--- |
| **Logic & Control** | Python |
| **Frontend** | Streamlit |
| **UX/UI Prototyping** | Figma (HCI Standards) |
| **Vision Logic** | MediaPipe & OpenCV (Architectural Blueprint) |
| **Audio Interaction** | SpeechRecognition (STT) & Pyttsx3 (TTS) |
| **Protocols** | RTSP, ONVIF (Simulation Logic) |

---

## 🚀 Future Roadmap

- [ ] **EVM Integration**: Implementing Eulerian Video Magnification to detect pulse rates via skin micro-color changes.
- [ ] **Thread Optimization**: Refining Python concurrency to reduce the latency between CV detection and STT activation.
- [ ] **Containerization**: Packaging the logic as a Docker service for deployment on local NAS or Raspberry Pi.

---

> "Because when it comes to the people we love, silence should never be the final answer."

# 🎙 AudioText – Voice-to-Text Recorder

AudioText is a simple voice-to-text application written in Python.  
It listens to your microphone and converts speech into text.  
Recording starts when you say **“START MY FRIEND”** 
and stops when you say **“FINISH MY FRIEND”** —  
after that, the program automatically saves everything and exits.

---

## 🚀 Features

- 🎧 Real-time voice recognition (English)
- 🗣️ Start/stop recording using voice commands
- 💾 Automatically logs recognized text with timestamps
- ⚙️ Lightweight – uses only `SpeechRecognition` and `PyAudio`

---

## 🧰 Installation & Setup

### 1. Clone the repository

`git clone https://github.com/mathewtroy/audiotext.git`

### 2. Select root package
`cd audiotext`

### 3. Install dependencies**
`pip install -r requirements.txt`

### 4. Run the program**
`python main.py`

---

## 🧾 Logs

All recognized text and system events are written to a file named logs.txt.
Each line has a timestamp, log level, and message.

---


## 🧑‍💻 Author : Aleksandr Kross **[📧](mailto:krossale@fel.czut.cz)**
**[GitHub](https://github.com/mathewtroy)**



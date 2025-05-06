# 🎸 Live Tonation Classification

**Live Tonation Classification** is a real-time key (tonality) detection system for musical audio, designed for musicians, music technologists, and audio hackers. It analyzes live audio input (e.g., from a guitar, keyboard, or microphone), detects the dominant notes, and predicts the musical key (major/minor) on the fly. The project features a modern Tkinter GUI for instant feedback and is built with modular, readable Python code.

---

## 🚀 Features

- Real-time audio streaming and processing
- Automatic key (tonality) detection (major/minor)
- Live note histogram for visualization and debugging
- Tkinter GUI for easy use and instant feedback
- Modular codebase: easy to extend, hack, or integrate
- Customizable detection window and analysis interval
- Cross-platform (Linux, Windows, macOS)

---

## 🖥️ GUI Preview

<!-- Add your screenshot here -->
<!-- ![GUI Preview](https://user-images.githubusercontent.com/your-github-username/your-screenshot.png) -->
*Example: The app showing detected key and mode in real time.*

---

## 🛠️ Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-github-username/liveTonationClassification.git
    cd liveTonationClassification
    ```

2. **Install dependencies**
    ```bash
    pip install numpy sounddevice
    ```
    *(You may also need `tkinter`, which is included with most Python installations.)*

---

## 🎹 Usage

### Run the GUI application

```bash
python main.py
```

- Click **Start Detection** to begin analyzing audio from your default input device (microphone, audio interface, etc.).
- The detected key and mode will update live in the window.
- Click **Stop Detection** to end the session.

### Run from terminal (no GUI)

```bash
python audio/stream.py
```

---

## 🧩 Project Structure

```
liveTonationClassification/
│
├── audio/
│   ├── stream.py           # Audio streaming & processing logic
│   ├── preprocessing.py    # Audio preprocessing utilities
│
├── model/
│   └── keyClassifier.py    # Core key detection logic
│
├── signalProcessing/
│   ├── pitchDetection.py   # Pitch detection from audio frames
│   └── fastFourierTransform.py # FFT utilities
│
├── windowApplication/
│   └── windowApplication.py # Tkinter GUI
│
├── main.py                 # GUI entry point
└── README.md
```

---

## 🧠 How it works

- Audio is streamed from your input device and split into frames.
- Pitch detection is performed on each frame using FFT.
- Detected notes are mapped to a histogram (C, C#, D, ..., B).
- Key classification uses custom templates for major/minor keys and a sliding window for robust detection.
- Results are displayed live in the GUI.

---

## 🎸 Example Use Cases

- Practice tool for musicians to check if they're staying in key
- Live music analysis for jam sessions or improvisation
- Educational tool for music theory classes
- Audio research and prototyping

---

## 📝 TODO / Ideas

- [ ] Add chord detection
- [ ] Visualize note histogram in the GUI
- [ ] Support for multiple audio input devices
- [ ] Export analysis results to file
- [ ] Add support for more scales/modes

---

## 🤝 Contributing

Pull requests, issues, and feature suggestions are welcome!  
Feel free to fork and hack away.

---

## 📄 License

MIT License

---

## 🙏 Credits

- [numpy](https://numpy.org/)
- [sounddevice](https://python-sounddevice.readthedocs.io/)
- [Tkinter](https://wiki.python.org/moin/TkInter)

---

> Made with ❤️ for live music and code.

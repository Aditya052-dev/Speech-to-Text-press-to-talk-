# Speech-to-Text-press-to-talk-
A simple Python script for real-time audio transcription. Press and hold the spacebar to record your voice, and release to have it instantly transcribed to text using the high-accuracy faster-whisper library. All transcriptions are automatically saved to a log file.
# Real-Time Audio Transcription with Faster-Whisper

A simple yet powerful Python script that provides real-time, "press-to-talk" audio transcription using the `faster-whisper` library. Just press and hold the spacebar to dictate, and release to see the transcription appear in your terminal.



---

## ✨ Features

* **Press-to-Talk Interface**: Simple and intuitive recording controlled by holding and releasing the **spacebar**.
* **High-Accuracy Transcription**: Leverages the state-of-the-art `large-v3` Whisper model via the highly optimized `faster-whisper` library for top-tier accuracy.
* **CPU Optimized**: Designed to run efficiently on a standard CPU using `int8` quantization, making it accessible without a dedicated GPU.
* **Automatic Logging**: Saves every transcription with a timestamp to a `transcription_log.txt` file for your records.
* **Lightweight & Cross-Platform**: Built with minimal dependencies that support Windows, macOS, and Linux.

---

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

* **Python 3.8+**
* **PortAudio**: The `sounddevice` library requires this for audio I/O.
    * **Windows & macOS**: PortAudio is usually included with Python's installers.
    * **Linux (Debian/Ubuntu)**: You may need to install it manually:
        ```sh
        sudo apt-get install libportaudio2
        ```

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Create a `requirements.txt` file** with the following content:
    ```txt
    sounddevice
    numpy
    scipy
    pynput
    faster-whisper
    ```

4.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    *Note: The first time you run the script, `faster-whisper` will download the `large-v3` model files, which may take some time and require a stable internet connection.*

---

## 🎤 How to Use

1.  **Run the script from your terminal:**
    ```sh
    python speech.py
    ```

2.  You will see the message: `Press and hold the spacebar to record audio. Release to stop and transcribe.`

3.  **Press and hold the spacebar** to start recording your voice.

4.  **Release the spacebar** to stop. The script will immediately process the audio and print the transcription to the console.

5.  The transcription will also be appended to the `transcription_log.txt` file in the same directory.

---

## ⚙️ Configuration

You can easily change the Whisper model size to balance between speed and accuracy. Smaller models are faster but less accurate.

1.  Open the `speech.py` file.
2.  Locate this line in the `__init__` method of the `FasterWhisperTranscriber` class:
    ```python
    def __init__(self, model_size="large-v3", sample_rate=16000):
    ```
3.  Change the `model_size` default value from `"large-v3"` to one of the following options:
    * `"tiny"`
    * `"base"`
    * `"small"`
    * `"medium"`
    * `"large-v2"` (as an alternative to v3)

**Example for a faster, less accurate model:**
```python
def __init__(self, model_size="base", sample_rate=16000):
```

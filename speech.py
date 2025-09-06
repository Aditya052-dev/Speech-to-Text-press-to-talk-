import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pynput.keyboard as keyboard
import tempfile
import os
import threading
from faster_whisper import WhisperModel
from datetime import datetime  # Import the datetime module

class FasterWhisperTranscriber:
    def __init__(self, model_size="large-v3", sample_rate=16000):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        
        self.is_recording = False
        self.frames = []
        self.recording_thread = None
        # Define the name of the log file
        self.log_file = "transcription_log.txt"

    def _record_loop(self):                                      
        """The loop that runs in a separate thread to capture audio."""
        channels = 1
        blocksize = int(self.sample_rate / 10) # 100ms frames

        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=channels, dtype='int16', blocksize=blocksize) as stream:
                while self.is_recording:
                    frame, _ = stream.read(blocksize)
                    self.frames.append(frame)
        except Exception as e:
            print(f"An error occurred during recording: {e}")

    def on_press(self, key):
        """Callback function for key press events."""
        if key == keyboard.Key.space and not self.is_recording:
            print("Recording started...")
            self.is_recording = True
            self.frames.clear()
            self.recording_thread = threading.Thread(target=self._record_loop)
            self.recording_thread.start()

    def on_release(self, key):
        """Callback function for key release events."""
        if key == keyboard.Key.space and self.is_recording:
            print("Recording stopped. Transcribing...")
            self.is_recording = False
            if self.recording_thread:
                self.recording_thread.join()

            if not self.frames:
                print("No audio recorded.")
                return

            recording = np.vstack(self.frames)
            
            audio_path = self.save_audio(recording)
            transcript = self.transcribe_audio(audio_path)
            
            print("\n--- Transcription ---")
            print(transcript)
            
            # --- NEW: Save the transcription to a file ---
            self.log_transcription(transcript)
            
            print("\nPress and hold the spacebar to record again.")
    

    def log_transcription(self, transcript):
        """Appends the transcription with a timestamp to the log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {transcript}\n")
            print(f"Transcription saved to {self.log_file}")
        except Exception as e:
            print(f"Error saving transcription: {e}")
    
    def save_audio(self, recording):
        """Saves the NumPy audio array to a temporary WAV file."""
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", mode='wb')
        wav.write(temp_wav.name, self.sample_rate, recording)
        temp_wav.close()
        return temp_wav.name
    
    def transcribe_audio(self, audio_path):
        """Transcribes the audio file using the Whisper model."""
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        print(f"Detected language: {info.language} with probability {info.language_probability:.2f}")
        
        full_transcript = " ".join(segment.text for segment in segments)
        
        os.remove(audio_path)
        return full_transcript.strip()
    
    def run(self):
        """Starts the keyboard listener and runs the application."""
        print("Press and hold the spacebar to record audio. Release to stop and transcribe.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    transcriber = FasterWhisperTranscriber()
    transcriber.run()
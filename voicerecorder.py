# voice_recorder.py

import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import wave
import threading

class VoiceRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Recorder")
        self.master.geometry("300x200")
        self.is_recording = False
        self.frames = []

        # Label for recording duration
        self.label = tk.Label(master, text="Recording Duration (seconds):")
        self.label.pack(pady=10)

        # Entry for recording duration
        self.duration_entry = tk.Entry(master)
        self.duration_entry.pack(pady=5)
        self.duration_entry.insert(0, "10")  # Default duration

        # Record button
        self.record_button = tk.Button(master, text="Record", command=self.start_recording)
        self.record_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(master, text="Status: Idle")
        self.status_label.pack(pady=10)

    def start_recording(self):
        # Get the duration from the entry
        try:
            self.record_duration = int(self.duration_entry.get())
            if self.record_duration <= 0:
                raise ValueError("Duration must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        self.is_recording = True
        self.frames = []  # Reset frames for new recording
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Recording...")

        # Start recording in a separate thread
        self.record_thread = threading.Thread(target=self.record)
        self.record_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped")

    def record(self):
        fs = 44100  # Sample rate
        with sd.InputStream(samplerate=fs, channels=2) as stream:
            for _ in range(int(self.record_duration * fs / 1024)):
                if not self.is_recording:
                    break
                data = stream.read(1024)[0]
                self.frames.append(data)

        # Save the recorded data to a WAV file
        self.save_recording()

    def save_recording(self):
        filename = "output.wav"
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(2)  # Stereo
                wf.setsampwidth(2)  # 2 bytes for int16
                wf.setframerate(44100)
                wf.writeframes(b''.join(self.frames))
            self.status_label.config(text=f"Status: Saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save the file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    recorder = VoiceRecorder(root)
    root.mainloop()
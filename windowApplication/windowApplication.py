import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from audio.stream import AudioStreamer
import threading

class KeyDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Detection")
        self.root.geometry("400x200")
        
        self.streamer = AudioStreamer(sample_rate=16000, frame_size=2048, hop_size=512)

        self.key_label = tk.Label(root, text="Current key: Not detected", font=("Arial", 14))
        self.key_label.pack(pady=20)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Detection", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(button_frame, text="Stop Detection", command=self.stop_detection)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.stop_button.config(state=tk.DISABLED)

        self.is_running = False
    
    def start_detection(self):
        self.stream_thread = threading.Thread(target=self.streamer.start_stream)
        self.stream_thread.daemon = True
        self.stream_thread.start()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True

        self.update_display()
    
    def stop_detection(self):
        self.streamer.stop_stream()
        self.streamer.reset_histogram()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False
    
    def update_display(self):
        if self.is_running:
            current_key = self.streamer.current_key
            current_mode = self.streamer.current_mode
            
            if current_key and current_mode:
                self.key_label.config(text=f"Current key: {current_key} {current_mode}")
            else:
                self.key_label.config(text="Current key: Not detected")

            # Debug info
            print(f"Display update - Key: {current_key}, Mode: {current_mode}")
            
            self.root.after(500, self.update_display)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyDetectionApp(root)
    root.mainloop()
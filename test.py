import utils.transport
import utils.session
import tkinter as tk
from PIL import Image, ImageTk 
import os  
import speech_recognition as sr  
import threading 

class OverlayCircle:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.5)
        self.root.geometry("200x200+100+100")

        self.canvas = tk.Canvas(self.root, width=200, height=200)
        self.canvas.pack()
        self.draw_image()

        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.recognizer = sr.Recognizer()
        self.listen_thread = threading.Thread(target=self.listen_to_mic)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        self.text_display = tk.Text(self.root, height=5, width=30)  # Add a Text widget to display recognized text
        self.text_display.pack()  # Pack the Text widget
        self.root.mainloop()

    def draw_image(self):
        image_path = "C:/Users/ACER/Documents/Python/Test AI TOOL/cat.png"
        if os.path.exists(image_path):
            # Open and resize the image
            self.image = Image.open(image_path)
            self.image = self.image.resize((200, 200), Image.LANCZOS)
            
            # Make the canvas transparent
            self.root.attributes('-transparentcolor', 'black')
            self.canvas.configure(bg='black', highlightthickness=-90)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(100, 100, anchor=tk.CENTER, image=self.photo)
        else:
            print("Image not found at the specified path.")

            

    def start_move(self, event):
        self.prev_x = event.x
        self.prev_y = event.y

    def move(self, event):
        x = self.root.winfo_x() + (event.x - self.prev_x)
        y = self.root.winfo_y() + (event.y - self.prev_y)
        self.root.geometry(f"+{x}+{y}")

    def on_close(self):
        self.root.destroy()

    def listen_to_mic(self):
        with sr.Microphone() as source:
            print("Listening continuously... (Press Ctrl+C to stop)")
            self.recognizer.adjust_for_ambient_noise(source, duration=3)
            while True:
                try:
                    print("Waiting for audio...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    print("Audio received, processing...")
                    text = self.recognizer.recognize_google(audio)
                    print(f"Recognized text: {text}")  # Debug print to check recognized text
                    self.text_display.insert(tk.END, f"You said: {text}\n")  # Insert recognized text into the Text widget
                except sr.UnknownValueError:
                    print("Sorry, I could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                except sr.WaitTimeoutError:
                    print("Listening timed out, waiting for audio again...")
                    continue

if __name__ == "__main__":
    OverlayCircle()

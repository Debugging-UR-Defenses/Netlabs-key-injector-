import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

try:
    import pyautogui
except ImportError:
    print("pyautogui not installed. Run: pip install pyautogui")
    exit(1)

class KeyInjectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Injector")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure pyautogui settings
        pyautogui.PAUSE = 0.01  # Small pause between keystrokes
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = ttk.Label(
            main_frame, 
            text="Paste your script below, click Start, then click into your target window.\n"
                 "Typing begins after 5 seconds. Move mouse to top-left corner to abort.",
            wraplength=550
        )
        instructions.pack(pady=(0, 10))
        
        # Text area for script input
        self.text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 12, "bold"))
        self.status_label.pack(pady=(0, 10))
        
        # Countdown label
        self.countdown_var = tk.StringVar(value="")
        self.countdown_label = ttk.Label(main_frame, textvariable=self.countdown_var, font=("Arial", 24, "bold"), foreground="red")
        self.countdown_label.pack(pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start (5s delay)", command=self.start_injection)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_injection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT)
        
        # Typing speed slider
        speed_frame = ttk.Frame(main_frame)
        speed_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(speed_frame, text="Typing delay (ms):").pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=10)
        self.speed_slider = ttk.Scale(speed_frame, from_=1, to=100, variable=self.speed_var, orient=tk.HORIZONTAL, length=200)
        self.speed_slider.pack(side=tk.LEFT, padx=(10, 10))
        self.speed_display = ttk.Label(speed_frame, text="10")
        self.speed_display.pack(side=tk.LEFT)
        self.speed_slider.configure(command=self.update_speed_display)
        
        # Control flag
        self.running = False
        
    def update_speed_display(self, val):
        self.speed_display.config(text=str(int(float(val))))
        
    def start_injection(self):
        script_text = self.text_area.get("1.0", tk.END).rstrip('\n')
        if not script_text.strip():
            self.status_var.set("Error: No text to type!")
            return
            
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.text_area.config(state=tk.DISABLED)
        
        # Start injection in a separate thread
        thread = threading.Thread(target=self.injection_thread, args=(script_text,), daemon=True)
        thread.start()
        
    def injection_thread(self, script_text):
        # Countdown
        for i in range(5, 0, -1):
            if not self.running:
                self.reset_ui()
                return
            self.countdown_var.set(str(i))
            self.status_var.set(f"Starting in {i} seconds... Click into target window!")
            time.sleep(1)
        
        self.countdown_var.set("")
        self.status_var.set("Typing...")
        
        # Set typing interval
        typing_interval = self.speed_var.get() / 1000.0
        pyautogui.PAUSE = typing_interval
        
        try:
            # Type each character
            total_chars = len(script_text)
            for i, char in enumerate(script_text):
                if not self.running:
                    self.status_var.set("Stopped by user")
                    break
                    
                # Use write for regular characters, press for special keys
                if char == '\n':
                    pyautogui.press('enter')
                elif char == '\t':
                    pyautogui.press('tab')
                else:
                    pyautogui.write(char, interval=0)
                    
                # Update progress every 10 characters
                if i % 10 == 0:
                    progress = int((i / total_chars) * 100)
                    self.status_var.set(f"Typing... {progress}%")
                    
            if self.running:
                self.status_var.set("Done!")
        except pyautogui.FailSafeException:
            self.status_var.set("Aborted (failsafe triggered)")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
        finally:
            self.reset_ui()
            
    def reset_ui(self):
        self.running = False
        self.countdown_var.set("")
        self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.text_area.config(state=tk.NORMAL))
        
    def stop_injection(self):
        self.running = False
        self.status_var.set("Stopping...")
        
    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyInjectorApp(root)
    root.mainloop()

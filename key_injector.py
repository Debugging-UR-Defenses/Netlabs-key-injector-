import threading
import time

try:
    import customtkinter as ctk
except ImportError:
    print("customtkinter not installed. Run: pip install customtkinter")
    exit(1)

try:
    import pyautogui
except ImportError:
    print("pyautogui not installed. Run: pip install pyautogui")
    exit(1)

# Knight Agent V4 Color Scheme
COLORS = {
    "bg_dark": "#07070c",
    "bg_card": "#0a0a12",
    "border": "#1a1a2e",
    "text": "#ffffff",
    "text_muted": "#6b7280",
    "accent": "#ef4444",
    "accent_hover": "#dc2626",
    "accent_muted": "#7f1d1d",
    "success": "#22c55e",
}

class KeyInjectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("NetLabs Key Injector")
        self.geometry("650x650")
        self.minsize(500, 550)
        self.configure(fg_color=COLORS["bg_dark"])
        self.resizable(True, True)
        
        # Configure pyautogui
        pyautogui.PAUSE = 0.01
        pyautogui.FAILSAFE = True
        
        # Control flag
        self.running = False
        
        self._build_ui()
        
    def _build_ui(self):
        # Main container
        container = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"])
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 16))
        
        # Logo/Icon
        logo_frame = ctk.CTkFrame(header_frame, fg_color=COLORS["accent_muted"], corner_radius=8, width=40, height=40)
        logo_frame.pack(side="left")
        logo_frame.pack_propagate(False)
        logo_label = ctk.CTkLabel(logo_frame, text="⌨", font=("Segoe UI Emoji", 18), text_color=COLORS["accent"])
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=(12, 0))
        
        title = ctk.CTkLabel(title_frame, text="Key Injector", font=("Segoe UI", 18, "bold"), text_color=COLORS["text"])
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(title_frame, text="NetLabs VM Script Injector", font=("Segoe UI", 11), text_color=COLORS["text_muted"])
        subtitle.pack(anchor="w")
        
        # Instructions card
        instructions_card = ctk.CTkFrame(container, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        instructions_card.pack(fill="x", pady=(0, 16))
        
        instructions_text = ctk.CTkLabel(
            instructions_card,
            text="Paste your script below, click Start, then click into your target window.\nTyping begins after 5 seconds. Move mouse to top-left corner to abort.",
            font=("Segoe UI", 12),
            text_color=COLORS["text_muted"],
            justify="left"
        )
        instructions_text.pack(padx=16, pady=12, anchor="w")
        
        # Text area card
        text_card = ctk.CTkFrame(container, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        text_card.pack(fill="both", expand=True, pady=(0, 16))
        
        self.text_area = ctk.CTkTextbox(
            text_card,
            font=("Consolas", 12),
            fg_color=COLORS["bg_dark"],
            text_color=COLORS["text"],
            border_width=0,
            corner_radius=6,
            height=200
        )
        self.text_area.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Status section
        status_frame = ctk.CTkFrame(container, fg_color="transparent")
        status_frame.pack(fill="x", pady=(0, 16))
        
        self.status_label = ctk.CTkLabel(status_frame, text="Ready", font=("Segoe UI", 13, "bold"), text_color=COLORS["text_muted"])
        self.status_label.pack(side="left")
        
        self.countdown_label = ctk.CTkLabel(status_frame, text="", font=("Segoe UI", 28, "bold"), text_color=COLORS["accent"])
        self.countdown_label.pack(side="right")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(container, fg_color=COLORS["border"], progress_color=COLORS["accent"], height=4, corner_radius=2)
        self.progress_bar.pack(fill="x", pady=(0, 16))
        self.progress_bar.set(0)
        
        # Speed slider section
        speed_card = ctk.CTkFrame(container, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1, border_color=COLORS["border"])
        speed_card.pack(fill="x", pady=(0, 16))
        
        speed_inner = ctk.CTkFrame(speed_card, fg_color="transparent")
        speed_inner.pack(fill="x", padx=16, pady=12)
        
        speed_label = ctk.CTkLabel(speed_inner, text="Typing Delay", font=("Segoe UI", 12), text_color=COLORS["text_muted"])
        speed_label.pack(side="left")
        
        self.speed_value_label = ctk.CTkLabel(speed_inner, text="10 ms", font=("Segoe UI", 12, "bold"), text_color=COLORS["text"])
        self.speed_value_label.pack(side="right")
        
        self.speed_slider = ctk.CTkSlider(
            speed_card,
            from_=1, to=100,
            number_of_steps=99,
            fg_color=COLORS["border"],
            progress_color=COLORS["accent"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            command=self._update_speed_display
        )
        self.speed_slider.set(10)
        self.speed_slider.pack(fill="x", padx=16, pady=(0, 12))
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x")
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶  Start (5s delay)",
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="#ffffff",
            corner_radius=8,
            height=44,
            command=self.start_injection
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=(0, 8))
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="■  Stop",
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["border"],
            hover_color=COLORS["bg_card"],
            text_color=COLORS["text_muted"],
            corner_radius=8,
            height=44,
            state="disabled",
            command=self.stop_injection
        )
        self.stop_button.pack(side="left", expand=True, fill="x", padx=(0, 8))
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            font=("Segoe UI", 13),
            fg_color="transparent",
            hover_color=COLORS["bg_card"],
            text_color=COLORS["text_muted"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=8,
            height=44,
            width=80,
            command=self.clear_text
        )
        self.clear_button.pack(side="left")
        
    def _update_speed_display(self, val):
        self.speed_value_label.configure(text=f"{int(val)} ms")
        
    def start_injection(self):
        script_text = self.text_area.get("1.0", "end").rstrip('\n')
        if not script_text.strip():
            self.status_label.configure(text="Error: No text to type!", text_color=COLORS["accent"])
            return
            
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal", fg_color=COLORS["accent_muted"], text_color=COLORS["accent"])
        self.text_area.configure(state="disabled")
        self.progress_bar.set(0)
        
        thread = threading.Thread(target=self._injection_thread, args=(script_text,), daemon=True)
        thread.start()
        
    def _injection_thread(self, script_text):
        # Countdown
        for i in range(5, 0, -1):
            if not self.running:
                self._reset_ui()
                return
            self.countdown_label.configure(text=str(i))
            self.status_label.configure(text=f"Starting in {i}s — Click into target window!", text_color=COLORS["accent"])
            time.sleep(1)
        
        self.countdown_label.configure(text="")
        self.status_label.configure(text="Typing...", text_color=COLORS["success"])
        
        typing_interval = self.speed_slider.get() / 1000.0
        pyautogui.PAUSE = typing_interval
        
        try:
            total_chars = len(script_text)
            for i, char in enumerate(script_text):
                if not self.running:
                    self.status_label.configure(text="Stopped", text_color=COLORS["text_muted"])
                    break
                    
                if char == '\n':
                    pyautogui.press('enter')
                elif char == '\t':
                    pyautogui.press('tab')
                else:
                    pyautogui.write(char, interval=0)
                    
                if i % 5 == 0:
                    progress = i / total_chars
                    self.progress_bar.set(progress)
                    self.status_label.configure(text=f"Typing... {int(progress * 100)}%")
                    
            if self.running:
                self.progress_bar.set(1)
                self.status_label.configure(text="Done!", text_color=COLORS["success"])
        except pyautogui.FailSafeException:
            self.status_label.configure(text="Aborted (failsafe)", text_color=COLORS["accent"])
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color=COLORS["accent"])
        finally:
            self._reset_ui()
            
    def _reset_ui(self):
        self.running = False
        self.countdown_label.configure(text="")
        self.after(0, lambda: self.start_button.configure(state="normal"))
        self.after(0, lambda: self.stop_button.configure(state="disabled", fg_color=COLORS["border"], text_color=COLORS["text_muted"]))
        self.after(0, lambda: self.text_area.configure(state="normal"))
        
    def stop_injection(self):
        self.running = False
        self.status_label.configure(text="Stopping...", text_color=COLORS["text_muted"])
        
    def clear_text(self):
        self.text_area.delete("1.0", "end")
        self.status_label.configure(text="Ready", text_color=COLORS["text_muted"])
        self.progress_bar.set(0)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = KeyInjectorApp()
    app.mainloop()

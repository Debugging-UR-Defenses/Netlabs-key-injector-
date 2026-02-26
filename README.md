# NetLabs Key Injector

A simple Python GUI application that simulates keyboard typing to inject scripts into environments where copy/paste doesn't work (like NetLabs virtual machines).

## Features

- **5-second countdown** - Gives you time to click into the target window
- **Adjustable typing speed** - 1-100ms delay between keystrokes
- **Stop button** - Abort typing at any time
- **Failsafe** - Move mouse to top-left corner to emergency abort
- **Progress indicator** - Shows typing completion percentage

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/netlabs-key-injector.git
cd netlabs-key-injector

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Run the application:
   ```bash
   python key_injector.py
   ```

2. Paste your script into the text area

3. Click **"Start (5s delay)"**

4. Click into your target window (e.g., NetLabs VM) during the countdown

5. The app will type each character as if you were typing manually

## Requirements

- Python 3.6+
- pyautogui

## License

MIT License

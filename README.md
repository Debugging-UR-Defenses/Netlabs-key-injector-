# NetLabs Key Injector

A simple GUI tool that simulates keyboard typing to inject scripts into environments where copy/paste doesn't work (like NetLabs virtual machines).

## Download

**[Download key_injector.exe](https://github.com/Debugging-UR-Defenses/Netlabs-key-injector/releases)** - No Python required!

## How to Use

1. **Run** `key_injector.exe` (or `python key_injector.py`)
2. **Paste** your script into the text area
3. **Click** "Start (5s delay)"
4. **Click** into your target window (NetLabs VM, etc.) during the countdown
5. **Watch** as it types your script character by character

### Controls
- **Typing delay slider** - Adjust speed (1-100ms between keystrokes)
- **Stop button** - Abort typing at any time
- **Failsafe** - Move mouse to top-left corner to emergency abort

## Run from Source

```bash
git clone https://github.com/Debugging-UR-Defenses/Netlabs-key-injector.git
cd Netlabs-key-injector
pip install -r requirements.txt
python key_injector.py
```

## Build EXE Yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name key_injector key_injector.py
```
The exe will be in the `dist/` folder.

## License

MIT License

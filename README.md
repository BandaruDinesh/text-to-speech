# Text-to-Speech (pyttsx3) — CLI

A tiny command‑line Text‑to‑Speech tool built on **pyttsx3** (offline, cross‑platform). It lets you pass text and choose language, accent, and gender; the script picks the best matching installed voice and speaks your text.

---

## Features

* Offline speech (no API keys or internet).
* Command‑line flags for **text**, **language**, **accent**, **gender**, and **voice index**.
* Works on Windows (SAPI5), macOS (NSSpeechSynthesizer), and Linux (eSpeak/eSpeak‑NG).
* Graceful fallback if an exact voice match isn’t available.

---

## Requirements

* **Python 3.8+**
* **Windows**: `pyttsx3`, `comtypes`, `pywin32`
* **macOS**: `pyttsx3` (voices provided by macOS)
* **Linux**: `pyttsx3` and an engine like eSpeak / eSpeak‑NG

### Install (Windows example)

```powershell
# From your project folder
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install pyttsx3 comtypes pywin32
```

### Install (macOS / Linux)

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pyttsx3
# Linux may require speech engine libs, e.g. (Debian/Ubuntu):
# sudo apt-get update && sudo apt-get install -y espeak-ng libespeak-ng1
```

---

## Quick Start

Run with defaults (English/US male):

```powershell
.\.venv\Scripts\python.exe app.py
```

Speak a custom string:

```powershell
.\.venv\Scripts\python.exe app.py -t "This is a test" -l english -a us -g male
```

> On macOS/Linux, replace the venv path with `python3 app.py ...` or your interpreter path.

---

## Usage

`app.py` accepts these flags:

| Flag | Long         | Type   | Allowed                            | Default                             | Description                                                        |
| ---- | ------------ | ------ | ---------------------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| `-t` | `--text`     | string | any                                | "Hi there! I'll read text for you." | Text to speak                                                      |
| `-l` | `--language` | choice | `english`, `hindi`                 | `english`                           | Language family                                                    |
| `-a` | `--accent`   | choice | `us`, `uk`, `indian`, `australian` | `us`                                | Regional accent (for Hindi, defaults to `indian` if you omit `-a`) |
| `-g` | `--gender`   | choice | `male`, `female`, `none`           | `male`                              | Preferred voice gender (ignored if engine omits gender)            |
| `-i` | `--index`    | int    | `0..N`                             | `0`                                 | Choose among matching voices by index                              |

### Examples

* English, UK female:

```powershell
.\.venv\Scripts\python.exe app.py -t "Hello from the UK voice" -l english -a uk -g female
```

* Hindi (defaults to Indian accent if you don’t pass `-a`):

```powershell
.\.venv\Scripts\python.exe app.py -t "नमस्ते, आपका दिन शुभ हो!" -l hindi -g female
```

* Pick a specific match (after you see the printed list):

```powershell
.\.venv\Scripts\python.exe app.py -t "Use voice index 1" -l english -a us -g male -i 1
```

---

## Running in PyCharm

1. **Run ▸ Edit Configurations…**
2. Select your Python config (script: `app.py`).
3. In **Parameters**, add something like:

   ```
   -t "This is a test from PyCharm" -l english -a us -g male
   ```
4. Ensure the **Interpreter** points to your project venv: `...text-to-speech\.venv\Scripts\python.exe`.
5. **Apply ▸ Run**.

> Tip: Use double quotes around the `-t` text on Windows.

---

## How voice selection works

* The script maps your `-l`/`-a`/`-g` choices to tags like `en_US`, `hi_IN` and filters installed voices.
* If multiple match, it prints an **AVAILABLE READERS** list with indices; use `-i` to pick one.
* If no exact match, it relaxes the rules and/or falls back to the engine’s default voice.

---

## Optional tweaks

You can adjust speed/volume by inserting these lines after `reader = pyttsx3.init()`:

```python
reader.setProperty('rate', 180)   # ~default 200; try 150–200
reader.setProperty('volume', 1.0) # 0.0–1.0
```

Optionally prompt for text when `-t` is omitted (interactive run):

```python
if not args.text:
    try:
        text_to_read = input("Type text to speak: ").strip() or text_to_read
    except EOFError:
        pass
```

---

## Troubleshooting

**ModuleNotFoundError: pyttsx3**
Install into the same interpreter PyCharm uses:

```powershell
.\.venv\Scripts\python.exe -m pip install pyttsx3 comtypes pywin32
```

**No sound / silent output**

* Check Windows Volume Mixer for Python/PyCharm.
* Try a short English line with default voice:
  `.\.venv\Scripts\python.exe app.py -t "Hello" -l english -a us -g none`
* On RDP/VMs, ensure audio redirection/output device is enabled.

**Hindi voice not found on Windows**
Install a Hindi speech voice: *Settings ▸ Time & Language ▸ Language & region ▸ Add language ▸ Hindi* (include **Speech**). Then rerun with `-l hindi`.

**AttributeError: 'Voice' object has no attribute 'language'**
Already handled in the script by checking both `language` and `languages`.

---

## Project layout

```
text-to-speech/
├─ app.py        # main CLI script
└─ README.md     # this file
```

---

## License

Choose a license (e.g., MIT) if you plan to share the project publicly.

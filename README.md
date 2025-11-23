# The Cyber Avengers

# Offensive and Defensive Keylogging System
# Offensive and Defensive Keylogging (Training Lab)

A small educational project that demonstrates a controlled offensive keylogger and a defensive detector. The code is intended for authorized lab use only — for learning, red-team/blue-team exercises, and demonstrations.

Important: Do not run any component on systems you do not own or do not have explicit permission to test.

## Table of contents

- About
- Features
- Requirements
- Installation
- Usage
  - Offensive (keylogger)
  - Defensive (detector)
- Project structure
- Safety & Legal
- Contributing

## About

This repository contains two simple Python tools:

- `offensive/keylogger.py` — a learning-purpose keylogger that captures keystrokes and writes them to a log file.
- `defensive/detector.py` — a basic detector that watches for suspicious log files and process names and can attempt to stop them.

They show how attackers collect input and how defenders can detect and respond in a controlled environment.

## Features

- Minimal, easy-to-read Python examples.
- Decoupled offensive (attack) and defensive (detection) components.
- Simple file- and process-based detection logic suitable for demonstrations.

## Requirements

- Python 3.8+
- For the offensive keylogger: `pynput` (only required to run the keylogger)

Install `pynput` in a virtual environment or system package manager as needed.

## Installation

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pynput
```

Or, on Debian/Ubuntu, install the package via apt if available:

```bash
sudo apt update
sudo apt install python3-pynput
```

## Usage

Run each tool from its directory. Use a controlled test environment.

### Offensive (keylogger)

```bash
cd offensive
python3 keylogger.py
```

The keylogger writes captured keystrokes to a file (by default `keystrokes_audit.log`) in the same directory.

### Defensive (detector)

```bash
cd defensive
python3 detector.py
```

The detector watches log filenames and process names for indicators of keylogging activity and prints alerts to the console.

Notes
- Use absolute paths if you run these tools from different working directories.
- Run the detector with appropriate privileges if it needs to inspect or terminate processes.

## Project structure

```
offensiveanddefensive/
├── offensive/
│   └── keylogger.py     # Learning keylogger (requires pynput)
├── defensive/
│   └── detector.py      # Basic detector that monitors logs and processes
└── README.md
```

## Safety & Legal

This project is for education and testing in permitted environments only. Misuse of keyloggers is illegal and unethical. Always get written permission before testing on systems you do not own.

## Contributing

Small improvements, documentation fixes, and tests are welcome. Please open an issue or pull request with a description of changes.

## License

This repository does not include a license file. Add one (for example, MIT) if you intend to share or collaborate under a specific license.

---

If you'd like, I can:

- add a minimal LICENSE file (MIT)
- add a short CONTRIBUTING.md with rules for safe use
- add basic unit tests or static checks for the detector

Tell me which of those you'd like next.


# 2. Defensive Tool



### File: `detector.py`

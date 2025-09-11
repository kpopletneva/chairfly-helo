# 🚁 Helicopter Chair Fly Trainer

![CI](https://github.com/kpopletneva/chairfly-helo/actions/workflows/tests.yml/badge.svg)

A desktop training app built with PySide6 to help student pilots to practice startup & shutdown checklists, emergency procedures, 
radio communication flows, and establish "mental picture" in a "chair flying" environment without the cost and risk of real flight time,
using an interactive cockpit mock based on the Robinson R22 panel layout.
This project also includes a pytest-based automation framework with GUI testing and CI/CD integration.

## ✨ Features (MVP)
### Python & PySide6 Application
- Simulated cockpit panel 
- Toggleable switches, visual indicators and lights
- Push-to-talk button to simulate ATC communication with predefined dialog playbook
- Startup & shutdown procedures practice
- (Stretch) Ability to save/load aircraft and airport related information to file

### Automation Framework
- Built on pytest with structured fixtures
- GUI automation powered by pytest-qt

### CI/CD Pipeline
- GitHub Actions workflow running tests on Ubuntu (macOS, Windows later as I go)
- Python 3.10 & 3.11 test matrix
- Caching optimization for faster builds

## 🛠️ Built With
- Python 3.10+
- PySide6 (CUI)
- pytest, pytest-qt (testing)
- GitHub Actions (CI)
- PyInstaller (for `.exe` bundling)
- (Stretch) gTTS / pyttsx3 for voice output

## 🚀 Running Locally
```# Clone repo
git clone https://github.com/kpopletneva/chairfly-helo.git
cd chairfly-helo

# Create and activate the virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the app
python app/main.py

# Run tests
pytest
```


## ✅ Status
🚧 Work in Progress.

## 🧑‍🚀 Author
Kseniia Popletneva | Private pilot & SW Engineer/ SDET

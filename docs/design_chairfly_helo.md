🧩 1. Feature Breakdown

MVP

- GUI cockpit mockup (PySide6)
- Toggle switches:
    - Ldg. light
    - Mags/ Ignition switch
    - Master Battery
    - Alternator
    - Clutch
    - Nav. lights
    - Strobe switch
    - Pressure altitude rotary dial
    - Simulate key in/ out upon touch
    - Digital clock/ timer (?)
    - Transponder(?)
    - Radio/ GPS(?)
    - Cabin air vent(?)
    - Panel lights (?)
- Instrument state simulation (lights, gauges):
    - engine/ rotor RPM
    - airspeed indicator
    - altimeter
    - VSI
    - manifold pressure
    - start-ON light
    - clutch light
    - governor light
    - brake light
    - CAT gage
    - main & AUX fuel
    - ammeter
    - oil pressure
    - oil temperature
    - cylinder head temperature
- Emergency lights:
    - MR Temp
    - MR Chip
    - TR Chip
    - Low Fuel
    - Low RPM
    - Carbon Monoxide
    - Oil
- Save/load aircraft and airport related information to text (json?) file:
    - aircraft callsign
    - RW & taxiway numbers
    - airport code
    - tower callsign
    - airport ATIS, tower, ground frequencies
    - area frequency
- Procedure logic validator: startup checklist
- Procedure logic validator: shutdown checklist


Stretch

First:
- Chair-flying radio interaction simulator:
    - User pre-inputs expected ATC radio clearance in order he/she wants it to be played back (e.g., "Departure at pilots own risk, Helicopter 779SH")
    - User press push-to-talk button and says his/her request
    - AI or pre-scripted voice playbacks pre-inputs in specified order 5-10 seconds after pressing push-to-talk
    - Support proper aviation alphabet voice out
    - Ignore "readback" push-to-talk button press (one time after ATC clearance)
    - ATC request clearance confirmation if user forgot to read it back
    - Support occasional unexpected ATC instructions:
        - "Hold position"
        - "Make left/ right turn for traffic"
        - ATC asking PIREP
- Voice out ATIS information from text file (random ATIS), when switch to ATIS frequency
- Save/load text-to-voice radio com playbooks
- AI-generated background ATC-style audio to simulate ambient feel of an active tower/ radio environment

Second:
- Voice recognition input for commands (via speech-to-text or GPT) :
    - Calling throttle roll ON/ OFF during start-up & shutdown => RPM rise/ drop 55% / 75%/ 101-104%
    - Calling carb heat pull ON(up)/ OFF(down) during start-up & shutdown => CAT rise/ drop (maybe reflect RPM drop/ rise?)
    - Calling sprag clutch check at 75% RPM during start-up => needles split
    - Calling governor switch ON/ OFF during start-up & shutdown => governor light OFF/ ON
    - Calling low RPM warning check => hort & light at 97% RPM
    - Radio communication inputs and propvide proper response when not using pre-input ordered text playbook
    - Repeat last clearance upon "Say again"

Third:
- Procedure selection dropdown (startup, shutdown, emergency procedure)
- Emergency procedures practice and walkthrough (no autorotarion, governor failure):
  - electrical fire on board
  - alternator light ON
  - low oil pressure
  - etc.

Fours:
- Sound or text-based feedback for correct/incorrect action order
- Save/load student sessions

🧱 2.  Architecture Overview 

```
┌───────────────────────────────────────┐
│           Main App UI Layer           │
│            (main.py)                  │
└────────────────┬──────────────────────┘
                 │
      ┌──────────▼────────────┐
      │   Instrument Panel    │
      │ ┌───────────────────┐ │
      │ │ ui_r22.py         │ │  ← PySide6 GUI layout
      │ └───────────────────┘
      │ ┌───────────────────┐ │
      │ │ styles.py         │ │  ← GUI styles sheets
      │ └───────────────────┘ |
      │ ┌───────────────────┐ │
      │ │ state_manager.py  │ │  ← Tracks state of toggles/switches
      │ └───────────────────┘ |
      │ ┌───────────────────┐ │    Receives user input (clicked buttons, selected drop downs, etc.)
      │ │ app_controller.py │ │  ← Updates state_manager.py
      │ └───────────────────┘ │    Selects view to present
      └──────────┬────────────┘
                 │
      ┌──────────▼────────────┐
      │ ChecklistEngine.py    │  <- procedure validation logic for startup, shutdown, emergency
      └───────────────────────┘
                 │
      ┌──────────▼────────────┐
      │ FeedbackManager.py    │  <- GUI cues or sound alerts for visuals/audio/text feedback (stretch)
      └───────────────────────┘
                 │
      ┌──────────▼────────────┐
      │ ChairFlyComms.py      │  <- push-to-talk & voice playback (stretch)
      └───────────────────────┘
```

🧱 3. Project Structure

```

chairfly-helo/
├── app/                     # Main app source code
│   ├── __init__.py
│   ├── main.py
|   ├── views/                  # MVC View
│   │   ├──                     # App entry point
│   |   ├── ui_r22.py           # PySide6 GUI
│   |   ├── styles.py           # GUI styles sheets
│   ├── model/                  # Application logic
│   │   ├── __init__.py
│   │   └── state_manager.py     # Tracks toggle state, logic
|   ├── controllers/             # Coordination between Model and View
│   │   └── app_controller.py    # Intermediary between the Model and the View, handles user input
│   └── assets/                  # Images, icons, mock panel graphics
│       └── r22_panel.png
├── tests/                       # Tests
│   └── test_state_manager.py
├── .gitignore
├── README.md
├── requirements.txt             # Dependencies for pip
└── LICENSE                  
```

🧰 4. Technology Stack

| Area	         | Tech Used	                 | Notes                             |
| -------------- | ----------------------------- | --------------------------------- |
| GUI	         | PySide6	                     | All are modern UI libraries       |
| Audio	         | pyttsx3, gTTS or pygame	     | For offline/online voice playback |
| Packaging	     | PyInstaller, cx_Freeze	     | To make .exe for Windows or .app  |
| Data/Input	 | JSON, CSV, text	             | For checklist data, comm scripts  |
| AI/Voice (opt.)| OpenAI API, SpeechRecognition | For simulated ATC conversations   |

🗃️ 5. Data & UI Sketches

- Checklist data stored as simple JSON:

{
  "startup": [
    {"step": "Battery ON", "type": "switch", "name": "battery"},
    {"step": "Alternator ON", "type": "switch", "name": "alternator"},
    ...
  ]
}
- UI shows:
  - Realistic or stylized cockpit with clickable switches
  - Procedure selection dropdown
  - Checklist window (progress display), feature might be turned ON/ OFF
  - Feedback area, feature might be turned ON/ OFF
  - (Stretch) Push-to-talk button
  - (Stretch) AI-generated background ATC-style audio toggle
  - (Stretch) Log user interactions for session replay
  - (Optional) Simulated ATC conversations toggle

🧪 6. Testing Strategy
Auto tests for:
- Checklist validation logic
- Instrument state tracking
- GUI click behavior (use pytest-qt test harnesses)

Manual tests for:
- Full procedure flow (end-to-end)
- Simulate voice/audio output for tests

⚠️ 7. Risks & Tradeoffs
| Risk                            |	Mitigation                                   |
| ------------------------------- | -------------------------------------------- |
| Feature creep                   |	Stick to MVP list before adding stretch      |
| GUI complexity or bugs          |	Use reusable widgets/components              |
| Voice API latency or quality    |	Use offline text-to-speech where possible    |
| Chair-fly logic complexity      |	Simplify with pre-filled call templates      |
| Packaging issues                |	Test early with PyInstaller or alternatives  |

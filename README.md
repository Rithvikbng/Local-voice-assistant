
# Local AI Assistant
Local AI Assistant is a privacy-focused, offline AI assistant designed to handle speech recognition, natural language understanding, and text-to-speech tasks. The assistant operates entirely on local hardware, ensuring user data stays secure and private.

# Features
Speech-to-Text (STT): Converts spoken words into text using offline models.
Natural Language Processing (NLP): Processes user commands and determines intent.
Text-to-Speech (TTS): Provides voice responses in the desired language.
Multilingual Support: Includes local language integration for broader accessibility.
Privacy-First: All computations are performed locally, with no data sent to the cloud.
Installation
Prerequisites
Python 3.9 or higher
Git
Compatible hardware (recommended: GPU for faster processing)

# Installation
Prerequisites

Python 3.9 or higher
Git
Compatible hardware (recommended: GPU for faster processing)

# Steps

**1- Clone this Repo**





```bash
git clone https://github.com/Rithvikbng/Local-voice-assistant.git
cd local-ai-assistant

```
**2- Install required dependencies:**
```bash
pip install -r requirements.txt

```
**3- Set up a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows


```
# Usage

Run the main script to start the assistant:

```bash
python main.py
```

# Command-Line Options
--language [lang_code]: Specify the language (default: en for English).
--device [cpu|gpu|mps]: Choose the device for computation.

# Example 

```bash
python main.py --language en --device cpu
```

# Directory structure

```bash
local-ai-assistant/
├── stt/                 # Speech-to-Text modules
├── nlu/                 # Natural Language Understanding logic
├── tts/                 # Text-to-Speech modules
├── data/                # Example datasets or model files
├── main.py              # Entry point for the application
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```


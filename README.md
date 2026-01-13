# 🌐 Indian Multilingual Translator

An **interactive multilingual translator** for Indian languages. Supports **audio input, text files, and manual typing**, and provides **translated text and speech output**.

---

## Features

- Translate between **English, Hindi, Telugu, Tamil, Kannada, Malayalam, and Bengali**  
- Supports **Audio Input** (speech-to-text)  
- Supports **Text File Input**  
- Manual typing input supported  
- Provides **native script transliteration**  
- Generates **MP3 speech output** for all target languages  

---

## Demo Videos

### Demo 1
<video width="600" controls>
  <source src="media/Media3.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Demo 2
<video width="600" controls>
  <source src="media/Media2.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

> ✅ Visitors can click **Play** to watch the demos directly in the README.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/HarshiniPeddapudi/Indian-Multilingual-Translator.git
cd Indian-Multilingual-Translator
Create a virtual environment:

bash
Copy code
python -m venv .venv
Activate the environment:

Windows: .venv\Scripts\activate

Linux/Mac: source .venv/bin/activate

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Create a .env file with your keys:

env
Copy code
ASSEMBLYAI_API_KEY=your_assemblyai_key
GOOGLE_APPLICATION_CREDENTIALS=credentials/your_google_key.json
PROJECT_ID=your_google_project_id
⚠️ Make sure .env and credentials/ are not pushed to GitHub.

Usage
bash
Copy code
python hasle.py
Open the Gradio link shown in the terminal.

Select Input Type, Input Language, and Target Language.

Upload audio/text file or type manually.

Click Translate to see text and hear audio output.

Technologies
Gradio – Interactive UI

Google Cloud Translation & TTS – Translation and speech synthesis

AssemblyAI – Audio transcription

Indic Transliteration – Native script conversion

Python 3.10+

Contributing
Fork the repository

Create a feature branch: git checkout -b feature-name

Commit your changes: git commit -m "Add feature"

Push: git push origin feature-name

Open a Pull Request
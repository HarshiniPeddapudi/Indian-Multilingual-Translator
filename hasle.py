import gradio as gr
from google.cloud import texttospeech
from google.cloud.translate import TranslationServiceClient
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import tempfile
import assemblyai as aai
import os

from dotenv import load_dotenv
load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")

# ================= LANGUAGE MAP =================
LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn"
}

TARGET_LANGUAGES = ["Hindi", "Telugu", "Tamil", "Kannada", "Malayalam", "Bengali"]

# ================= TRANSLITERATION =================
def transliterate_to_native(text, lang_code):
    script_map = {
        "hi": sanscript.DEVANAGARI,
        "te": sanscript.TELUGU,
        "ta": sanscript.TAMIL,
        "kn": sanscript.KANNADA,
        "ml": sanscript.MALAYALAM,
        "bn": sanscript.BENGALI
    }
    if lang_code in script_map:
        return transliterate(text, sanscript.ITRANS, script_map[lang_code])
    return text

# ================= AUDIO TRANSCRIPTION =================
def audio_transcription(audio_file, lang_code):
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(language_code=lang_code)
    transcript = transcriber.transcribe(audio_file, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        return f"Error: {transcript.error}"
    return transcript.text

# ================= FILE READ =================
def read_text_file(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

# ================= GOOGLE TRANSLATION =================
def translate_text(text, src_code, tgt_code):
    client = TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global" # Your Project ID

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": src_code,
            "target_language_code": tgt_code,
        }
    )
    return response.translations[0].translated_text

# ================= GOOGLE TTS =================
def text_to_speech_google(text, lang_code):
    client = texttospeech.TextToSpeechClient()

    tts_lang_map = {
        "hi": "hi-IN",
        "te": "te-IN",
        "ta": "ta-IN",
        "kn": "kn-IN",
        "ml": "ml-IN",
        "bn": "bn-IN",
        "en": "en-US"
    }

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=tts_lang_map.get(lang_code, "en-US"),
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio.write(response.audio_content)
    temp_audio.close()
    return temp_audio.name

# ================= MAIN PROCESS =================
def process_input(input_type, input_language, audio_file, text_file, manual_text, target_language):
    src_code = LANG_MAP[input_language]
    tgt_code = LANG_MAP[target_language]

    if input_type == "Audio" and audio_file:
        text = audio_transcription(audio_file, src_code)
    elif input_type == "Text File" and text_file:
        text = read_text_file(text_file)
    else:
        text = manual_text.strip()

    translated = translate_text(text, src_code, tgt_code)
    native_text = transliterate_to_native(translated, tgt_code)
    audio_path = text_to_speech_google(native_text, tgt_code)

    lines_needed = max(2, min(len(native_text) // 50 + 1, 20))

    # ✅ Use gr.update() instead of gr.Textbox.update()
    return (
        gr.update(
            value=f"🔹 {target_language} Translation:\n\n{native_text}",
            lines=lines_needed
        ),
        audio_path
    )

# ================= VISIBILITY CONTROL =================
def toggle_inputs(choice):
    return (
        gr.update(visible=choice == "Audio"),
        gr.update(visible=choice == "Text File"),
        gr.update(visible=choice == "Manual Text")
    )

# ================= UI =================
with gr.Blocks() as demo:

    gr.Markdown("<h2 style='color:#1e3a8a'>🌐 Indian Multilingual Translator</h2>")

    input_type = gr.Radio(["Audio", "Text File", "Manual Text"], label="Step 1: Select Input Type", value="Manual Text")
    input_language = gr.Dropdown(list(LANG_MAP.keys()), label="Step 2: Input Language", value="English")
    target_lang = gr.Dropdown(TARGET_LANGUAGES, label="Step 3: Target Language", value="Telugu")

    audio_input = gr.Audio(type="filepath", label="Upload Audio", visible=False)
    text_file = gr.File(file_types=[".txt"], label="Upload Text File", visible=False)
    manual_text = gr.Textbox(label="Enter Text", placeholder="Type here...", visible=True)

    translate_btn = gr.Button("Translate")
    output_text = gr.Textbox(label="Translated Text", interactive=False)
    output_audio = gr.Audio(label="Translated Audio")

    input_type.change(toggle_inputs, input_type, [audio_input, text_file, manual_text])
    translate_btn.click(
        process_input,
        [input_type, input_language, audio_input, text_file, manual_text, target_lang],
        [output_text, output_audio]
    )

# ================= LAUNCH =================
if __name__ == "__main__":
    demo.launch(
        share=True,
        pwa=True,
        css="""
        .gradio-container { background-color: #f0f4ff !important; padding: 20px; }
        .gr-button { background-color: #1e3a8a !important; color: white !important; font-weight: bold !important; border-radius: 12px !important; }
        .gr-button:hover { background-color: black !important; }
        .gr-dropdown, .gr-textbox textarea, .gr-file, .gr-audio audio { border: 2px solid #1e3a8a !important; border-radius: 10px !important; }
        label { font-weight: bold !important; color: #1e3a8a !important; }
        """
    )

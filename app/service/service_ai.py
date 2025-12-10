import os
import uuid
import json
from pathlib import Path
from typing import Tuple

from openai import OpenAI

# Gemini GenAI SDK
try:
    from google import genai
    from google.genai import types as genai_types
except Exception:
    genai = None
    genai_types = None


MEDIA_ROOT = Path("media")
ASR_UPLOAD_DIR = MEDIA_ROOT / "uploads"
TTS_OUTPUT_DIR = MEDIA_ROOT / "tts"


def _ensure_dirs() -> None:
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    ASR_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    TTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def transcribe_audio(save_filename: str, file_bytes: bytes, provider_override: str | None = None) -> dict:
    """
    Simpan audio masuk dan lakukan transkripsi menggunakan Gemini Audio API.

    Mengembalikan dict: {"text": "..."} berisi transcript.
    Catatan: parameter provider_override dipertahankan untuk kompatibilitas, namun tidak digunakan oleh Gemini.
    """
    _ensure_dirs()
    target_path = ASR_UPLOAD_DIR / save_filename
    with open(target_path, "wb") as f:
        f.write(file_bytes)

    if genai is None:
        raise RuntimeError("google-genai library not installed. Please add 'google-genai' to requirements.")

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable is not set")

    client = genai.Client(api_key=api_key)

    # Siapkan input audio untuk Gemini: coba upload via Files API, jika gagal gunakan inline bytes
    parts = []
    file_uri = None
    try:
        uploaded = client.files.upload(file=str(target_path))
        file_uri = getattr(uploaded, "uri", None) or getattr(uploaded, "file_uri", None)
    except Exception:
        file_uri = None

    if file_uri:
        parts.append(genai_types.Part(file_data=genai_types.FileData(file_uri=file_uri)))
    else:
        # Inline bytes fallback
        with open(target_path, "rb") as af:
            audio_bytes = af.read()
        # Tentukan mime type sederhana dari ekstensi
        ext = target_path.suffix.lower()
        mime = "audio/wav"
        if ext in {".mp3"}:
            mime = "audio/mpeg"
        elif ext in {".m4a"}:
            mime = "audio/mp4"
        elif ext in {".ogg"}:
            mime = "audio/ogg"
        elif ext in {".flac"}:
            mime = "audio/flac"
        parts.append(genai_types.Part(inline_data=genai_types.Blob(mime_type=mime, data=audio_bytes)))

    # Instruksi untuk transkripsi verbatim; hasilkan hanya teks transkrip
    parts.append(genai_types.Part(text=(
        "Transcribe the audio verbatim in the original language. "
        "Provide only the transcript text without timestamps or extra commentary."
    )))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[genai_types.Content(parts=parts)],
    )

    transcript = ""
    try:
        # Properti helper yang biasanya tersedia
        transcript = (getattr(response, "text", "") or "").strip()
        if not transcript:
            # Coba ambil dari part pertama
            transcript = (
                getattr(response.candidates[0].content.parts[0], "text", "")
                if getattr(response, "candidates", None)
                else ""
            ).strip()
    except Exception:
        transcript = ""

    if not transcript:
        # Fallback: gabungkan semua part teks yang ada
        try:
            texts = []
            for cand in getattr(response, "candidates", []) or []:
                for p in getattr(cand.content, "parts", []) or []:
                    t = getattr(p, "text", None)
                    if t:
                        texts.append(str(t))
            transcript = "\n".join(texts).strip()
        except Exception:
            transcript = ""

    return {"text": transcript}


def _build_validation_prompt(instruction: str, speech_text: str, spoken_text: str) -> Tuple[str, list]:
    """
    Build system and user messages that strictly instruct the model to return JSON.
    """
    system_prompt = (
        "Anda adalah asisten evaluasi ujaran untuk pengguna dengan gangguan bicara. "
        "Tugas Anda: bandingkan 'teks yang diucapkan' dengan 'instruction' dan 'speech_text'. "
        "Jika ucapan SUDAH SEPENUHNYA sesuai (tidak kurang dari speech_text dan mengikuti instruction), balas HANYA JSON: {\"message\": \"complete\"}. "
        "Jika BELUM sesuai, balas HANYA JSON: {\"message\": \"<feedback singkat, positif, suportif dalam bahasa Indonesia>\"}. "
        "Tidak boleh menambahkan teks lain, penjelasan, atau kode blok—hanya satu objek JSON dengan kunci 'message'."
    )

    user_prompt = (
        f"Instruction: {instruction}\n"
        f"Speech text (target): {speech_text}\n"
        f"Teks yang diucapkan pengguna: {spoken_text}\n\n"
        "Nilai apakah teks yang diucapkan sudah lengkap dan sesuai dengan target. "
        "Jika sudah lengkap dan sesuai, balas {\"message\": \"complete\"}. Jika belum, berikan umpan balik singkat, empatik, dan jelas dalam bahasa Indonesia, misalnya: \"Coba ulangi perlahan, fokus pada kata ...\"."
    )

    return system_prompt, [{"role": "user", "content": user_prompt}]


def validate_speech_json(instruction: str, speech_text: str, spoken_text: str) -> dict:
    """
    Use gpt-oss-20b (Groq via Hugging Face Router) to validate user's spoken text.
    Returns strictly a dict with key 'message'.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable is not set")

    system_prompt, messages = _build_validation_prompt(instruction, speech_text, spoken_text)
    client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_token)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:groq",
        messages=[{"role": "system", "content": system_prompt}] + messages,
        max_tokens=200,
        temperature=0.2,
    )

    content = completion.choices[0].message.content if completion and completion.choices else ""
    # Try to parse JSON safely; strip code fences if any
    text = content.strip()
    if text.startswith("```"):
        text = text.strip("`\n ")
        # after stripping fences, text should be JSON
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "message" in data:
            return {"message": str(data["message"])[:1000]}
    except Exception:
        pass

    # Fallback heuristic: if spoken_text matches or contains speech_text
    spoken_norm = (spoken_text or "").strip().lower()
    target_norm = (speech_text or "").strip().lower()
    if target_norm and (spoken_norm == target_norm or target_norm in spoken_norm):
        return {"message": "complete"}
    # Otherwise generic supportive feedback
    return {"message": "Coba ulangi perlahan dengan jeda kecil antar kata. Fokus pada pengucapan sesuai instruksi."}


def synthesize_feedback_tts(message: str) -> dict:
    """
    Generate TTS audio from Gemini with voice 'Kore', save to media/tts, and return absolute file URL.
    """
    _ensure_dirs()

    if genai is None:
        raise RuntimeError("google-genai library not installed. Please add 'google-genai' to requirements.")

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable is not set")

    # Use prebuilt voice 'Kore'
    voice_name = "Kore"

    client = genai.Client(api_key=api_key)

    # Prompt style: Indonesian, warm, supportive, encouraging repetition.
    contents = (
        "Berikan umpan balik singkat dalam bahasa Indonesia dengan nada hangat, tenang, dan suportif. "
        "Tujuan: membantu pengguna dengan gagap/stuttering agar mau mengulang latihan.\n\n"
        f"Umpan balik: {message}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=contents,
        config=genai_types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=genai_types.SpeechConfig(
                voice_config=genai_types.VoiceConfig(
                    prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(
                        voice_name=voice_name,
                    )
                )
            ),
        ),
    )

    # Extract PCM data and write WAV (24kHz, mono, 16-bit)
    part = response.candidates[0].content.parts[0]
    inline = getattr(part, "inline_data", None)
    data_b64 = getattr(inline, "data", None)
    mime = getattr(inline, "mime_type", "audio/wav")
    if not data_b64:
        raise RuntimeError("No audio data returned from Gemini TTS")

    import base64, wave
    # google-genai (Python) mengembalikan inline_data.data sebagai bytes (PCM) langsung.
    # Jika yang diterima berupa string base64, baru lakukan decode.
    if isinstance(data_b64, (bytes, bytearray)):
        audio_bytes = data_b64
    else:
        audio_bytes = base64.b64decode(data_b64)

    # Determine extension by mime type (default wav)
    ext = ".wav"
    if isinstance(mime, str):
        if "mp3" in mime or "mpeg" in mime:
            ext = ".mp3"
        elif "ogg" in mime:
            ext = ".ogg"
        elif "wav" in mime:
            ext = ".wav"
        elif "pcm" in mime:
            ext = ".wav"  # we'll wrap raw PCM into WAV

    file_id = uuid.uuid4().hex
    out_path = TTS_OUTPUT_DIR / f"feedback_{file_id}{ext}"

    # If bytes already contain a WAV header (RIFF), write directly. Otherwise, wrap as PCM -> WAV.
    has_wav_header = len(audio_bytes) >= 12 and audio_bytes[:4] == b"RIFF" and audio_bytes[8:12] == b"WAVE"
    if ext == ".wav" and not has_wav_header:
        with wave.open(str(out_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio_bytes)
    else:
        with open(out_path, "wb") as f:
            f.write(audio_bytes)

    # Bangun URL absolut menggunakan env, fallback ke localhost
    base_url = os.getenv("PUBLIC_BASE_URL") or os.getenv("APP_BASE_URL") or "http://127.0.0.1:8000"
    full_url = f"{base_url.rstrip('/')}/media/tts/{out_path.name}"
    return {"url": full_url}
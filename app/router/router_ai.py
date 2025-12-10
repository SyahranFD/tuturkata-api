from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from ..service.service_ai import transcribe_audio, validate_speech_json, synthesize_feedback_tts


router_ai = APIRouter(prefix="/api/ai", tags=["AI"])


class ValidatePayload(BaseModel):
    instruction: str = Field(..., description="Instruksi yang harus diikuti")
    speech_text: str = Field(..., description="Teks target yang diharapkan")
    spoken_text: str = Field(..., description="Teks hasil ucapan user dari audio")


class TtsPayload(BaseModel):
    message: str = Field(..., description="Teks feedback yang akan diucapkan")


@router_ai.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Determine filename with original extension if available
        filename = file.filename or f"audio_{file.content_type.replace('/', '_')}.bin"
        result = transcribe_audio(filename, contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_ai.post("/validate")
def validate(payload: ValidatePayload):
    try:
        result = validate_speech_json(payload.instruction, payload.speech_text, payload.spoken_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_ai.post("/tts")
def tts(payload: TtsPayload):
    try:
        result = synthesize_feedback_tts(payload.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
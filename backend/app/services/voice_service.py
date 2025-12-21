"""
Voice Analysis Service for Hotword Detection
"""
import speech_recognition as sr
from pydub import AudioSegment
import io
import logging
import os
import json

logger = logging.getLogger(__name__)

class VoiceAnalysisService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    async def analyze_audio_for_hotwords(self, audio_file: bytes, user_hotwords: list[str]) -> dict:
        """
        Transcribes audio and checks for matches in user's hotword list.
        """
        try:
            # Convert audio format if necessary (e.g., from m4a/aac to wav for SpeechRecognition)
            # Assuming incoming might be wav or m4a from mobile
            
            # Use pydub to convert to compatible Wav
            try:
                audio = AudioSegment.from_file(io.BytesIO(audio_file))
                
                # Export to wav for SpeechRecognition
                wav_io = io.BytesIO()
                audio.export(wav_io, format="wav")
                wav_io.seek(0)
                
            except Exception as e:
                logger.error(f"Audio conversion error: {e}")
                return {"triggered": False, "transcription": "", "error": "Invalid audio format"}

            # Perform Speech Recognition
            with sr.AudioFile(wav_io) as source:
                # self.recognizer.adjust_for_ambient_noise(source) # Optional, might slow down
                audio_data = self.recognizer.record(source)
                
            try:
                # Use Google Web Speech API (Free, decent accuracy)
                # For offline, we'd use Sphinx (bad accuracy) or Whisper (heavy)
                text = self.recognizer.recognize_google(audio_data)
                logger.info(f"🗣️ Transcribed text: '{text}'")
                
            except sr.UnknownValueError:
                logger.info("🤷 Could not understand audio")
                return {"triggered": False, "transcription": "", "error": "Unintelligible"}
            except sr.RequestError as e:
                logger.error(f"API Error: {e}")
                return {"triggered": False, "transcription": "", "error": "Service unavailable"}

            # Check for hotwords
            # Simple substring matching (fuzzy matching could be better)
            triggered = False
            matched_word = None
            
            transcribed_lower = text.lower()
            
            for word in user_hotwords:
                if word.lower() in transcribed_lower:
                    triggered = True
                    matched_word = word
                    break
                    
            return {
                "triggered": triggered,
                "transcription": text,
                "matched_word": matched_word
            }

        except Exception as e:
            logger.error(f"Voice analysis failed: {str(e)}")
            return {"triggered": False, "error": str(e)}

voice_service = VoiceAnalysisService()

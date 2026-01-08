"""
Voice Analysis endpoints for Hot Word Detection
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from typing import Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze")
async def analyze_voice(
    audio: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze audio for hot words using server-side Speech-to-Text.
    Fetches user's specific hotwords from DB.
    """
    try:
        from app.services.voice_service import voice_service # Import here to avoid circulars
        
        # 1. Fetch user's hot words
        # current_user is a dict from get_current_user security dependency
        user_id = current_user.get("id")
        
        # Query User model to get hot_words list
        # We need to execute a query since current_user is just a JWT payload dict usually
        query = select(User.hot_words).where(User.id == user_id)
        result = await db.execute(query)
        user_hot_words = result.scalars().first()
        
        if not user_hot_words:
             # Default fallback if somehow missing or empty
            user_hot_words = ["help", "bachao", "save me", "police", "emergency"]
            
        logger.info(f"🎤 Analyzing voice for User {user_id}. Hotwords: {user_hot_words}")

        # 2. Read audio file
        audio_content = await audio.read()
        
        # 3. Analyze
        result = await voice_service.analyze_audio_for_hotwords(audio_content, user_hot_words)
        
        logger.info(f"✅ Analysis Result: {result}")
        
        return {
            "trigger": result["triggered"],
            "transcript": result.get("transcription", ""),
            "matched_word": result.get("matched_word"),
            "debug_info": "Used server-side SpeechRecognition"
        }
        
    except Exception as e:
        logger.error(f"Voice analysis error: {str(e)}")
        # Don't crash the app, just return false
        return {"trigger": False, "error": str(e)}

"""
SMS Service for sending emergency alerts via SMS.net.bd
"""
import httpx
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        self.api_url = "https://api.sms.net.bd/sendsms"
        # Temporarily hardcoded as requested
        self.api_key = "2q51lFEMKAIZq37L539IXXR8y28F2v317Th18z38" 
        self.target_number = "01605954603"

    async def send_sos_sms(
        self,
        phone_number: str,
        user_name: str,
        location: dict
    ) -> bool:
        """
        Send SOS SMS to the recipient.
        Currently filtered to ONLY send to the specific target number.
        """
        # 1. Filter: specific constraint requested by user
        # Note: We prioritize the Hardcoded Target Number for the test
        # If the incoming phone_number is NOT the target, we skip or redirect?
        # User said: "Use this API key to only send to the emergency contact of the user... For the time being only send to 01886709707"
        # Implication: Regardless of who the contact IS, force send to 01886709707?
        # OR: Only send IF the contact is 01886709707.
        # Interpretation: "For testing, replace any recipient with 01886709707" or "Only allow this number".
        # Safest approach: Send to 01886709707 every time an SOS is triggered, ignoring the actual contact list number for now to avoid spamming strangers.
        
        recipient = self.target_number
        
        lat = location.get('latitude', 0)
        lon = location.get('longitude', 0)
        maps_link = f"https://maps.google.com/?q={lat},{lon}"
        
        message = f"SOS! {user_name} needs help. Location: {maps_link}"
        
        try:
            params = {
                "api_key": self.api_key,
                "msg": message,
                "to": recipient
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, data=params)
                
            resp_data = response.json()
            
            if response.status_code == 200 and not resp_data.get('error'):
                logger.info(f"✅ SMS Sent Successfully to {recipient}")
                logger.info(f"Response: {resp_data}")
                return True
            else:
                logger.error(f"❌ SMS Failed: {resp_data}")
                return False
                
        except Exception as e:
            logger.error(f"❌ SMS Service Error: {str(e)}")
            return False

# Singleton instance
sms_service = SMSService()

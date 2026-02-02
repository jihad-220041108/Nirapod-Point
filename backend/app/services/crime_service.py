"""
Crime Service for handling crime reports and risk analysis
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, text, Float
from app.models.crime import CrimeReport
from datetime import datetime, timedelta
import math
import logging

logger = logging.getLogger(__name__)

class CrimeService:
    
    CRIME_WEIGHTS = {
        "low": 1.0,
        "medium": 3.0,
        "high": 5.0,
        "critical": 10.0
    }

    async def calculate_crime_score(self, lat: float, lng: float, db: Session, radius_km: float = 1.0):
        """
        Calculate crime score for a location based on nearby incidents.
        Score is 0-100 (normalized).
        """
        try:
            # Simple Haversine approximation in SQL or Python. 
            # Since lat/long are strings in DB (legacy choice), we cast them.
            # Using Python for filtering if dataset is small, or SQL for efficiency.
            # SQL is better.
            
            # Note: 1 degree latitude ~= 111km. 1km ~= 0.009 degrees.
            deg_radius = radius_km / 111.0
            
            # First pass: Bounding box query to filter candidates (fast)
            min_lat = lat - deg_radius
            max_lat = lat + deg_radius
            min_lng = lng - deg_radius # Approximate
            max_lng = lng + deg_radius
            
            query = select(CrimeReport).where(
                CrimeReport.latitude.cast(Float) >= min_lat,
                CrimeReport.latitude.cast(Float) <= max_lat,
                CrimeReport.longitude.cast(Float) >= min_lng,
                CrimeReport.longitude.cast(Float) <= max_lng
            )
            
            result = await db.execute(query)
            crimes = result.scalars().all()
            
            total_score = 0
            recent_crimes_count = 0
            
            current_time = datetime.utcnow()
            
            for crime in crimes:
                try:
                    c_lat = float(crime.latitude)
                    c_lng = float(crime.longitude)
                    
                    # Exact distance calculation
                    dist = self._haversine_distance(lat, lng, c_lat, c_lng)
                    
                    if dist <= radius_km:
                        # Determine weight based on severity (implied from category or if exists)
                        # The model has 'status' and 'category', but implies severity elsewhere. 
                        # We will map category to severity if needed, or assume a default.
                        # Wait, CrimeSeverity enum is in models/crime.py but not explicitly used in CrimeReport columns in the file I viewed?
                        # I viewed models/crime.py and it DID NOT have a severity column! 
                        # It has 'category'. I'll infer severity.
                        
                        severity = self._infer_severity(crime.category)
                        weight = self.CRIME_WEIGHTS.get(severity, 3.0)
                        
                        # Time decay: Recent crimes matter more
                        # Linear decay over 90 days
                        days_diff = (current_time - crime.incident_date_time).days
                        time_factor = max(0, 1.0 - (days_diff / 90.0))
                        
                        if time_factor > 0:
                            total_score += weight * time_factor
                            recent_crimes_count += 1
                            
                except ValueError:
                    continue

            # Normalize score (0-100)
            # Threshold: 50 points = 100% danger (arbitrary calibration)
            normalized_score = min((total_score / 50.0) * 100, 100.0)
            
            # Determine level
            if normalized_score < 20:
                level = "Safe"
                color = "#4CAF50" # Green
            elif normalized_score < 50:
                level = "Moderate"
                color = "#FFC107" # Amber
            elif normalized_score < 80:
                level = "High Risk"
                color = "#FF9800" # Orange
            else:
                level = "Critical"
                color = "#F44336" # Red
                
            return {
                "score": round(normalized_score, 1),
                "level": level,
                "color": color,
                "incident_count": recent_crimes_count
            }

        except Exception as e:
            logger.error(f"Error calculating crime score: {str(e)}")
            return {"score": 0, "level": "Unknown", "color": "#9E9E9E", "incident_count": 0}

    def _infer_severity(self, category: str) -> str:
        category = category.lower()
        if category in ["murder", "rape", "robbery", "kidnapping", "assault"]:
            return "critical"
        elif category in ["burglary", "drug related", "vandalism"]:
            return "high"
        elif category in ["theft", "harassment"]:
            return "medium"
        return "low"

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

crime_service = CrimeService()

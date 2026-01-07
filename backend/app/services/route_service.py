import logging
import math
import httpx
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Float
from app.models.crime import CrimeReport
from app.schemas.route import RouteRequest, RouteResponse, RouteSegment, Location

import json
import os

logger = logging.getLogger(__name__)

class RouteService:
    def __init__(self):
        self.risk_model = {}
        self._load_risk_model()

    def _load_risk_model(self):
        try:
            # Path to backend/scripts/crime_risk_model.json
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            model_path = os.path.join(base_dir, "scripts", "crime_risk_model.json")
            
            if os.path.exists(model_path):
                with open(model_path, "r") as f:
                    self.risk_model = json.load(f)
                logger.info("✅ Crime Risk Model loaded successfully")
            else:
                logger.warning(f"⚠️ Crime Risk Model not found at {model_path}")
        except Exception as e:
            logger.error(f"Failed to load Crime Risk Model: {e}")

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in km"""
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
        
    def _get_regional_risk(self, lat: float, lon: float) -> float:
        """Get normalized risk score based on regional model (0-100)"""
        max_risk = 0.0
        
        for unit, data in self.risk_model.items():
            center = data.get("location", {})
            c_lat = center.get("lat")
            c_lon = center.get("lon")
            radius = center.get("radius_km", 10)
            
            if c_lat and c_lon:
                dist = self._haversine_distance(lat, lon, c_lat, c_lon)
                if dist <= radius:
                    # Point is within this high-risk zone
                    # We take the max risk if overlapping zones
                    risk = data.get("normalized_risk", 0.0)
                    if risk > max_risk:
                        max_risk = risk
                        
        return max_risk

    def _generate_path(self, start: Location, end: Location, num_points: int = 10, curve_factor: float = 0.0) -> List[Tuple[float, float]]:
        """
        Generate a simulated path if OSRM fails.
        """
        path = []
        for i in range(num_points + 1):
            t = i / num_points
            lat = start.latitude + t * (end.latitude - start.latitude)
            lng = start.longitude + t * (end.longitude - start.longitude)
            if curve_factor != 0:
                deviation = math.sin(t * math.pi) * curve_factor
                lat += deviation * 0.01
                lng += deviation * 0.01
            path.append((lat, lng))
        return path

    async def _fetch_osrm_routes(self, start: Location, end: Location) -> List[dict]:
        """Fetch real routes from OSRM"""
        # OSRM demo server (use with care, rate/reliability not guaranteed for prod)
        url = f"http://router.project-osrm.org/route/v1/driving/{start.longitude},{start.latitude};{end.longitude},{end.latitude}"
        params = {
            "overview": "full",
            "geometries": "geojson",
            "alternatives": "true"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == "Ok":
                        return data.get("routes", [])
        except Exception as e:
            logger.error(f"OSRM Fetch Error: {e}")
        return []

    async def _calculate_path_risk(self, path: List[Tuple[float, float]], db: AsyncSession) -> Tuple[float, List[Location]]:
        """
        Calculate risk score for a path based on nearby crimes AND regional model.
        Returns (risk_score, hotspots_list)
        """
        local_incident_risk = 0.0
        hotspots = []
        
        # 1. Regional Risk Calculation (Base Level)
        # Sample points along path to determine max regional risk
        # We check every 10th point to save compute
        regional_risks = []
        sample_step = max(1, len(path) // 20)
        for i in range(0, len(path), sample_step):
            p = path[i]
            regional_risks.append(self._get_regional_risk(p[0], p[1]))
            
        avg_regional_risk = sum(regional_risks) / len(regional_risks) if regional_risks else 0.0
        
        # 2. Local Incident Risk Calculation (Specific Crimes)
        # Calculate bounding box for the path
        lats = [p[0] for p in path]
        lngs = [p[1] for p in path]
        
        if not lats or not lngs:
             return 100.0, []
             
        padding = 0.02 # approx 2km buffer
        min_lat, max_lat = min(lats) - padding, max(lats) + padding
        min_lng, max_lng = min(lngs) - padding, max(lngs) + padding

        # Optimization: Filter in DB using bounding box to avoid fetching 48k records
        # Cast string lat/lon to float for comparison
        query = select(CrimeReport).where(
            CrimeReport.status.in_(['verified', 'pending', 'investigating']),
            cast(CrimeReport.latitude, Float).between(min_lat, max_lat),
            cast(CrimeReport.longitude, Float).between(min_lng, max_lng)
        )
        
        try:
            result = await db.execute(query)
            all_crimes = result.scalars().all()
        except Exception as e:
            logger.error(f"Database Query Error: {e}")
            return 100.0, []
        
        # Further processing in memory (fine for smaller subset)
        crimes = all_crimes # Already filtered by bbox
        
        processed_crimes = set()
        
        for lat, lng in path:
            for crime in crimes:
                try:
                    c_lat = float(crime.latitude)
                    c_lng = float(crime.longitude)
                except: continue

                # Check if crime is within 200m (0.2km) - further reduced for precision
                # 0.0018 degrees approx 200m
                if abs(c_lat - lat) < 0.0018 and abs(c_lng - lng) < 0.0018:
                    if crime.id not in processed_crimes:
                        # Updated weights for dense dataset (48k records)
                        # VERY CONSERVATIVE SCORING
                        # With 48k records, we assume minor crimes are frequent but low risk
                        cat = str(crime.category).lower()
                        weight = 0.1 # default (other/fraud)
                        
                        if 'theft' in cat: weight = 0.2
                        elif 'burglary' in cat: weight = 0.5
                        elif 'harassment' in cat: weight = 0.8
                        elif 'riot' in cat or 'vandalism' in cat: weight = 1.0
                        elif 'assault' in cat: weight = 1.5
                        elif 'robbery' in cat: weight = 2.5
                        elif 'murder' in cat: weight = 5.0
                        elif 'kidnap' in cat: weight = 5.0
                        
                        local_incident_risk += weight
                        processed_crimes.add(crime.id)
                        hotspots.append(Location(latitude=c_lat, longitude=c_lng))
        
        # Combine Risks
        # Regional Risk (0-100) is general "feeling" of the area.
        # Local Risk is specific "incidents" on the path.
        
        # Normalize local risk using a logarithmic scale to handle density
        # With lower weights:
        # 10 score (e.g. 50 thefts or 4 robberies) -> ~9.5% risk
        # 50 score -> ~40% risk
        # Formula: risk_impact = 100 * (1 - e^(-0.01 * local_score))
        # Adjusted exponent to 0.01 to be even more forgiving (requires 100 points for 63% risk)
        import math
        normalized_local_risk = 100.0 * (1.0 - math.exp(-0.01 * local_incident_risk))
        
        # Weighted Average: 
        # 30% Regional (Background radiation)
        # 70% Local (Active threats) - reduced form 80%
        # If regional is high (60), it contributes 18 points.
        # So baseline safety is 82%. Local crimes subtract from there.
        total_risk_score = (avg_regional_risk * 0.3) + (normalized_local_risk * 0.7)
        
        # Safety Score is inverse of Risk
        safety_score = max(0.0, 100.0 - total_risk_score)
        
        return safety_score, hotspots

    def _calculate_offset_point(self, start: Location, end: Location, offset_pct: float = 0.2, right: bool = True) -> Tuple[float, float]:
        """
        Calculate a waypoint offset from the midpoint of the straight line.
        """
        # Midpoint
        mid_lat = (start.latitude + end.latitude) / 2
        mid_lon = (start.longitude + end.longitude) / 2
        
        # Bearing from start to end
        d_lon = end.longitude - start.longitude
        y = math.sin(d_lon) * math.cos(end.latitude)
        x = math.cos(start.latitude) * math.sin(end.latitude) - math.sin(start.latitude) * math.cos(end.latitude) * math.cos(d_lon)
        bearing = math.atan2(y, x)
        
        # Add 90 degrees (pi/2) for offset direction
        offset_bearing = bearing + (math.pi / 2 if right else -math.pi / 2)
        
        # Distance (approx in degrees, rough heuristic)
        # Total distance
        dist = math.sqrt((end.latitude - start.latitude)**2 + (end.longitude - start.longitude)**2)
        offset_dist = dist * offset_pct
        
        # New point
        new_lat = mid_lat + offset_dist * math.cos(offset_bearing)
        new_lon = mid_lon + offset_dist * math.sin(offset_bearing)
        
        return new_lat, new_lon

    async def _fetch_osrm_route_via(self, start: Location, end: Location, waypoint: Tuple[float, float]) -> Optional[dict]:
        """Fetch a single OSRM route passing through a waypoint"""
        # Format: {lon},{lat};{lon},{lat};{lon},{lat}
        url = f"http://router.project-osrm.org/route/v1/driving/{start.longitude},{start.latitude};{waypoint[1]},{waypoint[0]};{end.longitude},{end.latitude}"
        params = {
            "overview": "full",
            "geometries": "geojson"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == "Ok" and data.get("routes"):
                        return data.get("routes")[0]
        except Exception as e:
            logger.error(f"OSRM Waypoint Fetch Error: {e}")
        return None

    async def calculate_routes(self, request: RouteRequest, db: AsyncSession) -> List[RouteResponse]:
        """
        Generate exactly 3 routes: Safest, Fastest, and Optimal.
        Uses OSRM for real paths.
        """
        candidates = []
        
        # Helper to build RouteResponse
        def build_response(rid, points, dist_km, safety, hotspots):
            segments = []
            for pt in points:
                segments.append(RouteSegment(latitude=pt[0], longitude=pt[1], crime_score=(100-safety)/10))
            
            # Simple composite: safety is 70% weight, distance is 30%
            dist_score = max(0.0, 100.0 - (dist_km * 2.0))
            composite = (safety * 0.7) + (dist_score * 0.3)
            
            return RouteResponse(
                route_id=rid,
                path=segments,
                distance_km=round(dist_km, 2),
                duration_minutes=int(dist_km * 60 / 30), # default 30km/h
                safety_score=round(safety, 1),
                composite_score=round(composite, 1),
                crime_hotspots=hotspots,
                route_type="Optimal"
            )

        # 1. Try OSRM (Primary)
        osrm_routes = await self._fetch_osrm_routes(request.source, request.destination)
        
        if osrm_routes:
            logger.info(f"✅ OSRM returned {len(osrm_routes)} distinct initial routes")
            for i, r in enumerate(osrm_routes):
                coordinates = r['geometry']['coordinates']
                path = [(c[1], c[0]) for c in coordinates]
                dist_km = r['legs'][0]['distance'] / 1000.0
                safety, hotspots = await self._calculate_path_risk(path, db)
                candidates.append(build_response(f"route_osrm_{i}", path, dist_km, safety, hotspots))
        else:
            logger.warning("⚠️ OSRM returned no routes or failed")
        
        # 2. Force Diversity if fewer than 3 routes
        # Instead of fake curves, force OSRM to route through intermediate waypoints
        needed = 3 - len(candidates)
        if needed > 0:
            logger.info(f"ℹ️ Fetching {needed} alternative real routes via waypoints")
            
            # Alt 1: Deviate Right
            if needed >= 1:
                wp1 = self._calculate_offset_point(request.source, request.destination, offset_pct=0.15, right=True)
                r_alt1 = await self._fetch_osrm_route_via(request.source, request.destination, wp1)
                if r_alt1:
                    coordinates = r_alt1['geometry']['coordinates']
                    path = [(c[1], c[0]) for c in coordinates]
                    dist_km = r_alt1['legs'][0]['distance'] / 1000.0 + r_alt1['legs'][1]['distance'] / 1000.0
                    safety, hotspots = await self._calculate_path_risk(path, db)
                    candidates.append(build_response("route_alt_right", path, dist_km, safety, hotspots))

            # Alt 2: Deviate Left
            needed = 3 - len(candidates) # Recheck
            if needed >= 1:
                wp2 = self._calculate_offset_point(request.source, request.destination, offset_pct=0.15, right=False)
                r_alt2 = await self._fetch_osrm_route_via(request.source, request.destination, wp2)
                if r_alt2:
                    coordinates = r_alt2['geometry']['coordinates']
                    path = [(c[1], c[0]) for c in coordinates]
                    dist_km = r_alt2['legs'][0]['distance'] / 1000.0 + r_alt2['legs'][1]['distance'] / 1000.0
                    safety, hotspots = await self._calculate_path_risk(path, db)
                    candidates.append(build_response("route_alt_left", path, dist_km, safety, hotspots))

            # Fallback: If still not enough (e.g. OSRM failed waypoints), use straight line ONLY then
            needed = 3 - len(candidates)
            if needed > 0:
                 # Sim (Zigzag) as last resort
                path3 = self._generate_path(request.source, request.destination, num_points=20, curve_factor=0.0)
                safety3, hotspots3 = await self._calculate_path_risk(path3, db)
                dist_base = self._haversine_distance(request.source.latitude, request.source.longitude, request.destination.latitude, request.destination.longitude)
                candidates.append(build_response("route_fallback", path3, dist_base, safety3, hotspots3))

        
        # 3. Categorize Routes - FORCE DIVERSITY
        # Per user request:
        # Route 1 = Best Path (Optimal/Balanced)
        # Route 2 = Second Best (Safest - prioritized for safety app)
        # Route 3 = Third (Shortest/Fastest)
        
        sorted_by_safety = sorted(candidates, key=lambda x: x.safety_score, reverse=True)
        sorted_by_dist = sorted(candidates, key=lambda x: x.distance_km)
        sorted_by_optimal = sorted(candidates, key=lambda x: x.composite_score, reverse=True)
        
        used_ids = set()
        final_routes = []
        
        # 1. Route 1 (Best/Optimal)
        route1 = sorted_by_optimal[0]
        r1 = route1.model_copy()
        r1.route_type = "Route 1"
        r1.route_id = f"{route1.route_id}_route1"
        final_routes.append(r1)
        used_ids.add(route1.route_id)
        
        # 2. Route 2 (Safest)
        # Find safest route not used as Route 1 (if possible)
        route2 = next((r for r in sorted_by_safety if r.route_id not in used_ids), sorted_by_safety[0])
        
        # If forced to reuse, maybe try finding second safest?
        if route2.route_id in used_ids and len(sorted_by_safety) > 1:
             # If duplicate, try next best safe route if valid
             route2 = sorted_by_safety[1]

        r2 = route2.model_copy()
        r2.route_type = "Route 2"
        r2.route_id = f"{route2.route_id}_route2"
        final_routes.append(r2)
        used_ids.add(route2.route_id)
        
        # 3. Route 3 (Shortest/Fastest)
        # Find shortest distance route not used
        route3 = next((r for r in sorted_by_dist if r.route_id not in used_ids), sorted_by_dist[0])
        
        # If duplicate, try next best dist
        if route3.route_id in used_ids and len(sorted_by_dist) > 1:
            route3 = sorted_by_dist[1]
            
        r3 = route3.model_copy()
        r3.route_type = "Route 3"
        r3.route_id = f"{route3.route_id}_route3"
        final_routes.append(r3)
        
        return final_routes

route_service = RouteService()

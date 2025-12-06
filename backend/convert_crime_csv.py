import pandas as pd
import json
import random
import math
import uuid
from datetime import datetime, timedelta

# Constants
TARGET_USER_ID = "d5237340-9358-4542-ab37-b969ba3687b8"

# Category Mapping
CATEGORY_MAP = {
    'Dacoity': 'robbery',
    'Robbery': 'robbery',
    'Murder': 'assault',
    'Speedy Trial': 'other',
    'Riot': 'vandalism',
    'Woman & Child Repression': 'harassment',
    'Kidnapping': 'other',
    'Police Assault': 'assault',
    'Burglary': 'burglary',
    'Theft': 'theft',
    'Other Cases': 'other',
    'RC Arms Act': 'other',
    'RC Explosive Act': 'other',
    'RC Narcotics': 'other',
    'RC Smuggling': 'other'
}

def load_risk_model(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_random_point(center_lat, center_lon, radius_km):
    # Convert radius from km to degrees (roughly)
    radius_deg = radius_km / 111.0
    
    u = random.random()
    v = random.random()
    
    w = radius_deg * math.sqrt(u)
    t = 2 * math.pi * v
    
    x = w * math.cos(t)
    y = w * math.sin(t)
    
    new_lat = center_lat + x
    new_lon = center_lon + y
    
    return new_lat, new_lon

def parse_date(date_str):
    # Format: Jan-20
    try:
        dt = datetime.strptime(date_str, "%b-%y")
        # Spread randomly within the month
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return dt.replace(day=day, hour=hour, minute=minute)
    except:
        return datetime.now()

def main():
    print("Loading data...")
    df = pd.read_csv('bangladesh_crime_data_full.csv')
    risk_model = load_risk_model('scripts/crime_risk_model.json')
    
    output_rows = []
    
    print("Processing rows...")
    for idx, row in df.iterrows():
        unit = row['Names of Unit']
        
        # Skip if unit location not known
        if unit not in risk_model:
            continue
            
        unit_info = risk_model[unit]['location']
        u_lat = unit_info['lat']
        u_lon = unit_info['lon']
        u_rad = unit_info.get('radius_km', 10)
        
        incident_date = parse_date(row['Date'])
        
        # Iterate through crime columns
        for crime_type, category in CATEGORY_MAP.items():
            if crime_type in df.columns:
                try:
                    val = row[crime_type]
                    if pd.isna(val):
                        count = 0
                    else:
                        count = int(round(float(val)))
                except:
                    count = 0
                
                # Limit count to avoid generating millions of rows for large stats
                # For demo/map visual purposes, capped at 5 per type per month per unit
                # (You can remove this cap for full import, but 1323 narcotics cases might flood it)
                if count > 5:
                    count = 5 
                
                for _ in range(count):
                    lat, lon = generate_random_point(u_lat, u_lon, u_rad)
                    
                    output_rows.append({
                        'user_id': TARGET_USER_ID,
                        'category': category,
                        'title': f"Reported {crime_type}",
                        'description': f"Historical record of {crime_type} in {unit} area.",
                        'incident_date_time': incident_date.isoformat(),
                        'latitude': str(lat),
                        'longitude': str(lon),
                        'location_name': f"{unit} Area",
                        'status': 'verified',
                        'verified': True,
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    })

    print(f"Generated {len(output_rows)} incidents.")
    
    out_df = pd.DataFrame(output_rows)
    out_df.to_csv('supabase_import_crimes.csv', index=False)
    print("Done! Saved to supabase_import_crimes.csv")

if __name__ == "__main__":
    main()

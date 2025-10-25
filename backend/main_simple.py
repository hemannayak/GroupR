from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional
import random
from datetime import datetime
import os

app = FastAPI(title="CrisisLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data on startup
EVENTS = []

@app.on_event("startup")
async def startup():
    global EVENTS
    
    # City coordinates (lat, lon)
    CITY_COORDS = {
        'Hyderabad': (17.3850, 78.4867),
        'Mumbai': (19.0760, 72.8777),
        'Delhi': (28.6139, 77.2090),
        'Bangalore': (12.9716, 77.5946),
        'Chennai': (13.0827, 80.2707),
        'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567),
        'Ahmedabad': (23.0225, 72.5714),
    }
    
    try:
        # Try to load from data directory
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'disaster_tweets.csv')
        df = pd.read_csv(data_path)
        df = df[df['target'] == 1].head(200)  # Load more events
        
        for _, row in df.iterrows():
            location = str(row.get('location', 'Mumbai'))
            
            # Get base coordinates for the city
            if location in CITY_COORDS:
                base_lat, base_lon = CITY_COORDS[location]
            else:
                base_lat, base_lon = CITY_COORDS['Mumbai']  # Default to Mumbai
            
            # Add small random offset for variety (within ~5km)
            lat = base_lat + random.uniform(-0.05, 0.05)
            lon = base_lon + random.uniform(-0.05, 0.05)
            
            EVENTS.append({
                'id': str(row['id']),
                'text': str(row['text']),
                'keyword': str(row.get('keyword', 'other')),
                'location': location,
                'severity': str(row.get('severity', random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']))),
                'type': str(row.get('keyword', 'other')).upper(),
                'timestamp': datetime.now().isoformat(),
                'lat': lat,
                'lon': lon,
            })
        print(f"✅ Loaded {len(EVENTS)} events across {len(set([e['location'] for e in EVENTS]))} cities")
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        # Create some dummy data with proper coordinates
        for i in range(40):
            location = random.choice(list(CITY_COORDS.keys()))
            base_lat, base_lon = CITY_COORDS[location]
            
            EVENTS.append({
                'id': f'event_{i}',
                'text': f'Sample disaster event {i} in {location}',
                'keyword': random.choice(['earthquake', 'flood', 'fire']),
                'location': location,
                'severity': random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
                'type': random.choice(['EARTHQUAKE', 'FLOOD', 'FIRE']),
                'timestamp': datetime.now().isoformat(),
                'lat': base_lat + random.uniform(-0.05, 0.05),
                'lon': base_lon + random.uniform(-0.05, 0.05),
            })
        print(f"✅ Created {len(EVENTS)} dummy events")

@app.get("/health")
def health():
    return {"status": "healthy", "events": len(EVENTS)}

@app.get("/stats")
def get_stats():
    severities = {}
    types = {}
    for event in EVENTS:
        severities[event['severity']] = severities.get(event['severity'], 0) + 1
        types[event['type']] = types.get(event['type'], 0) + 1
    
    return {
        "total_events": len(EVENTS),
        "events_per_minute": random.randint(5, 15),
        "severity_distribution": severities,
        "disaster_types": types,
        "critical": severities.get('CRITICAL', 0),
        "new_last_hour": random.randint(5, 15),
        "critical_change": random.randint(-2, 5)
    }

@app.get("/events")
def get_events(limit: int = 50):
    return EVENTS[:limit]

@app.get("/events/map-data")
def get_map_data():
    return EVENTS

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_events(req: QueryRequest):
    question_lower = req.question.lower()
    
    # Simple keyword matching
    relevant = []
    for event in EVENTS:
        if any(word in event['text'].lower() for word in question_lower.split()):
            relevant.append(event)
    
    relevant = relevant[:5]
    
    if not relevant:
        answer = "No relevant disaster events found for your query."
    else:
        answer = f"Found {len(relevant)} relevant events. "
        if 'critical' in question_lower:
            critical = [e for e in relevant if e['severity'] == 'CRITICAL']
            if critical:
                answer += f"Most critical: {critical[0]['text'][:100]}..."
        else:
            answer += f"Recent event: {relevant[0]['text'][:100]}..."
    
    return {
        "answer": answer,
        "sources": [e['id'] for e in relevant],
        "relevant_events": relevant,
        "confidence": 0.8 if relevant else 0.3
    }

@app.get("/resources")
def get_resources():
    return [
        {"id": "R001", "type": "RESCUE_TEAM", "location": "Central Station", "available": True},
        {"id": "R002", "type": "MEDICAL", "location": "City Hospital", "available": True},
        {"id": "R003", "type": "SUPPLIES", "location": "Warehouse A", "available": True},
    ]

@app.get("/agent/decisions")
def get_agent_decisions():
    decisions = []
    critical_events = [e for e in EVENTS if e['severity'] == 'CRITICAL'][:3]
    for event in critical_events:
        decisions.append({
            "timestamp": datetime.now().isoformat(),
            "event_id": event['id'],
            "priority_score": random.randint(80, 100),
            "recommended_action": f"Deploy resources to {event['location']}",
            "assigned_resources": ["R001", "R002"],
            "reasoning": f"High priority {event['type']} event requiring immediate response.",
            "event_text": event['text']
        })
    return decisions

@app.get("/report")
def generate_report():
    critical = [e for e in EVENTS if e['severity'] == 'CRITICAL']
    high = [e for e in EVENTS if e['severity'] == 'HIGH']
    
    report = f"""# Crisis Situation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- Total Events: {len(EVENTS)}
- Critical Situations: {len(critical)}
- High Priority: {len(high)}

## Top Critical Events
"""
    for i, event in enumerate(critical[:5], 1):
        report += f"\n{i}. **{event['type']}** - {event['location']}\n   {event['text'][:100]}...\n"
    
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

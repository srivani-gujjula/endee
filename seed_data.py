"""
Emergency Resource Seed Data (India-focused)
These get embedded into Endee vector DB on startup.
"""

EMERGENCY_RESOURCES = [
    # ── Hospitals ──
    {
        "id": "hosp_001",
        "type": "hospital",
        "icon": "🏥",
        "name": "City General Hospital",
        "address": "12 MG Road, Sector 4, New Delhi",
        "phone": "011-2345-6789",
        "distance_km": 0.3,
        "is_open": True,
        "description": "Multi-specialty hospital with 24/7 emergency medical services, ICU, surgery, trauma care, doctor on call"
    },
    {
        "id": "hosp_002",
        "type": "hospital",
        "icon": "🏥",
        "name": "St. Mary's Clinic & Hospital",
        "address": "Lajpat Nagar, Main Road, New Delhi",
        "phone": "011-4455-6677",
        "distance_km": 1.8,
        "is_open": True,
        "description": "General hospital with outpatient and emergency clinic, doctor consultations, medical treatment"
    },
    {
        "id": "hosp_003",
        "type": "hospital",
        "icon": "🏥",
        "name": "AIIMS Emergency Wing",
        "address": "Ansari Nagar, Aurobindo Marg, New Delhi",
        "phone": "011-2659-3000",
        "distance_km": 3.2,
        "is_open": True,
        "description": "Premier medical institute with world-class emergency care, trauma center, all specialties available 24 hours"
    },

    # ── Police ──
    {
        "id": "pol_001",
        "type": "police",
        "icon": "🚔",
        "name": "Central Police Station",
        "address": "Civil Lines, Block B, New Delhi",
        "phone": "100",
        "distance_km": 0.6,
        "is_open": True,
        "description": "Main police station handling crime reports, emergencies, law enforcement, security, patrol, FIR"
    },
    {
        "id": "pol_002",
        "type": "police",
        "icon": "🚔",
        "name": "Traffic Police Control Post",
        "address": "Ring Road Junction 3, New Delhi",
        "phone": "100",
        "distance_km": 2.3,
        "is_open": True,
        "description": "Traffic police post handling road accidents, vehicle emergencies, signal violations, traffic law enforcement"
    },

    # ── Fire ──
    {
        "id": "fire_001",
        "type": "fire",
        "icon": "🚒",
        "name": "Fire Brigade Station No. 7",
        "address": "Industrial Area Gate 2, Okhla, New Delhi",
        "phone": "101",
        "distance_km": 1.1,
        "is_open": True,
        "description": "Fire station with rescue teams, firefighting equipment, hazmat response, burning building emergency, smoke"
    },
    {
        "id": "fire_002",
        "type": "fire",
        "icon": "🚒",
        "name": "Fire & Rescue Services HQ",
        "address": "Connaught Place, New Delhi",
        "phone": "101",
        "distance_km": 2.7,
        "is_open": True,
        "description": "Headquarters fire rescue service handling large scale emergencies, industrial accidents, rescue operations"
    },

    # ── Blood Banks ──
    {
        "id": "blood_001",
        "type": "blood",
        "icon": "🩸",
        "name": "Red Cross Blood Bank",
        "address": "Gandhi Nagar, Near Central Park, New Delhi",
        "phone": "011-9988-7766",
        "distance_km": 1.4,
        "is_open": True,
        "description": "Blood bank for donation and transfusion, all blood types available, plasma, platelets, donor registration"
    },
    {
        "id": "blood_002",
        "type": "blood",
        "icon": "🩸",
        "name": "Rotary Blood Bank",
        "address": "Sector 12, RK Puram, New Delhi",
        "phone": "011-2617-0003",
        "distance_km": 2.5,
        "is_open": False,
        "description": "Voluntary blood donation center, blood type O positive negative, rare blood groups, emergency supply"
    },

    # ── Ambulance ──
    {
        "id": "amb_001",
        "type": "ambulance",
        "icon": "🚑",
        "name": "24/7 Ambulance Response Hub",
        "address": "Nehru Place, Ground Floor, New Delhi",
        "phone": "108",
        "distance_km": 0.8,
        "is_open": True,
        "description": "Emergency ambulance service with paramedics, advanced life support, patient transport, critical injury"
    },
    {
        "id": "amb_002",
        "type": "ambulance",
        "icon": "🚑",
        "name": "CATS Ambulance Service",
        "address": "Centralized Dispatch, ITO, New Delhi",
        "phone": "102",
        "distance_km": 1.5,
        "is_open": True,
        "description": "Centralized ambulance service trauma response, urgent medical transport, accident victims, cardiac emergency"
    },

    # ── Shelters ──
    {
        "id": "shelt_001",
        "type": "shelter",
        "icon": "🏠",
        "name": "Disaster Relief Shelter — Sector 9",
        "address": "Community Hall, Sector 9, New Delhi",
        "phone": "1078",
        "distance_km": 2.1,
        "is_open": False,
        "description": "Temporary shelter for flood disaster refugees, cyclone victims, earthquake relief housing, food water"
    },
    {
        "id": "shelt_002",
        "type": "shelter",
        "icon": "🏠",
        "name": "NDRF Relief Camp",
        "address": "Ground, Jawaharlal Nehru Stadium, New Delhi",
        "phone": "011-2436-0016",
        "distance_km": 3.0,
        "is_open": True,
        "description": "National disaster response force camp, emergency temporary housing, medical aid, flood relief, disaster management"
    },
]
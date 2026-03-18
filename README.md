# 🚨 ResQ AI — Emergency Resource Locator

> Built using **Endee Vector Database** 

---

## 📌 Project Overview

**ResQ AI** is an AI-powered emergency resource locator that uses **Endee** as the vector database for semantic search. It helps users instantly find the nearest:

- 🏥 Hospitals & Clinics
- 🚔 Police Stations
- 🚒 Fire Brigades
- 🩸 Blood Banks
- 🚑 Ambulance Services
- 🏠 Disaster Shelters

---

## 🧠 Use of Endee Vector Database

Endee is the **core search engine** of this project. Here is how it is used:

1. All emergency resources are converted to **48-dimensional vectors** using text embedding
2. Vectors are stored in an Endee index named `emergency_resources`
3. When a user types a query, it is embedded and matched using **HNSW cosine similarity search**
4. Endee returns the most relevant resources ranked by similarity score

**Example:**
- User types → `"I need a doctor urgently"`
- Endee finds → `City General Hospital` (score: 0.9721)
- Even though the word "hospital" was not typed — Endee understands the meaning

**Endee Index Config:**
```
Name       : emergency_resources
Dimensions : 48
Space Type : Cosine Similarity
Precision  : INT8
Algorithm  : HNSW (M=16, ef=128)
```

---

## ✨ Features

- 📍 Live GPS tracking — updates as you move
- 🔍 Semantic search via Endee — finds resources by meaning
- 🗺️ Real nearby places — from OpenStreetMap (free, no API key)
- 📞 One-tap calling — direct phone dial on mobile
- 🗺️ Google Maps directions — instant navigation
- 🤖 AI chat assistant — natural language emergency queries
- 🆘 SOS button — all emergency numbers (112, 100, 101, 108)
- 📤 Share location — sends your GPS link

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Endee** (endee-io/endee) | Vector database — semantic search |
| **FastAPI** (Python 3.11) | Backend REST API |
| **HTML5 / JS** | Frontend — single file UI |
| **OpenStreetMap** | Free real nearby places data |
| **Browser Geolocation API** | Live GPS tracking |
| **Docker Compose** | Run Endee + FastAPI together |

---

## 📁 Project Structure

```
resq-ai/
├── app/
│   ├── main.py            # FastAPI routes
│   ├── endee_client.py    # Endee SDK integration
│   ├── seed_data.py       # Emergency resources data
│   └── __init__.py
├── frontend/
│   └── index.html         # Complete UI
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Setup Instructions

### Without Docker

```bash
# 1. Clone this repo
git clone https://github.com/srivani-gujjula/endee
cd endee/resq-ai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload --port 5000

# 5. Open browser
http://localhost:5000
```

### With Docker (Full Endee Integration)

```bash
docker compose up -d

# Frontend : http://localhost:5000
# Endee DB : http://localhost:8080
```

---

## 📞 India Emergency Numbers

| Number | Service |
|---|---|
| **112** | All Emergencies |
| **100** | Police |
| **101** | Fire Brigade |
| **108** | Ambulance (Free) |
| **104** | Medical Helpline |

---

**Built by:** Srivani Gujjula   
**Date:** March 2026

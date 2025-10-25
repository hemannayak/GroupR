* * * * *

🚨 CrisisLens AI
================

### Real-time Disaster Intelligence Platform

![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen)

* * * * *

🌟 Key Features
---------------

-   🚨 **Real-time Disaster Detection**\
    Monitors floods, fires, earthquakes, and more from social, news, and community inputs (live or demo mode).

-   🗺️ **Interactive Map Dashboard**\
    Severity-based visualization of crisis events (Critical, High, Medium, Low).

-   🤖 **AI-Powered Crisis Extraction**\
    Classifies events, identifies rescue needs, and geolocates areas using NLP.

-   📊 **Automated Situation Reports**\
    Top urgent SOS signals summarized for quick decision making.

-   🔍 **Semantic Search**\
    AI-powered retrieval of most relevant incidents.

-   🚦 **Severity-First Prioritization**\
    Critical alerts are always surfaced first.

-   📱 **Planned Alerts**\
    Email/SMS push alerts for CRITICAL events in future releases.

* * * * *

🎯 Problem Statement
--------------------

Disaster responders face:

-   Overwhelming volume of unstructured data

-   Delayed identification of life-threatening emergencies

-   Redundant and unverifiable reporting

-   Poor real-time triage and resource allocation

**Real-world impact example:**\
During Kerala 2018 floods, several high-risk SOS posts were missed or delayed due to lack of prioritization.

* * * * *

💡 Solution Overview
--------------------

CrisisLens AI provides:

✅ Unified ingestion across multi-source crisis streams\
✅ Automatic deduplication, severity scoring, and entity extraction\
✅ Map-based dashboards for response centers and NGOs\
✅ AI-generated situation reports for faster rescue actions\
✅ Free and open for public benefit (MIT License)

* * * * *

🏆 Uniqueness & Competitive Advantages
--------------------------------------

| Capability | CrisisLens AI | Traditional Systems |
| --- | :-: | :-: |
| Severity-based prioritization | ✅ | ❌ |
| Multi-source real-time ingest | ✅ | ❌ |
| AI-powered geolocation + classification | ✅ | Partial |
| Semantic vector search | ✅ | ❌ |
| Open-source & free | ✅ | ❌ |

* * * * *

🏗️ Architecture Overview
-------------------------

### High-Level Architecture

```
graph TD
    subgraph Data Sources
        A1[Twitter - snscrape]
        A2[News Feeds]
        A3[NGO / User Reports]
    end
    A1 --> B[Ingestion Layer]
    A2 --> B
    A3 --> B
    B --> C[Processing Pipeline]
    C --> D[AI Models - HF Transformers]
    D --> E[Vector DB - ChromaDB]
    E --> F[API Layer - FastAPI]
    F --> G1[Map Dashboard - Streamlit]
    F --> G2[Automated Reporting]
    F --> G3[Alerts & Dashboards]

```

### AI/ML Flow

```
graph LR
    A[Incoming Message] --> B[Text Cleaning]
    B --> C[Embeddings: MiniLM, spaCy]
    C --> D[Severity Classification]
    D --> E[Location & Entity Extraction]
    E --> F[Store in ChromaDB]
    F --> G[Semantic Search + RAG]

```

### Severity-driven Prioritization

```
flowchart TD
    IN[New Event] --> PROC[AI Processing]
    PROC --> SEV[Severity: Critical, High, Medium, Low]
    SEV --> SORT[Priority Sorting]
    SORT --> UI[Map & Reports with Priority Ordering]

```

* * * * *

🛠️ Technology Stack
--------------------

**Backend**

-   FastAPI, Python 3.11+

-   HuggingFace Transformers

-   ChromaDB for semantic retrieval

-   snscrape for real-time streams

-   Docker-ready architecture

**Frontend**

-   Streamlit dashboard

-   Folium / Plotly for maps and analytics

* * * * *

🌍 Use Cases
------------

-   Rapid triage of SOS requests in floods

-   Wildfire early-warning detection

-   Earthquake situational overview mapping

-   NGO and government emergency coordination

* * * * *

🚀 Quick Start
--------------

**Requirements**

-   Python 3.11+

-   pip installed

```
git clone https://github.com/yourusername/crisis-lens-ai.git
cd crisis-lens-ai

python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env        # add your HF_TOKEN

```

### Run Sample Demo

```
python3 scripts/quick_sample.py

```

### Start Backend + Frontend

```
uvicorn backend.main_simple:app --reload --port 8000
cd frontend
streamlit run app_simple.py

```

Open in browser:\
[http://localhost:8501](http://localhost:8501/)

* * * * *

📊 Dataset
----------

-   **Sample size**: 300 disaster-related messages (Kaggle + curated synthetic + streamed)

-   **Fields**: text, timestamp, location, severity classification, alert metadata

* * * * *

📌 Core Logic
-------------

Severity definitions:

| Severity | Description |
| --- | --- |
| CRITICAL | Immediate life risk, emergency rescue required |
| HIGH | Risky but not immediately fatal |
| MEDIUM | Needs monitoring |
| LOW | Informational |

Critical messages receive highest UI weight and alert priority.

* * * * *

📄 License
----------

Released under **MIT License**\
Refer to the `LICENSE` file for details.

* * * * *

👥 Contributors
---------------

-   **Lead:** Hemanth Nayak

-   Hackathon collaborators & open-source contributors

* * * * *


* * * * *

**Built for GenAIVersity Hackathon 2025\
Future-ready for NGOs, Government Agencies, and Disaster Relief Teams.**

* * * * *

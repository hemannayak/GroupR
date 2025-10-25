# 🚨 SnapFix - Real-Time Pothole & Road Damage Detection System

## 📋 Problem Statement

India loses over **₹30,000 crores annually** due to pothole-related vehicle damage, and **3,000+ deaths** occur each year from accidents caused by poor road conditions. Hyderabad alone reported **15,000+ potholes** in 2024, with municipality complaint systems like T-RACSHA suffering from:

- **Low Reporting Rate**: Only 5-10% of potholes get manually reported by citizens
- **Delayed Response**: Average repair time of 45+ days after complaint
- **Incomplete Data**: No severity classification or prioritization system
- **Manual Effort**: Citizens must stop, open app, take photo, and manually mark location
- **Spam & Duplicates**: 30-40% of reports are fake or duplicate entries

**The Core Problem**: Existing solutions require high user effort, resulting in sparse coverage and delayed municipal action, leading to continued accidents and vehicle damage.

---

## 💡 Solution

**SnapFix AI** is an intelligent, **zero-friction pothole detection system** that transforms every commuter's smartphone into an automated road quality sensor. Using advanced computer vision and predictive analytics, we:

### Key Features:

1. **Automated Detection**: Background AI detection while users commute - no manual intervention required
2. **Severity Classification**: AI-powered categorization (Small/Medium/Large) with depth estimation
3. **Smart Prioritization**: Risk-based urgency scoring considering traffic density, location type, and weather
4. **Community Verification**: Gamified crowdsourcing system with credibility scores to prevent spam
5. **Predictive Analytics**: ML model predicts high-risk zones for preventive maintenance
6. **Municipality Dashboard**: Real-time heatmaps, cost-benefit analysis, and API integration with GHMC

### How It Works:
```
User commutes → Phone camera + GPS active → YOLOv8 detects pothole → 
Auto-classify severity → GPS marks location → Community verifies → 
Municipality receives prioritized repair list
```

***

## 🌍 Real-World Use Case

### Scenario: Daily Commuter - Priya's Journey

**Before RoadGuard AI:**
- Priya hits a pothole on Gachibowli-HITAM route
- Damages her scooter (₹3,000 repair cost)
- Thinks about reporting but too busy
- Pothole remains unreported for 3 months
- 10+ other vehicles get damaged

**After RoadGuard AI:**
- Priya installs app, keeps phone on dashboard during commute
- App automatically detects 5 potholes on her route in background
- Each pothole gets severity classification + GPS coordinates
- 3 other users verify the detections (credibility +10 points each)
- GHMC receives urgent repair alert for the 8cm deep pothole
- Road fixed within 7 days
- Priya earns 50 points, unlocks "Road Guardian" badge

### Municipal Use Case: GHMC Ward Officer

**Dashboard View:**
- **47 verified potholes** detected in Ward 150 (Gachibowli)
- 12 marked as "HIGH URGENCY" (>7cm depth, high traffic)
- Total estimated repair cost: **₹1.2 lakhs**
- Predictive heatmap shows 8 new high-risk zones for next month
- One-click export for contractor assignment

**Result**: Data-driven resource allocation, 60% faster repair turnaround

***

## 🎯 Impact of Solution

### Quantifiable Impact:

| Metric | Before | After RoadGuard AI | Improvement |
|--------|--------|-------------------|-------------|
| **Pothole Detection Rate** | 5-10% (manual) | 85-90% (automated) | **9x increase** |
| **Citizen Effort** | 5-10 mins per report | 0 mins (passive) | **100% reduction** |
| **Municipality Response Time** | 45+ days | 7-10 days | **75% faster** |
| **Data Quality** | 30% spam/duplicates | <5% (verified) | **83% improvement** |
| **Coverage Density** | Sparse (user-dependent) | Dense (all commuters) | **10x coverage** |
| **Preventive Maintenance** | None | Predictive zones identified | **NEW capability** |

### Social Impact:

✅ **Safety**: Reduce pothole-related accidents by 40-50%  
✅ **Economic**: Save citizens ₹500-1000 crores annually in vehicle damage  
✅ **Efficiency**: Enable data-driven municipal budgeting and planning  
✅ **Accessibility**: Works on any smartphone, no special hardware needed  
✅ **Transparency**: Public dashboard builds government accountability  
✅ **Employment**: Faster repairs = more work for road contractors

### Environmental Impact:
- Preventive maintenance extends road lifespan by 30%
- Reduces need for full road reconstruction (lower carbon footprint)
- Optimized repair routes reduce municipality vehicle emissions

***

## 🛠️ Tech Stack

### **Frontend**
- **Mobile App**: Flutter / React Native (cross-platform)
- **Web Dashboard**: React.js + Tailwind CSS
- **Maps Integration**: Google Maps JavaScript API / Mapbox
- **Real-time Updates**: Firebase Realtime Database

### **Backend**
- **API Server**: Python Flask / FastAPI
- **Database**: PostgreSQL (pothole data) + Firebase (real-time sync)
- **Authentication**: Firebase Auth / JWT
- **Cloud Hosting**: AWS EC2 / Google Cloud Run
- **File Storage**: AWS S3 (for images)

### **AI/ML Pipeline**
- **Object Detection**: YOLOv8 (Ultralytics) - Pre-trained + fine-tuned
- **Depth Estimation**: MiDaS v3.1 (Monocular depth from single image)
- **Severity Classifier**: Custom CNN (TensorFlow/PyTorch)
- **Predictive Model**: XGBoost / Random Forest (risk zone prediction)
- **Image Preprocessing**: OpenCV, PIL
- **Model Serving**: TensorFlow Serving / ONNX Runtime

### **Data & Analytics**
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Folium (heatmaps)
- **Weather API**: OpenWeatherMap API
- **Traffic Data**: Google Maps Traffic Layer API

### **DevOps**
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Version Control**: Git + GitHub

***

## 🏗️ Backend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MOBILE APP (Flutter)                     │
│  Camera Feed → Background Detection → GPS Tagging → Upload   │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Flask/FastAPI)               │
│         /detect  |  /verify  |  /severity  |  /heatmap      │
└────────────┬────────────────────────────────────────────────┘
             │
        ┌────┴────┐
        ▼         ▼
┌──────────────┐  ┌──────────────────────────────────────────┐
│ ML INFERENCE │  │         DATABASE LAYER                   │
│   PIPELINE   │  │  ┌──────────────┐  ┌─────────────────┐  │
│              │  │  │ PostgreSQL   │  │ Firebase        │  │
│ YOLOv8       │◄─┤  │ - Potholes   │  │ - Real-time     │  │
│ Detection    │  │  │ - Users      │  │ - Notifications │  │
│              │  │  │ - Verifications│ │ - Sync          │  │
│ MiDaS Depth  │  │  └──────────────┘  └─────────────────┘  │
│ Estimation   │  │                                          │
│              │  │  ┌──────────────┐  ┌─────────────────┐  │
│ Severity     │  │  │ Redis Cache  │  │ AWS S3          │  │
│ Classifier   │  │  │ - API Cache  │  │ - Images        │  │
│              │  │  │ - Session    │  │ - Model Files   │  │
└──────┬───────┘  │  └──────────────┘  └─────────────────┘  │
       │          └──────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│              ANALYTICS & PREDICTION ENGINE                   │
│  Risk Scoring → Heatmap Generation → Predictive Model       │
│  (XGBoost + Historical Data + Weather + Traffic)            │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│               MUNICIPALITY DASHBOARD (React)                 │
│  Ward-wise View | Urgency Sorting | Cost Analysis | Export  │
└─────────────────────────────────────────────────────────────┘
```

### **Data Flow:**

1. **Detection Phase**:
   - User's phone camera captures frames every 2 seconds
   - YOLOv8 model runs on-device (TensorFlow Lite) or sends to server
   - Confidence score >0.6 triggers pothole detection
   - GPS coordinates + timestamp + image uploaded to backend

2. **Classification Phase**:
   - MiDaS depth estimation calculates pothole depth
   - CNN severity classifier assigns Small/Medium/Large label
   - Risk score computed using traffic density + road type + weather

3. **Verification Phase**:
   - Nearby users receive notification to verify detection
   - 3+ verifications → "Confirmed" status
   - False reports reduce user credibility score

4. **Action Phase**:
   - Confirmed potholes appear on municipality dashboard
   - Auto-prioritized by urgency score
   - API integration with GHMC complaint system

***

## 🏛️ Architecture Diagram

```
                    ┌───────────────────────────────────┐
                    │   FRONTEND LAYER                  │
                    │                                   │
                    │  ┌─────────────┐  ┌────────────┐ │
                    │  │ Mobile App  │  │ Web Portal │ │
                    │  │  (Flutter)  │  │  (React)   │ │
                    │  └──────┬──────┘  └─────┬──────┘ │
                    └─────────┼────────────────┼────────┘
                              │                │
                    ┌─────────┴────────────────┴────────┐
                    │      LOAD BALANCER (Nginx)        │
                    └─────────┬─────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
    ┌───────▼───────┐ ┌───────▼───────┐ ┌──────▼──────┐
    │ API Server 1  │ │ API Server 2  │ │API Server 3 │
    │   (FastAPI)   │ │   (FastAPI)   │ │  (FastAPI)  │
    └───────┬───────┘ └───────┬───────┘ └──────┬──────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
    ┌─────────▼──────────┐        ┌──────────▼─────────┐
    │  ML INFERENCE      │        │   DATA LAYER       │
    │  ┌──────────────┐  │        │  ┌──────────────┐  │
    │  │ YOLOv8       │  │        │  │ PostgreSQL   │  │
    │  │ (ONNX)       │  │        │  │ (Master)     │  │
    │  └──────────────┘  │        │  └──────┬───────┘  │
    │  ┌──────────────┐  │        │         │          │
    │  │ MiDaS        │  │        │  ┌──────▼───────┐  │
    │  │ (Depth)      │  │        │  │ PostgreSQL   │  │
    │  └──────────────┘  │        │  │ (Replica)    │  │
    │  ┌──────────────┐  │        │  └──────────────┘  │
    │  │ Severity CNN │  │        │  ┌──────────────┐  │
    │  └──────────────┘  │        │  │ Redis Cache  │  │
    └────────────────────┘        │  └──────────────┘  │
                                  │  ┌──────────────┐  │
                                  │  │ Firebase     │  │
                                  │  │ Realtime DB  │  │
                                  │  └──────────────┘  │
                                  └────────────────────┘
                                           │
                              ┌────────────┴────────────┐
                              │   ANALYTICS ENGINE      │
                              │  ┌──────────────────┐   │
                              │  │ XGBoost Model    │   │
                              │  │ (Prediction)     │   │
                              │  └──────────────────┘   │
                              │  ┌──────────────────┐   │
                              │  │ Heatmap Generator│   │
                              │  └──────────────────┘   │
                              └─────────────────────────┘
```

***

## 🌟 Why It Is Unique

### **Compared to Existing Solutions:**

| Feature | T-RACSHA (Govt) | Waze | iWatchRoad | **SnapFix AI** |
|---------|----------------|------|-----------|-----------------|
| Detection Method | Manual | Manual | Dashcam | ✅ **Auto (Phone)** |
| User Effort | High | Medium | Medium | ✅ **Zero** |
| Hardware Required | Smartphone | Smartphone | Dashcam | ✅ **Smartphone Only** |
| AI Detection | ❌ | ❌ | ✅ | ✅ |
| Severity Classification | ❌ | ❌ | ❌ | ✅ |
| Community Verification | ❌ | Basic | ❌ | ✅ **Gamified** |
| Predictive Analytics | ❌ | ❌ | ❌ | ✅ |
| Municipality Integration | Manual | ❌ | ❌ | ✅ **API + Dashboard** |
| Spam Prevention | ❌ | Basic | ❌ | ✅ **Credibility System** |
| Cost-Benefit Analysis | ❌ | ❌ | ❌ | ✅ |

### **Core Innovations:**

1. **Zero-Friction Detection**: First solution to enable truly passive, background detection without user intervention

2. **Predictive Maintenance**: Only platform that predicts where potholes will form next using ML on historical + environmental data

3. **Community Intelligence**: Gamified verification system with credibility scoring prevents spam while increasing engagement

4. **Decision-Ready Data**: Provides municipalities with urgency scores, cost estimates, and repair prioritization - not just location data

5. **Hyperlocal Optimization**: Hyderabad-specific features (GHMC integration, local landmarks, Telugu support) vs generic India-wide tools

***

## 🌍 Social Impact & Alignment

### **UN Sustainable Development Goals (SDGs):**

✅ **SDG 3 - Good Health & Well-being**: Reduce road accident injuries/deaths  
✅ **SDG 9 - Industry, Innovation & Infrastructure**: Smart infrastructure monitoring  
✅ **SDG 11 - Sustainable Cities**: Make cities safer, resilient, and sustainable  
✅ **SDG 17 - Partnerships**: Citizen-government collaboration for civic improvement

### **Social Impact Metrics:**

**For Citizens:**
- Save ₹1000-3000/year in vehicle repair costs per person
- Reduce commute stress and accident risk
- Empower civic participation through gamification

**For Government:**
- Enable data-driven budgeting (allocate ₹50 lakhs where needed vs uniform distribution)
- Improve accountability and transparency
- Reduce complaint handling workload by 70%

**For Society:**
- Prevent 1000+ accidents annually in Hyderabad alone
- Create safer roads for vulnerable groups (two-wheeler riders, cyclists)
- Build citizen-government trust through visible action

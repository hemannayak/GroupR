import streamlit as st
import httpx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime
import time

# Page config
st.set_page_config(
    layout="wide", 
    page_title="🚨 CrisisLens AI", 
    page_icon="🚨",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #ff4444, #ff8800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .critical-alert {
        background: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #cc0000;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    .city-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 20px;
        background: #667eea;
        color: white;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 2rem;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# API Config
API_BASE = "http://localhost:8000"

@st.cache_data(ttl=5)
def api_call(endpoint):
    try:
        response = httpx.get(f"{API_BASE}{endpoint}", timeout=5)
        return response.json()
    except Exception as e:
        return None

# Header
st.markdown('<h1 class="main-header">🚨 CrisisLens AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Real-Time Disaster Intelligence & Response Coordination System</p>', unsafe_allow_html=True)

# Check backend
try:
    health = api_call("/health")
    if health:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.success(f"🟢 **Backend Online** | {health.get('events', 0)} events loaded")
        with col2:
            st.info(f"⏱️ Last Update: {datetime.now().strftime('%H:%M:%S')}")
        with col3:
            if st.button("🔄 Refresh Data"):
                st.cache_data.clear()
                st.rerun()
    else:
        st.error("🔴 Backend Offline")
        st.info("Start backend: `cd backend && python3 main_simple.py`")
        st.stop()
except:
    st.error("🔴 Cannot connect to backend")
    st.info("Start backend: `cd backend && python3 main_simple.py`")
    st.stop()

# Sidebar with enhanced stats
with st.sidebar:
    st.markdown("## 📊 Live Dashboard")
    
    stats = api_call("/stats")
    if stats:
        # Key metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Events", stats.get('total_events', 0))
            st.metric("Events/Min", stats.get('events_per_minute', 0))
        with col2:
            st.metric("Critical", stats.get('critical', 0), delta=stats.get('critical_change', 0))
            st.metric("New (1hr)", stats.get('new_last_hour', 0))
        
        st.markdown("---")
        
        # Severity distribution
        if stats.get('severity_distribution'):
            st.markdown("### ⚠️ Severity Levels")
            fig = px.pie(
                values=list(stats['severity_distribution'].values()),
                names=list(stats['severity_distribution'].keys()),
                color_discrete_map={
                    'CRITICAL': '#ff4444',
                    'HIGH': '#ff8800',
                    'MEDIUM': '#ffbb00',
                    'LOW': '#00cc66'
                },
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, height=250, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Disaster types
        if stats.get('disaster_types'):
            st.markdown("### 🔥 Disaster Types")
            fig = px.bar(
                x=list(stats['disaster_types'].values()),
                y=list(stats['disaster_types'].keys()),
                orientation='h',
                color=list(stats['disaster_types'].values()),
                color_continuous_scale='Reds'
            )
            fig.update_layout(
                showlegend=False,
                height=250,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Count",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)

# City filter in main area
st.markdown("### 🌍 City Focus")
events = api_call("/events?limit=500")
if events:
    df_all = pd.DataFrame(events)
    cities = ["All Cities"] + sorted(df_all['location'].unique().tolist())
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        selected_city = st.selectbox("Select City", cities, key="city_filter")
    with col2:
        severity_filter = st.multiselect("Severity", ["CRITICAL", "HIGH", "MEDIUM", "LOW"], default=["CRITICAL", "HIGH"])
    with col3:
        disaster_filter = st.multiselect("Type", df_all['type'].unique(), default=df_all['type'].unique())
    
    # Filter data
    if selected_city != "All Cities":
        df_filtered = df_all[df_all['location'] == selected_city]
    else:
        df_filtered = df_all
    
    df_filtered = df_filtered[
        (df_filtered['severity'].isin(severity_filter)) &
        (df_filtered['type'].isin(disaster_filter))
    ]
    
    # Show city stats
    if selected_city != "All Cities":
        city_critical = len(df_filtered[df_filtered['severity'] == 'CRITICAL'])
        city_high = len(df_filtered[df_filtered['severity'] == 'HIGH'])
        
        if city_critical > 0:
            st.markdown(f"""
            <div class="critical-alert">
                <h3>🚨 CRITICAL ALERT: {selected_city}</h3>
                <p><strong>{city_critical}</strong> critical situations requiring immediate response!</p>
                <p><strong>{city_high}</strong> high-priority events detected.</p>
            </div>
            """, unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Live Crisis Map",
    "💬 AI Query Assistant", 
    "🤖 Agent Decisions",
    "📋 Situation Report",
    "📊 Analytics & Feed"
])

with tab1:
    st.header(f"🗺️ Real-Time Crisis Map - {selected_city}")
    
    if len(df_filtered) > 0:
        # Determine map center
        if selected_city != "All Cities":
            center_lat = df_filtered['lat'].mean()
            center_lon = df_filtered['lon'].mean()
            zoom = 11
        else:
            center_lat = 20.5937
            center_lon = 78.9629
            zoom = 5
        
        # Create map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles='OpenStreetMap')
        
        # Color map
        colors = {'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'green'}
        icons = {'CRITICAL': 'exclamation-triangle', 'HIGH': 'warning-sign', 'MEDIUM': 'info-sign', 'LOW': 'ok-sign'}
        
        # Add markers
        for _, event in df_filtered.head(100).iterrows():
            folium.Marker(
                location=[event['lat'], event['lon']],
                popup=folium.Popup(f"""
                    <div style='width: 250px'>
                        <h4 style='color: {colors.get(event['severity'], 'blue')}'>{event['type']}</h4>
                        <p><strong>Severity:</strong> {event['severity']}</p>
                        <p><strong>Location:</strong> {event['location']}</p>
                        <p>{event['text'][:150]}...</p>
                    </div>
                """, max_width=300),
                icon=folium.Icon(
                    color=colors.get(event['severity'], 'blue'),
                    icon=icons.get(event['severity'], 'info-sign')
                )
            ).add_to(m)
        
        # Display map
        st_folium(m, width=1400, height=600)
        
        # Legend
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown("🔴 **Critical** - Immediate action required")
        col2.markdown("🟠 **High** - Urgent response needed")
        col3.markdown("🟡 **Medium** - Monitor situation")
        col4.markdown("🟢 **Low** - Informational")
        
        st.info(f"📍 Showing {len(df_filtered)} events for {selected_city}")
    else:
        st.warning(f"No events found for {selected_city} with current filters")

with tab2:
    st.header("💬 AI-Powered Query Assistant")
    
    # Example queries with city context
    if selected_city != "All Cities":
        examples = [
            "Custom query...",
            f"What are the critical situations in {selected_city}?",
            f"Show me flood events in {selected_city}",
            f"What kind of help is needed in {selected_city}?",
            f"Latest updates from {selected_city}"
        ]
    else:
        examples = [
            "Custom query...",
            "What are the most critical situations?",
            "Show me earthquake events",
            "Where are floods happening?",
            "Which cities need immediate help?"
        ]
    
    selected_example = st.selectbox("💡 Try example queries:", examples)
    
    query = st.text_area(
        "🔍 Ask about the disaster situation:",
        value="" if selected_example == "Custom query..." else selected_example,
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if search_btn and query:
        with st.spinner("🤖 AI analyzing disaster data..."):
            try:
                response = httpx.post(
                    f"{API_BASE}/query",
                    json={"question": query},
                    timeout=10
                ).json()
                
                # Display answer
                st.markdown("### 📝 AI Response")
                st.info(response['answer'])
                
                # Confidence meter
                confidence = response['confidence']
                st.markdown("### 🎯 Confidence Score")
                st.progress(confidence)
                st.caption(f"Confidence: {confidence*100:.1f}% | Based on {len(response.get('sources', []))} sources")
                
                # Sources
                if response.get('relevant_events'):
                    st.markdown("### 📚 Source Events")
                    for i, event in enumerate(response['relevant_events'][:5], 1):
                        with st.expander(f"📍 Source {i}: {event['type']} in {event['location']} - {event['severity']}"):
                            st.markdown(f"**Text:** {event['text']}")
                            st.caption(f"Location: {event['location']} | ID: {event['id']}")
            except Exception as e:
                st.error(f"❌ Query failed: {e}")

with tab3:
    st.header("🤖 AI Agent Decisions & Resource Allocation")
    
    decisions = api_call("/agent/decisions")
    if decisions:
        st.info(f"🎯 Showing top {len(decisions)} priority decisions")
        
        for i, decision in enumerate(decisions, 1):
            # Priority score visualization
            priority = decision.get('priority_score', 0)
            color = '#ff4444' if priority >= 90 else '#ff8800' if priority >= 70 else '#ffbb00'
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style='background: {color}; color: white; padding: 1rem; border-radius: 8px;'>
                        <h4>Decision #{i} - Priority: {priority}/100</h4>
                        <p><strong>Event:</strong> {decision.get('event_text', '')[:120]}...</p>
                        <p><strong>Recommended Action:</strong> {decision.get('recommended_action', '')}</p>
                        <p><strong>AI Reasoning:</strong> {decision.get('reasoning', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("Resources", len(decision.get('assigned_resources', [])))
                    for res in decision.get('assigned_resources', []):
                        st.caption(f"✅ {res}")
                
                with col3:
                    st.metric("Priority", f"{priority}%")
                    st.caption(f"Event: {decision.get('event_id', 'N/A')}")
                
                st.markdown("---")
    else:
        st.info("No agent decisions available. System is monitoring for critical events.")

with tab4:
    st.header("📋 Automated Situation Report")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button("📄 Generate Report", type="primary", use_container_width=True)
    with col2:
        st.caption("Generate comprehensive situation report for emergency response teams")
    
    if generate_btn:
        with st.spinner("🤖 AI generating comprehensive report..."):
            try:
                report = api_call("/report")
                if report:
                    st.markdown(report)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Report (Markdown)",
                        data=report,
                        file_name=f"crisis_report_{selected_city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                    st.success("✅ Report generated successfully!")
            except Exception as e:
                st.error(f"❌ Report generation failed: {e}")

with tab5:
    st.header("📊 Analytics & Event Feed")
    
    if len(df_filtered) > 0:
        # Analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Severity Trend")
            severity_counts = df_filtered['severity'].value_counts()
            fig = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                color=severity_counts.index,
                color_discrete_map={
                    'CRITICAL': '#ff4444',
                    'HIGH': '#ff8800',
                    'MEDIUM': '#ffbb00',
                    'LOW': '#00cc66'
                },
                labels={'x': 'Severity', 'y': 'Count'}
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🌍 Location Distribution")
            location_counts = df_filtered['location'].value_counts().head(10)
            fig = px.bar(
                x=location_counts.values,
                y=location_counts.index,
                orientation='h',
                color=location_counts.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Event feed
        st.markdown("### 📋 Live Event Feed")
        
        # Display as cards
        for _, event in df_filtered.head(20).iterrows():
            color = {'CRITICAL': '#ff4444', 'HIGH': '#ff8800', 'MEDIUM': '#ffbb00', 'LOW': '#00cc66'}
            
            st.markdown(f"""
            <div style='background: {color.get(event['severity'], '#cccccc')}; color: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;'>
                <div style='display: flex; justify-content: space-between;'>
                    <strong>{event['type']}</strong>
                    <span>{event['location']}</span>
                </div>
                <p style='margin: 0.5rem 0;'>{event['text']}</p>
                <small>Severity: {event['severity']} | ID: {event['id']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.caption(f"Showing {min(20, len(df_filtered))} of {len(df_filtered)} events")
    else:
        st.warning("No events to display with current filters")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🚨 CrisisLens AI** | Disaster Intelligence Platform")
with col2:
    st.markdown("Built for **GenAIVersity Hackathon 2025**")
with col3:
    st.markdown("Powered by **HuggingFace** & **ChromaDB**")

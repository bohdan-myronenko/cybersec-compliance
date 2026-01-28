"""
Cybersecurity Compliance Web UI
A Streamlit-based interface for the compliance monitoring system.
"""

import os
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration
API_URL = os.getenv("API_URL", "http://api:8080")
OUT_DIR = Path(os.getenv("OUT_DIR", "/out"))
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Compliance Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .status-ok {
        color: #00ff00;
        font-weight: bold;
    }
    .status-error {
        color: #ff4444;
        font-weight: bold;
    }
    .report-card {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def check_service_health(url: str, name: str) -> dict:
    """Check if a service is healthy."""
    try:
        resp = requests.get(f"{url}/health", timeout=5)
        if resp.status_code == 200:
            return {"name": name, "status": "ok", "detail": resp.json()}
        return {"name": name, "status": "error", "detail": f"HTTP {resp.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"name": name, "status": "error", "detail": str(e)}


def get_report_files() -> list:
    """Get list of generated report files."""
    if not OUT_DIR.exists():
        return []
    reports = []
    for f in sorted(OUT_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
        stat = f.stat()
        reports.append({
            "name": f.name,
            "path": str(f),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime),
        })
    return reports


def get_data_files() -> list:
    """Get list of data files available for processing."""
    if not DATA_DIR.exists():
        return []
    files = []
    for f in DATA_DIR.rglob("*"):
        if f.is_file():
            stat = f.stat()
            files.append({
                "name": f.name,
                "path": str(f.relative_to(DATA_DIR)),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime),
            })
    return sorted(files, key=lambda x: x["modified"], reverse=True)


def trigger_report_generation() -> dict:
    """Trigger the access control report generation."""
    try:
        resp = requests.post(
            f"{API_URL}/generate/access-control",
            json={},
            timeout=3600,
        )
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": "connection_error", "detail": str(e)}


def get_generation_progress() -> dict:
    """Get the current progress of report generation."""
    try:
        resp = requests.get(f"{API_URL}/generate/progress", timeout=5)
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


# Stage icons for visual feedback
STAGE_ICONS = {
    "init": "🚀",
    "scan": "🔍",
    "normalize": "📋",
    "metrics": "📊",
    "legal": "📚",
    "llm": "🤖",
    "render": "📝",
    "save": "💾",
    "complete": "✅",
}


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/security-checked.png", width=80)
        st.title("Navigation")
        
        page = st.radio(
            "Select Page",
            ["Dashboard", "Generate Reports", "View Reports", "Data Files", "Settings"],
            label_visibility="collapsed",
        )
        
        st.divider()
        
        # Service status indicators
        st.subheader("Service Status")
        api_health = check_service_health(API_URL, "API")
        
        if api_health["status"] == "ok":
            st.success("API: Online")
        else:
            st.error("API: Offline")
        
        return page


def render_dashboard():
    """Render the main dashboard page."""
    st.title("🔐 Cybersecurity Compliance Dashboard")
    st.markdown("Monitor your organization's security compliance status at a glance.")
    
    # Service Health Section
    st.header("System Health")
    col1, col2, col3 = st.columns(3)
    
    api_health = check_service_health(API_URL, "API Gateway")
    
    with col1:
        if api_health["status"] == "ok":
            st.metric("API Gateway", "Online", delta="Healthy")
        else:
            st.metric("API Gateway", "Offline", delta="Error", delta_color="inverse")
    
    with col2:
        reports = get_report_files()
        st.metric("Generated Reports", len(reports))
    
    with col3:
        data_files = get_data_files()
        st.metric("Data Files", len(data_files))
    
    st.divider()
    
    # Recent Reports Section
    st.header("Recent Reports")
    reports = get_report_files()
    
    if reports:
        for report in reports[:5]:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{report['name']}**")
                with col2:
                    st.caption(f"Size: {report['size'] / 1024:.1f} KB")
                with col3:
                    st.caption(report['modified'].strftime("%Y-%m-%d %H:%M"))
    else:
        st.info("No reports generated yet. Go to 'Generate Reports' to create your first report.")
    
    st.divider()
    
    # Quick Actions
    st.header("Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Generate New Report", use_container_width=True):
            st.switch_page_workaround = "Generate Reports"
            st.rerun()
    
    with col2:
        if st.button("📊 View Latest Report", use_container_width=True):
            if reports:
                st.session_state["selected_report"] = reports[0]["path"]
                st.switch_page_workaround = "View Reports"
                st.rerun()


def render_generate_reports():
    """Render the report generation page."""
    st.title("📝 Generate Compliance Reports")
    st.markdown("Analyze log data and generate access control compliance reports.")
    
    # Data Files Summary
    st.header("Available Data Files")
    data_files = get_data_files()
    
    if data_files:
        df = pd.DataFrame(data_files)
        df["size_kb"] = df["size"] / 1024
        df["modified"] = pd.to_datetime(df["modified"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Files", len(data_files))
        with col2:
            total_size = sum(f["size"] for f in data_files)
            st.metric("Total Size", f"{total_size / (1024*1024):.2f} MB")
        
        st.dataframe(
            df[["name", "path", "size_kb", "modified"]].rename(columns={
                "name": "File Name",
                "path": "Path",
                "size_kb": "Size (KB)",
                "modified": "Modified",
            }),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No data files found in the data directory. Please add log files to process.")
    
    st.divider()
    
    # Generation Controls
    st.header("Generate Report")
    
    st.info("""
    **What happens when you generate a report:**
    1. All log files in the data directory are processed
    2. Events are grouped by time windows (default: 7 days)
    3. Metrics are computed for each window (auth failures, attack IPs, etc.)
    4. An LLM generates compliance observations based on the metrics
    5. Final reports are rendered and saved to the output directory
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Generate Access Control Report", type="primary", use_container_width=True):
            # Create placeholders for progress UI
            progress_container = st.container()
            
            with progress_container:
                status_placeholder = st.empty()
                progress_bar = st.progress(0)
                stage_placeholder = st.empty()
                detail_placeholder = st.empty()
                
                # Use ThreadPoolExecutor for async execution
                with ThreadPoolExecutor(max_workers=1) as executor:
                    # Start the generation in a background thread
                    future = executor.submit(trigger_report_generation)
                    
                    # Poll for progress while waiting
                    last_stage = ""
                    while not future.done():
                        progress_data = get_generation_progress()
                        
                        if progress_data.get("status") == "running":
                            prog = progress_data.get("progress", {})
                            stage = prog.get("stage", "init")
                            stage_num = prog.get("stage_number", 1)
                            total_stages = prog.get("total_stages", 9)
                            message = prog.get("message", "Processing...")
                            detail = prog.get("detail", "")
                            
                            # Update progress bar
                            progress_pct = min(stage_num / total_stages, 0.99)
                            progress_bar.progress(progress_pct)
                            
                            # Update stage display
                            icon = STAGE_ICONS.get(stage, "⏳")
                            status_placeholder.markdown(f"### {icon} {message}")
                            
                            if detail:
                                detail_placeholder.caption(f"_{detail}_")
                            
                            # Show stage progression
                            if stage != last_stage:
                                last_stage = stage
                                stages_display = []
                                for s_key, s_msg in [
                                    ("init", "Initialize"),
                                    ("scan", "Scan Files"),
                                    ("normalize", "Parse Logs"),
                                    ("metrics", "Compute Metrics"),
                                    ("legal", "Load Legal Texts"),
                                    ("llm", "Query LLM"),
                                    ("render", "Render Report"),
                                    ("save", "Save Output"),
                                ]:
                                    s_icon = STAGE_ICONS.get(s_key, "⏳")
                                    s_num, _ = next(((i+1, m) for i, (k, m) in enumerate([
                                        ("init", ""), ("scan", ""), ("normalize", ""),
                                        ("metrics", ""), ("legal", ""), ("llm", ""),
                                        ("render", ""), ("save", ""), ("complete", "")
                                    ]) if k == s_key), (0, ""))
                                    
                                    if s_num < stage_num:
                                        stages_display.append(f"~~{s_icon} {s_msg}~~")
                                    elif s_num == stage_num:
                                        stages_display.append(f"**{s_icon} {s_msg}** ←")
                                    else:
                                        stages_display.append(f"{s_icon} {s_msg}")
                                
                                stage_placeholder.markdown(" → ".join(stages_display[:4]) + "\n\n" + " → ".join(stages_display[4:]))
                        
                        time.sleep(0.5)
                    
                    # Get the result
                    result = future.result()
                
                # Clear progress displays
                progress_bar.progress(1.0)
                
                if "error" in result:
                    status_placeholder.error(f"❌ Error: {result.get('error')}")
                    detail_placeholder.empty()
                    stage_placeholder.empty()
                    if "detail" in result:
                        st.code(result["detail"])
                    if "traceback" in result:
                        with st.expander("Full Traceback"):
                            st.code(result["traceback"])
                else:
                    status_placeholder.success("✅ Report generated successfully!")
                    detail_placeholder.empty()
                    stage_placeholder.empty()
                    if "windows" in result:
                        st.write(f"Generated {len(result['windows'])} report(s):")
                        for window in result["windows"]:
                            st.write(f"- Window: {window['window']} → {window['output']}")
                    st.balloons()


def render_view_reports():
    """Render the reports viewer page."""
    st.title("📊 View Reports")
    
    reports = get_report_files()
    
    if not reports:
        st.info("No reports available. Generate a report first.")
        return
    
    # Report Selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_report = st.selectbox(
            "Select Report",
            options=[r["path"] for r in reports],
            format_func=lambda x: Path(x).name,
        )
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    if selected_report:
        report_path = Path(selected_report)
        
        # Report metadata
        if report_path.exists():
            stat = report_path.stat()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Size", f"{stat.st_size / 1024:.1f} KB")
            with col2:
                modified = datetime.fromtimestamp(stat.st_mtime)
                st.metric("Generated", modified.strftime("%Y-%m-%d %H:%M"))
            with col3:
                if st.download_button(
                    "📥 Download",
                    data=report_path.read_text(encoding="utf-8"),
                    file_name=report_path.name,
                    mime="text/markdown",
                    use_container_width=True,
                ):
                    pass
            
            st.divider()
            
            # Display report content
            content = report_path.read_text(encoding="utf-8")
            
            tab1, tab2 = st.tabs(["📄 Rendered", "📝 Raw Markdown"])
            
            with tab1:
                st.markdown(content)
            
            with tab2:
                st.code(content, language="markdown")


def render_data_files():
    """Render the data files management page."""
    st.title("📁 Data Files")
    st.markdown("View and manage log files available for analysis.")
    
    data_files = get_data_files()
    
    if not data_files:
        st.warning("No data files found.")
        st.info(f"Add log files to: `{DATA_DIR}`")
        return
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    total_size = sum(f["size"] for f in data_files)
    
    with col1:
        st.metric("Total Files", len(data_files))
    with col2:
        st.metric("Total Size", f"{total_size / (1024*1024):.2f} MB")
    with col3:
        if data_files:
            newest = max(f["modified"] for f in data_files)
            st.metric("Latest File", newest.strftime("%Y-%m-%d"))
    
    st.divider()
    
    # File type distribution
    st.subheader("File Types")
    extensions = {}
    for f in data_files:
        ext = Path(f["name"]).suffix.lower() or "no extension"
        extensions[ext] = extensions.get(ext, 0) + 1
    
    if extensions:
        fig = px.pie(
            values=list(extensions.values()),
            names=list(extensions.keys()),
            title="Distribution by File Type",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # File listing
    st.subheader("All Files")
    df = pd.DataFrame(data_files)
    df["size_kb"] = df["size"] / 1024
    df["modified"] = pd.to_datetime(df["modified"])
    
    st.dataframe(
        df[["name", "path", "size_kb", "modified"]].rename(columns={
            "name": "File Name",
            "path": "Relative Path",
            "size_kb": "Size (KB)",
            "modified": "Last Modified",
        }),
        use_container_width=True,
        hide_index=True,
    )


def render_settings():
    """Render the settings page."""
    st.title("⚙️ Settings")
    
    st.header("Service Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("API Service")
        st.text_input("API URL", value=API_URL, disabled=True)
        api_health = check_service_health(API_URL, "API")
        if api_health["status"] == "ok":
            st.success("Connected")
        else:
            st.error(f"Error: {api_health['detail']}")
    
    with col2:
        st.subheader("Directories")
        st.text_input("Output Directory", value=str(OUT_DIR), disabled=True)
        st.text_input("Data Directory", value=str(DATA_DIR), disabled=True)
    
    st.divider()
    
    st.header("Environment Variables")
    st.info("These settings are configured via environment variables in the Docker container.")
    
    env_vars = {
        "API_URL": os.getenv("API_URL", "http://api:8080"),
        "OUT_DIR": os.getenv("OUT_DIR", "/out"),
        "DATA_DIR": os.getenv("DATA_DIR", "/data"),
    }
    
    for key, value in env_vars.items():
        st.text(f"{key}: {value}")
    
    st.divider()
    
    st.header("About")
    st.markdown("""
    **Cybersecurity Compliance Dashboard**
    
    A web-based interface for monitoring and generating security compliance reports.
    
    **Features:**
    - Real-time service health monitoring
    - Access control compliance report generation
    - Report viewing and download
    - Data file management
    
    **Architecture:**
    - **API Gateway**: FastAPI service handling external requests
    - **Worker**: Background service processing logs and generating reports
    - **Ollama**: LLM service for generating compliance observations
    - **Web UI**: This Streamlit dashboard
    """)


def main():
    """Main application entry point."""
    page = render_sidebar()
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "Generate Reports":
        render_generate_reports()
    elif page == "View Reports":
        render_view_reports()
    elif page == "Data Files":
        render_data_files()
    elif page == "Settings":
        render_settings()


if __name__ == "__main__":
    main()

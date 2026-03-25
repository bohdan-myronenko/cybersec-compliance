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


def trigger_report_generation(filename: str | None = None) -> dict:
    """Trigger the access control report generation. If filename is provided, only that file is processed."""
    try:
        payload = {}
        if filename:
            payload["filename"] = filename
        resp = requests.post(
            f"{API_URL}/generate/access-control",
            json=payload,
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


def get_checkpoint_info() -> dict:
    """Get checkpoint info from the API."""
    try:
        resp = requests.get(f"{API_URL}/generate/checkpoint", timeout=5)
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


def api_clear_checkpoint() -> dict:
    """Clear the pipeline checkpoint via the API."""
    try:
        resp = requests.delete(f"{API_URL}/generate/checkpoint", timeout=5)
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}


# Stage icons for visual feedback
STAGE_ICONS = {
    "init": "🚀",
    "scan": "🔍",
    "normalize": "📋",
    "metrics": "📊",
    "legal": "📚",
    "llm": "🤖",
    "insights": "💡",
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
            ["Dashboard", "Chat", "Format Onboarding", "Generate Reports", "View Reports", "Data Files", "Settings"],
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
        
        # Agent system status
        try:
            agent_resp = requests.get(f"{API_URL}/agent/health", timeout=5)
            if agent_resp.status_code == 200:
                agent_health = agent_resp.json()
                if agent_health.get("status") == "healthy":
                    st.success("Agent System: Online")
                else:
                    st.warning("Agent System: Degraded")
            else:
                st.warning("Agent System: Unknown")
        except:
            st.warning("Agent System: Unknown")
        
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
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files", len(data_files))
        with col2:
            total_size = sum(f["size"] for f in data_files)
            st.metric("Total Size", f"{total_size / (1024*1024):.2f} MB")
        with col3:
            if st.button("🔍 Check Format Status", use_container_width=True):
                st.session_state["check_formats"] = True
                st.rerun()
        
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
        
        # Check format status if requested
        if st.session_state.get("check_formats"):
            st.subheader("Format Status Check")
            with st.spinner("Scanning files for format compatibility..."):
                try:
                    scan_resp = requests.get(f"{API_URL}/agent/scan-data-formats", timeout=60)
                    if scan_resp.status_code == 200:
                        scan_data = scan_resp.json()
                        summary = scan_data.get("summary", {})
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Matched", summary.get("matched", 0), delta="OK" if summary.get("matched", 0) > 0 else None)
                        with col2:
                            unmatched = summary.get("unmatched", 0)
                            st.metric("Unmatched", unmatched, delta="Warning" if unmatched > 0 else None, delta_color="inverse" if unmatched > 0 else "normal")
                        with col3:
                            st.metric("Unknown", summary.get("unknown", 0))
                        
                        # Show warning for unmatched files
                        unmatched_files = scan_data.get("unmatched_files", [])
                        if unmatched_files:
                            st.error(f"""
                            🛑 **{len(unmatched_files)} file(s) have unrecognized formats!**
                            
                            These files may not be processed correctly. Consider onboarding their formats first.
                            """)
                            
                            with st.expander(f"View unmatched files ({len(unmatched_files)})"):
                                for uf in unmatched_files:
                                    closest = uf.get("closest_match")
                                    if closest:
                                        st.markdown(f"- **{uf['file']}**: Closest match: {closest['format_name']} ({closest['similarity']:.0%})")
                                    else:
                                        st.markdown(f"- **{uf['file']}**: No similar format found")
                            
                            st.warning("👉 Go to **Format Onboarding** to add support for these formats.")
                        else:
                            st.success("✅ All files match known formats!")
                        
                        # Show matched files
                        matched_files = scan_data.get("matched_files", [])
                        if matched_files:
                            with st.expander(f"View matched files ({len(matched_files)})"):
                                for mf in matched_files:
                                    fmt = mf.get("matched_format", mf.get("builtin_format", "unknown"))
                                    st.markdown(f"- **{mf['file']}**: {fmt}")
                    else:
                        st.warning("Could not check format status")
                except Exception as e:
                    st.warning(f"Could not check format status: {e}")
            
            if st.button("Hide Format Check"):
                st.session_state["check_formats"] = False
                st.rerun()
    else:
        st.warning("No data files found in the data directory. Please add log files to process.")
    
    st.divider()
    
    # Generation Controls
    st.header("Generate Report")
    
    # Checkpoint UI
    ckpt = get_checkpoint_info()
    has_checkpoint = ckpt.get("status") == "exists"
    
    if has_checkpoint:
        last_stage = ckpt.get("last_stage", "unknown")
        updated_at = ckpt.get("updated_at", "")
        completed = ckpt.get("completed_stages", [])
        st.warning(
            f"📌 **Checkpoint found** — Last completed stage: **{last_stage}** "
            f"({len(completed)} stage(s) done) — Saved at: {updated_at}"
        )
        col_resume, col_clear = st.columns(2)
        with col_resume:
            resume_clicked = st.button("▶️ Resume from Checkpoint", type="primary", use_container_width=True)
        with col_clear:
            if st.button("🗑️ Clear Checkpoint", use_container_width=True):
                api_clear_checkpoint()
                st.rerun()
    else:
        resume_clicked = False
    
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
        generate_clicked = st.button("🚀 Generate Access Control Report", type="primary", use_container_width=True)
    
    if generate_clicked or resume_clicked:
            # Create placeholders for progress UI
            progress_container = st.container()
            
            with progress_container:
                status_placeholder = st.empty()
                progress_bar = st.progress(0)
                table_placeholder = st.empty()
                detail_placeholder = st.empty()
                
                # Use ThreadPoolExecutor for async execution
                with ThreadPoolExecutor(max_workers=1) as executor:
                    # Start the generation in a background thread
                    future = executor.submit(trigger_report_generation)
                    
                    # Stage display names
                    STAGE_DISPLAY = [
                        ("init", "Initialize"),
                        ("scan", "Scan Files"),
                        ("normalize", "Parse Logs"),
                        ("metrics", "Compute Metrics"),
                        ("legal", "Load Legal Texts"),
                        ("llm", "Query LLM"),
                        ("insights", "Generate Insights"),
                        ("render", "Render Report"),
                        ("save", "Save Output"),
                        ("complete", "Complete"),
                    ]
                    
                    # Poll for progress while waiting
                    while not future.done():
                        progress_data = get_generation_progress()
                        
                        if progress_data.get("status") == "running":
                            prog = progress_data.get("progress", {})
                            stage = prog.get("stage", "init")
                            stage_num = prog.get("stage_number", 1)
                            total_stages = prog.get("total_stages", 9)
                            message = prog.get("message", "Processing...")
                            detail = prog.get("detail", "")
                            stages_status = prog.get("stages_status", {})
                            
                            # Update progress bar
                            progress_pct = min(stage_num / total_stages, 0.99)
                            progress_bar.progress(progress_pct)
                            
                            # Update heading
                            icon = STAGE_ICONS.get(stage, "⏳")
                            status_placeholder.markdown(f"### {icon} {message}")
                            
                            if detail:
                                detail_placeholder.caption(f"_{detail}_")
                            
                            # Build progress table
                            table_rows = []
                            for s_key, s_name in STAGE_DISPLAY:
                                s_icon = STAGE_ICONS.get(s_key, "⏳")
                                s_status = stages_status.get(s_key, "Pending")
                                table_rows.append({
                                    "Stage": f"{s_icon} {s_name}",
                                    "Status": s_status,
                                })
                            table_placeholder.table(pd.DataFrame(table_rows))
                        
                        time.sleep(0.5)
                    
                    # Get the result
                    result = future.result()
                
                # Clear progress displays
                progress_bar.progress(1.0)
                
                if "error" in result:
                    status_placeholder.error(f"❌ Error: {result.get('error')}")
                    detail_placeholder.empty()
                    table_placeholder.empty()
                    if "detail" in result:
                        st.code(result["detail"])
                    if "traceback" in result:
                        with st.expander("Full Traceback"):
                            st.code(result["traceback"])
                else:
                    status_placeholder.success("✅ Report generated successfully!")
                    detail_placeholder.empty()
                    table_placeholder.empty()
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
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    
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
            col1, col2, col3 = st.columns([3, 3, 2], vertical_alignment="bottom")
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


def render_format_onboarding():
    """Render the format onboarding page for agent-assisted log format configuration."""
    st.title("🔧 Format Onboarding")
    st.markdown("Use AI to analyze new log formats and configure field mappings.")
    
    # Initialize session state
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "suggested_metrics" not in st.session_state:
        st.session_state.suggested_metrics = None
    if "step" not in st.session_state:
        st.session_state.step = 1
    
    # Show existing formats
    st.header("Registered Formats")
    if "format_preview_id" not in st.session_state:
        st.session_state.format_preview_id = None
    try:
        formats_resp = requests.get(f"{API_URL}/agent/formats", timeout=10)
        if formats_resp.status_code == 200:
            formats_data = formats_resp.json()
            formats_list = formats_data.get("formats", [])
            if formats_list:
                for fmt in formats_list:
                    fmt_id = fmt.get("format_id", "")
                    fmt_name = fmt.get("format_name", "Unknown")
                    fmt_type = fmt.get("format_type", "")
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.text(f"{fmt_name} ({fmt_id})")
                    with col2:
                        st.caption(fmt_type)
                    with col3:
                        if st.button("Preview", key=f"preview_{fmt_id}", type="secondary"):
                            st.session_state.format_preview_id = fmt_id
                            st.rerun()
                if st.session_state.format_preview_id:
                    preview_id = st.session_state.format_preview_id
                    if st.button("Close preview", key="close_preview"):
                        st.session_state.format_preview_id = None
                        st.rerun()
                    try:
                        detail_resp = requests.get(f"{API_URL}/agent/formats/{preview_id}", timeout=10)
                        if detail_resp.status_code == 200:
                            config = detail_resp.json()
                            st.subheader(f"Format: {config.get('format_name', preview_id)}")
                            st.caption(f"Type: {config.get('format_type', '')} | Approved by: {config.get('_approved_by', '')} at {config.get('_approved_at', '')}")
                            field_mappings = config.get("field_mappings") or {}
                            if field_mappings:
                                st.markdown("**Field Mappings**")
                                st.dataframe(
                                    pd.DataFrame([{"source": k, "ECS field": v} for k, v in field_mappings.items()]),
                                    use_container_width=True,
                                    hide_index=True,
                                )
                            detection_rules = config.get("detection_rules") or {}
                            if detection_rules:
                                st.markdown("**Detection Rules**")
                                st.json(detection_rules)
                            unmapped = config.get("unmapped_fields") or []
                            if unmapped:
                                st.markdown("**Unmapped Fields**")
                                rows = []
                                for field in unmapped:
                                    if isinstance(field, dict):
                                        rows.append(
                                            {
                                                "name": field.get("name", ""),
                                                "sample_value": field.get("sample_value", ""),
                                                "potential_use": field.get("potential_use", ""),
                                            }
                                        )
                                    else:
                                        rows.append(
                                            {
                                                "name": str(field),
                                                "sample_value": "",
                                                "potential_use": "",
                                            }
                                        )
                                if rows:
                                    st.dataframe(
                                        pd.DataFrame(rows),
                                        use_container_width=True,
                                        hide_index=True,
                                    )
                        else:
                            st.warning("Could not load format details.")
                    except Exception as e:
                        st.warning(f"Error loading format: {e}")
            else:
                st.info("No custom formats registered yet.")
        else:
            st.warning("Could not load registered formats.")
    except Exception as e:
        st.warning(f"Could not connect to agent service: {e}")
    
    st.divider()
    
    # Step 1: Upload/Paste Samples
    st.header("Step 1: Provide Log Samples")
    st.markdown("Upload a log file or paste sample log lines for analysis.")
    
    input_method = st.radio(
        "Input Method",
        ["Upload File", "Paste Text"],
        horizontal=True,
    )
    
    samples = []
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload a log file (first 50 lines will be used)",
            type=["log", "txt", "csv", "json", "jsonl"],
        )
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            samples = content.strip().split("\n")[:50]
            st.success(f"Loaded {len(samples)} lines from file")
            with st.expander("Preview (first 10 lines)"):
                for i, line in enumerate(samples[:10], 1):
                    st.code(f"{i}: {line[:200]}{'...' if len(line) > 200 else ''}")
    else:
        sample_text = st.text_area(
            "Paste log samples (one per line)",
            height=200,
            placeholder="Paste your log samples here...\nEach line should be a separate log entry.",
        )
        if sample_text:
            samples = [l for l in sample_text.strip().split("\n") if l.strip()][:50]
            st.info(f"{len(samples)} sample lines ready for analysis")
    
    # Quick analyze button
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Quick Detect Format", disabled=len(samples) == 0):
            with st.spinner("Detecting format..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/agent/quick-analyze",
                        json={"samples": samples},
                        timeout=30,
                    )
                    if resp.status_code == 200:
                        result = resp.json()
                        fmt_type = result.get("format_type", "unknown")
                        confidence = result.get("confidence", 0)
                        custom_match = result.get("custom_format_match")
                        has_onboarded = result.get("has_onboarded_match", False)
                        recommendation = result.get("recommendation", "")
                        
                        # Show heuristic detection
                        st.info(f"**Heuristic detection:** {fmt_type} (confidence: {confidence:.0%})")
                        
                        # Show custom format match status
                        if custom_match:
                            similarity = custom_match.get("similarity", 0)
                            match_name = custom_match.get("format_name", custom_match.get("format_id", "Unknown"))
                            
                            if similarity >= 0.8:
                                st.success(f"✅ **Exact match found!** This format is already onboarded as: **{match_name}** ({similarity:.0%} match)")
                            elif similarity >= 0.5:
                                st.warning(f"⚠️ **Partial match found:** {match_name} ({similarity:.0%} match). You may want to update the existing format or create a new one.")
                            else:
                                st.info(f"📋 **Closest onboarded format:** {match_name} ({similarity:.0%} match)")
                        
                        if not has_onboarded:
                            st.error("""
                            🛑 **Format not onboarded!**
                            
                            This log format has not been added to the system yet. 
                            Click "Full AI Analysis" below to analyze and onboard this format.
                            """)
                        
                        if recommendation:
                            st.caption(f"💡 {recommendation}")
                    else:
                        st.error("Quick detection failed")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        if st.button("🤖 Full AI Analysis", type="primary", disabled=len(samples) == 0):
            with st.spinner("Analyzing with AI (this may take a minute)..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/agent/analyze-format",
                        json={"samples": samples, "max_samples": 20},
                        timeout=180,
                    )
                    if resp.status_code == 200:
                        st.session_state.analysis_result = resp.json()
                        st.session_state.step = 2
                        st.success("Analysis complete!")
                        st.rerun()
                    else:
                        st.error(f"Analysis failed: {resp.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Step 2: Review Mappings
    if st.session_state.analysis_result and st.session_state.step >= 2:
        st.divider()
        st.header("Step 2: Review Field Mappings")
        
        result = st.session_state.analysis_result
        
        if "error" in result:
            st.error(f"Analysis error: {result['error']}")
        else:
            # Show confidence and reasoning
            col1, col2 = st.columns(2)
            with col1:
                confidence = result.get("confidence", 0)
                st.metric("AI Confidence", f"{confidence:.0%}")
            with col2:
                format_type = result.get("format_type", "unknown")
                st.metric("Detected Type", format_type)
            
            if result.get("reasoning"):
                with st.expander("AI Reasoning"):
                    st.markdown(result["reasoning"])
            
            # Editable format name
            format_name = st.text_input(
                "Format Name",
                value=result.get("format_name", "Custom Format"),
                help="A descriptive name for this log format",
            )
            
            format_id = st.text_input(
                "Format ID",
                value=format_name.lower().replace(" ", "_").replace("-", "_"),
                help="Unique identifier (lowercase, no spaces)",
            )
            
            # Field mappings table
            st.subheader("Field Mappings")
            st.markdown("Review and adjust the proposed mappings from source fields to ECS fields.")
            
            mappings = result.get("field_mappings", {})
            ecs_options = ["@ts", "user", "src_ip", "dst_ip", "action", "status", "resource", "msg", "(unmapped)"]
            
            edited_mappings = {}
            for source_field, ecs_field in mappings.items():
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.text_input(f"Source", value=source_field, disabled=True, key=f"src_{source_field}")
                with col2:
                    default_idx = ecs_options.index(ecs_field) if ecs_field in ecs_options else len(ecs_options) - 1
                    selected = st.selectbox(
                        f"Maps to",
                        options=ecs_options,
                        index=default_idx,
                        key=f"ecs_{source_field}",
                    )
                    if selected != "(unmapped)":
                        edited_mappings[source_field] = selected
            
            # Unmapped fields info
            unmapped = result.get("unmapped_fields", [])
            if unmapped:
                with st.expander(f"Unmapped Fields ({len(unmapped)})"):
                    for field in unmapped:
                        name = field.get("name", "unknown")
                        sample = field.get("sample_value", "N/A")
                        use = field.get("potential_use", "")
                        st.markdown(f"- **{name}**: `{sample}` - _{use}_")
            
            # Detection rules
            with st.expander("Detection Rules"):
                detection = result.get("detection_rules", {})
                st.json(detection)
            
            # Approve button
            if st.button("✅ Approve Mappings & Continue", type="primary"):
                with st.spinner("Saving configuration..."):
                    try:
                        approve_resp = requests.post(
                            f"{API_URL}/agent/approve-format",
                            json={
                                "format_id": format_id,
                                "format_name": format_name,
                                "format_type": result.get("format_type", "custom"),
                                "detection_rules": result.get("detection_rules", {}),
                                "field_mappings": edited_mappings,
                                "unmapped_fields": unmapped,
                                "approved_by": "webui_user",
                            },
                            timeout=30,
                        )
                        if approve_resp.status_code == 200:
                            st.session_state.step = 3
                            st.session_state.approved_format_id = format_id
                            st.session_state.available_fields = list(edited_mappings.values())
                            st.success("Configuration saved!")
                            st.rerun()
                        else:
                            st.error(f"Failed to save: {approve_resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    # Step 3: Metric Suggestions
    if st.session_state.step >= 3:
        st.divider()
        st.header("Step 3: Configure Metrics")
        
        format_id = st.session_state.get("approved_format_id", "")
        available_fields = st.session_state.get("available_fields", [])
        unmapped_fields = st.session_state.analysis_result.get("unmapped_fields", []) if st.session_state.analysis_result else []
        
        st.info(f"Format: **{format_id}** | Available ECS fields: {', '.join(available_fields)}")
        
        # Get metric suggestions
        if st.session_state.suggested_metrics is None:
            if st.button("🤖 Get Metric Suggestions"):
                with st.spinner("Getting AI suggestions for metrics..."):
                    try:
                        resp = requests.post(
                            f"{API_URL}/agent/suggest-metrics",
                            json={
                                "format_id": format_id,
                                "available_fields": available_fields,
                                "unmapped_fields": unmapped_fields,
                                "sample_stats": {},
                            },
                            timeout=180,
                        )
                        if resp.status_code == 200:
                            st.session_state.suggested_metrics = resp.json().get("metrics", [])
                            st.rerun()
                        else:
                            st.error(f"Failed: {resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        if st.session_state.suggested_metrics:
            st.subheader("Suggested Metrics")
            st.markdown("Select which metrics to enable for this format.")
            
            metrics = st.session_state.suggested_metrics
            selected_metrics = []
            
            for metric in metrics:
                metric_id = metric.get("metric_id", "unknown")
                name = metric.get("name", metric_id)
                desc = metric.get("description", "")
                priority = metric.get("priority", "medium")
                compliance = metric.get("compliance_relevance", [])
                
                priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                priority_icon = priority_colors.get(priority, "⚪")
                
                enabled = st.checkbox(
                    f"{priority_icon} **{name}**",
                    value=metric.get("enabled", True),
                    key=f"metric_{metric_id}",
                    help=f"{desc}\nCompliance: {', '.join(compliance) if compliance else 'N/A'}",
                )
                
                if enabled:
                    metric_copy = dict(metric)
                    metric_copy["enabled"] = True
                    selected_metrics.append(metric_copy)
                
                with st.expander(f"Details: {name}"):
                    st.markdown(f"**Description:** {desc}")
                    st.markdown(f"**Priority:** {priority}")
                    st.markdown(f"**Required Fields:** {', '.join(metric.get('required_fields', []))}")
                    if compliance:
                        st.markdown(f"**Compliance:** {', '.join(compliance)}")
                    if metric.get("computation"):
                        st.json(metric["computation"])
            
            # Save metrics
            if st.button("💾 Save Metric Configuration", type="primary"):
                with st.spinner("Saving metrics..."):
                    try:
                        resp = requests.post(
                            f"{API_URL}/agent/save-metrics",
                            json={
                                "format_id": format_id,
                                "metrics": selected_metrics,
                            },
                            timeout=30,
                        )
                        if resp.status_code == 200:
                            st.success("Metrics saved successfully!")
                            st.balloons()
                            # Reset for new format
                            if st.button("➕ Onboard Another Format"):
                                st.session_state.analysis_result = None
                                st.session_state.suggested_metrics = None
                                st.session_state.step = 1
                                st.rerun()
                        else:
                            st.error(f"Failed: {resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    # Reset button
    st.divider()
    if st.button("🔄 Start Over"):
        st.session_state.analysis_result = None
        st.session_state.suggested_metrics = None
        st.session_state.step = 1
        st.rerun()


# -----------------------------------------------------------------------------
# Chat page helpers
# -----------------------------------------------------------------------------

def chat_api_message(message: str, history: list, include_context: bool = True) -> dict:
    """Send message to chat API and return response."""
    try:
        resp = requests.post(
            f"{API_URL}/chat",
            json={"message": message, "history": history, "include_context": include_context},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"response": f"Error: {str(e)}", "sources": []}


def chat_upload_logs(file) -> dict:
    """Upload log file via API."""
    try:
        files = {"file": (file.name, file.getvalue())}
        resp = requests.post(f"{API_URL}/upload/logs", files=files, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "ok": False}


def chat_upload_kb(file) -> dict:
    """Upload KB file via API."""
    try:
        files = {"file": (file.name, file.getvalue())}
        resp = requests.post(f"{API_URL}/upload/kb", files=files, timeout=120)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "ok": False}


def onboard_analyze_api(samples: list, max_samples: int = 20) -> dict:
    """Call onboard/analyze with samples."""
    try:
        resp = requests.post(
            f"{API_URL}/onboard/analyze",
            json={"samples": samples, "max_samples": max_samples},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def onboard_confirm_api(payload: dict) -> dict:
    """Call onboard/confirm with approved config."""
    try:
        resp = requests.post(f"{API_URL}/onboard/confirm", json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def render_chat():
    """Render the Chat page: uploads, text input, command handling, Q&A with RAG."""
    st.title("Chat")
    st.markdown("Upload logs or KB, ask questions about compliance, or use **/generate** and **/onboard** (with an attached file).")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "pending_onboard" not in st.session_state:
        st.session_state.pending_onboard = None
    if "last_uploaded_log" not in st.session_state:
        st.session_state.last_uploaded_log = None  # {name, content_preview} for /onboard

    # File upload zone
    st.subheader("Upload")
    col1, col2 = st.columns(2)
    with col1:
        log_file = st.file_uploader("Upload Logs", type=["txt", "csv", "json", "log"], key="chat_upload_logs")
        do_upload_logs = st.button("Upload and analyze logs", key="btn_upload_logs")
    with col2:
        kb_file = st.file_uploader("Upload KB", type=["md"], key="chat_upload_kb")
        do_upload_kb = st.button("Upload KB", key="btn_upload_kb")

    if do_upload_logs and log_file is not None:
        with st.spinner("Uploading and analyzing log file..."):
            result = chat_upload_logs(log_file)
            content_preview = log_file.getvalue().decode("utf-8", errors="ignore").splitlines()[:50]
            if result.get("ok"):
                st.session_state.last_uploaded_log = {
                    "name": log_file.name,
                    "content_preview": content_preview,
                    "format_detected": result.get("format_detected"),
                    "needs_onboard": result.get("needs_onboard", True),
                    "custom_match": result.get("custom_match"),
                }
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"Log file **{result.get('filename', 'file')}** saved. "
                    + (result.get("message", "") or (
                        "Use **/onboard** to add this format." if result.get("needs_onboard")
                        else "Format detected. You can **/generate** reports."
                    )),
                    "sources": [],
                })
            else:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"Upload failed: {result.get('error', 'Unknown error')}",
                    "sources": [],
                })
            st.rerun()
    if do_upload_kb and kb_file is not None:
        with st.spinner("Uploading KB and re-indexing..."):
            result = chat_upload_kb(kb_file)
            if result.get("ok"):
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"KB file **{result.get('filename', 'file')}** saved and index updated. You can ask questions about it.",
                    "sources": [],
                })
            else:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"Upload failed: {result.get('error', 'Unknown error')}",
                    "sources": [],
                })
            st.rerun()

    # Pending onboard confirmation UI
    if st.session_state.pending_onboard:
        pending = st.session_state.pending_onboard
        st.info("Review proposed format mappings below. Confirm to save, or send a new message to cancel.")
        st.json(pending.get("config", {}))
        if st.button("Confirm and save format", key="confirm_onboard_btn"):
            payload = {
                "format_id": pending["format_id"],
                "format_name": pending["config"].get("format_name", pending["format_id"]),
                "format_type": pending["config"].get("format_type", "unknown"),
                "detection_rules": pending["config"].get("detection_rules", {}),
                "field_mappings": pending["config"].get("field_mappings", {}),
                "unmapped_fields": pending["config"].get("unmapped_fields", []),
                "approved_by": "webui_user",
            }
            confirm_result = onboard_confirm_api(payload)
            if confirm_result.get("ok"):
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"Format **{pending['format_id']}** saved. You can now generate reports using this format.",
                    "sources": [],
                })
                st.session_state.pending_onboard = None
            else:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"Save failed: {confirm_result.get('error', 'Unknown error')}",
                    "sources": [],
                })
                st.session_state.pending_onboard = None
            st.rerun()

    # Chat history
    st.subheader("Conversation")
    if st.button("Clear Chat", key="clear_chat_btn", help="Clear chat history and uploaded file pointers (does not delete files from data/)"):
        st.session_state.chat_messages = []
        st.session_state.last_uploaded_log = None
        st.session_state.pending_onboard = None
        st.rerun()
    for idx, msg in enumerate(st.session_state.chat_messages):
        role = msg.get("role", "user")
        content = msg.get("content", "")
        with st.chat_message(role):
            st.markdown(content)
            # Confidence badge + expandable factors (assistant messages with RAG)
            confidence = msg.get("confidence")
            if confidence is not None and role == "assistant":
                if confidence >= 70:
                    badge_color = "green"
                elif confidence >= 40:
                    badge_color = "orange"
                else:
                    badge_color = "red"
                factors = msg.get("confidence_factors", [])
                with st.expander(f":{badge_color}[Confidence: {confidence:.0f}%] — What impacted it?"):
                    for f in factors:
                        f_score = f.get("score", 0)
                        f_name = f.get("name", "")
                        f_desc = f.get("description", "")
                        bar_val = max(0.0, min(f_score / 100.0, 1.0))
                        st.markdown(f"**{f_name}** — {f_score:.0f}%")
                        st.progress(bar_val)
                        st.caption(f_desc)
            # Sources (separate expander)
            if msg.get("sources"):
                with st.expander("Sources", expanded=False):
                    for s in msg["sources"]:
                        st.caption(f"{s.get('source', '')}: {s.get('title', '')}")

    # Text input and send
    user_input = st.chat_input("Message or /generate, /onboard (attach file above for commands)")
    if user_input:
        text = user_input.strip()
        st.session_state.chat_messages.append({"role": "user", "content": text, "sources": []})

        # Command handling
        if text.lower().startswith("/generate"):
            last_log = st.session_state.get("last_uploaded_log")
            if last_log and last_log.get("needs_onboard"):
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": "Report generation skipped: the uploaded log format is not onboarded. Use **/onboard** to add this format first, then **/generate**.",
                    "sources": [],
                })
                st.rerun()
            else:
                format_info = ""
                if last_log and last_log.get("format_detected"):
                    format_info = f" Format detected: **{last_log.get('format_detected')}**. "
                with st.spinner("Generating report..."):
                    filename = last_log.get("name") if last_log else None
                    gen_result = trigger_report_generation(filename=filename)
                    if gen_result.get("error"):
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": f"Report generation failed: {gen_result.get('error')}. {gen_result.get('detail', '')}",
                            "sources": [],
                        })
                    else:
                        wins = gen_result.get("windows", [])
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": f"{format_info}Generated {len(wins)} report(s). " + "; ".join(f"`{w.get('output', '')}`" for w in wins),
                            "sources": [],
                        })
                    st.rerun()

        elif text.lower().startswith("/onboard"):
            last_log = st.session_state.get("last_uploaded_log")
            if not last_log or not last_log.get("content_preview"):
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": "**/onboard** requires a log file. Use 'Upload Logs' and click 'Upload and analyze logs', then send **/onboard**.",
                    "sources": [],
                })
            else:
                with st.spinner("Analyzing format..."):
                    samples = last_log["content_preview"]
                    analyze_result = onboard_analyze_api(samples)
                    if analyze_result.get("error"):
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": f"Analysis failed: {analyze_result.get('error')}",
                            "sources": [],
                        })
                    else:
                        format_id = (analyze_result.get("format_name") or "custom").replace(" ", "_").lower()[:64]
                        st.session_state.pending_onboard = {
                            "format_id": format_id,
                            "config": analyze_result,
                            "samples_file_name": last_log.get("name", ""),
                        }
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": "Proposed format mappings are shown below. Review and click **Confirm and save format** to onboard.",
                            "sources": [],
                        })
                    st.rerun()

        else:
            # Regular chat with RAG
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_messages[:-1]
            ]
            result = chat_api_message(text, history, include_context=True)
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": result.get("response", ""),
                "sources": result.get("sources", []),
                "confidence": result.get("confidence"),
                "confidence_factors": result.get("confidence_factors", []),
            })
            st.rerun()


def main():
    """Main application entry point."""
    page = render_sidebar()
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "Chat":
        render_chat()
    elif page == "Format Onboarding":
        render_format_onboarding()
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

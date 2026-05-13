"""
ArcGIS Pro Script Helper — AI-Powered GIS Assistant
ITI Gen AI Course · Day 3 Assignment
Specialty: ArcGIS Pro Script Helper (ArcPy)
"""

import streamlit as st
import google.generativeai as genai
from groq import Groq
import os
import json
import re
import time
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# APP CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

APP_TITLE = "🗺️ ArcGIS Pro Script Helper"
APP_ICON = "🗺️"
APP_SUBTITLE = "Your AI-powered ArcPy & ModelBuilder companion"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Professional GIS dark theme
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Root variables */
:root {
    --esri-blue: #0079c1;
    --esri-blue-dark: #005a8e;
    --esri-green: #00897b;
    --bg-dark: #0d1117;
    --bg-card: #161b22;
    --bg-sidebar: #0d1117;
    --border: #30363d;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --accent: #58a6ff;
    --success: #3fb950;
    --warning: #d29922;
    --code-bg: #1e2432;
}

/* Global font */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* Main background */
.stApp {
    background-color: var(--bg-dark);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent);
}

/* Header strip */
.app-header {
    background: linear-gradient(135deg, #0d1f3c 0%, #0a2d4a 50%, #0d1f3c 100%);
    border: 1px solid var(--esri-blue-dark);
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.app-header h1 {
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}
.app-header p {
    color: var(--text-secondary);
    margin: 2px 0 0 0;
    font-size: 0.85rem;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    margin-bottom: 8px !important;
}

/* Code blocks inside chat */
[data-testid="stChatMessage"] code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem;
    background-color: var(--code-bg) !important;
    color: #79c0ff !important;
    padding: 2px 5px;
    border-radius: 4px;
}
[data-testid="stChatMessage"] pre {
    background-color: var(--code-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 14px !important;
}
[data-testid="stChatMessage"] pre code {
    background: transparent !important;
    color: #a5d6ff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.80rem !important;
    padding: 0 !important;
}

/* Input box */
[data-testid="stChatInput"] {
    border-color: var(--esri-blue) !important;
    background-color: var(--bg-card) !important;
}

/* Buttons */
.stButton > button {
    background-color: var(--esri-blue) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: background-color 0.2s ease !important;
}
.stButton > button:hover {
    background-color: var(--esri-blue-dark) !important;
}

/* Preset prompt buttons */
.preset-btn > button {
    background-color: var(--bg-card) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border) !important;
    font-size: 0.78rem !important;
    padding: 4px 10px !important;
    margin: 2px !important;
}
.preset-btn > button:hover {
    border-color: var(--esri-blue) !important;
    background-color: #1c2a3a !important;
}

/* Metric boxes */
.metric-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 16px;
    text-align: center;
}
.metric-box .value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--accent);
}
.metric-box .label {
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Select boxes and inputs */
.stSelectbox, .stTextInput, .stTextArea, .stSlider {
    color: var(--text-primary) !important;
}

/* Dividers */
hr {
    border-color: var(--border) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
}

/* Token counter badge */
.token-badge {
    display: inline-block;
    background: #1c2a3a;
    border: 1px solid var(--esri-blue);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 12px;
    margin-left: 8px;
}

/* Warning/info boxes */
.stAlert {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPTS — ArcGIS Pro Script Helper Specialty
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "🗺️ ArcGIS Pro — General Helper": """You are an expert ArcGIS Pro assistant with 15+ years of experience in the Esri ecosystem.
You specialize in:
- ArcPy scripting (Python API for ArcGIS Pro)
- ModelBuilder automation and export to Python
- ArcGIS Pro geoprocessing tools and their parameters
- Spatial analysis, cartography, and data management workflows

When generating ArcPy scripts:
1. Use the MODERN ArcPy API (ArcGIS Pro 3.x) — NOT ArcGIS Desktop 10.x legacy calls
2. Always use arcpy.env.workspace and arcpy.env.overwriteOutput
3. Prefer arcpy.analysis, arcpy.management, arcpy.conversion modules as appropriate
4. Include proper error handling with arcpy.GetMessages()
5. Add a clear docstring at the top explaining inputs, outputs, and purpose
6. Cite full tool names (e.g., arcpy.analysis.Buffer) not shorthand

Your audience: professional GIS analysts and developers. Be concise, technical, and precise.
When discussing projections, always cite the WKID (Well-Known ID) / EPSG code.
Never confuse ArcPy with PyQGIS or GDAL — they are different APIs.""",

    "⚙️ ArcPy Script Generator": """You are an ArcPy code generator for ArcGIS Pro. Your ONLY job is to write clean, production-ready Python scripts.

Rules:
1. Output Python code FIRST, explanation after
2. Use arcpy.env.workspace, arcpy.env.overwriteOutput = True at the start
3. Wrap all geoprocessing in try/except with arcpy.GetMessages(2) for error details
4. Use full module paths: arcpy.management.CopyFeatures, NOT CopyFeatures_management
5. All file paths as variables at the top — never hardcode paths inside tool calls
6. Include a header comment block: Purpose, Inputs, Outputs, Requirements
7. Always check if output already exists before overwriting

ArcGIS Pro version: 3.x
Python version: 3.x (conda environment)
Do NOT use arcpy.mapping (that is ArcMap/Desktop — use arcpy.mp for ArcGIS Pro)""",

    "🔍 Spatial Analysis Advisor": """You are a spatial analysis expert specializing in ArcGIS Pro tools and workflows.

Your role:
- Recommend the correct ArcGIS Pro tool for a given spatial analysis problem
- Explain parameter choices (distance units, method, environment settings)
- Warn about common pitfalls (projection issues, topology errors, large datasets)
- Suggest the right coordinate system for the task (always cite WKID/EPSG)
- Compare ArcGIS Pro tools vs open-source alternatives when relevant

When recommending analysis workflows:
1. List the tools in order (workflow steps)
2. Mention key parameters for each
3. Flag coordinate system requirements
4. Estimate processing time for typical dataset sizes
5. Mention licensing requirements (Basic/Standard/Advanced/Extensions)""",

    "🗂️ Data Management & ETL": """You are an ArcGIS Pro data management and ETL expert.

Specialties:
- File Geodatabase (FGDB) and Enterprise GDB management
- Feature class and table operations (schema, domains, subtypes)
- Data conversion (Shapefile ↔ FGDB ↔ GeoJSON ↔ CSV ↔ KML)
- Batch processing with arcpy.da cursors (SearchCursor, InsertCursor, UpdateCursor)
- Attribute table operations, field calculations, and joins
- Raster management and mosaic datasets

Always:
- Prefer arcpy.da cursors over arcpy.SearchCursor (legacy) for performance
- Use context managers (with arcpy.da.SearchCursor(...) as cursor:) 
- Mention field type requirements (TEXT, DOUBLE, SHORT, LONG, DATE)
- Warn about NULL handling in cursors
- Explain geodatabase locks and how to release them""",

    "🖼️ Layout & Cartography Helper": """You are an ArcGIS Pro cartography and layout automation expert using arcpy.mp.

Specialties:
- arcpy.mp (ArcGIS Pro Map Module) for layout automation
- Map frame, legend, north arrow, scale bar manipulation via Python
- Exporting layouts to PDF, PNG, TIFF
- Dynamic text and data-driven pages (Map Series)
- Layer symbology automation (CIMSymbol, color ramps)
- Print quality settings (DPI, extent, spatial reference)

Important: arcpy.mp is ONLY for ArcGIS Pro — do NOT use arcpy.mapping (that's ArcMap).
Key objects: ArcGISProject, Map, Layout, MapFrame, MapSeries
Always open projects with arcpy.mp.ArcGISProject(aprx_path)""",
}

# ─────────────────────────────────────────────────────────────────────────────
# PRESET PROMPTS — One-click common ArcGIS tasks
# ─────────────────────────────────────────────────────────────────────────────

PRESET_PROMPTS = {
    "Buffer + Intersect": "Write an ArcPy script that buffers a roads layer by 500 meters and intersects the buffer with a parcels layer. Save results to a file geodatabase.",
    "Batch Reproject": "Write an ArcPy script that reprojects all feature classes in a folder from EPSG:4326 (WGS84) to EPSG:32636 (UTM Zone 36N). Process recursively.",
    "Attribute Table Export": "Write an ArcPy script using arcpy.da.SearchCursor to export all records from a feature class attribute table to a CSV file.",
    "Clip by Extent": "Write an ArcPy script that clips multiple raster files in a folder to a polygon boundary layer and saves each clipped output to a new folder.",
    "Field Calculator": "Write an ArcPy script using UpdateCursor to calculate the area in square kilometers for all features in a polygon layer and store it in a new AREA_KM2 field.",
    "Layout to PDF": "Write an ArcPy script using arcpy.mp to export all layouts in an ArcGIS Pro project (.aprx) to individual PDF files.",
    "Merge Feature Classes": "Write an ArcPy script that merges multiple feature classes of the same geometry type from a folder into a single output feature class.",
    "Spatial Join": "Explain and write an ArcPy script for a spatial join between a points layer (survey sites) and a polygons layer (administrative boundaries) to add region names to each point.",
    "CRS Best Practice": "What is the best coordinate reference system (WKID/EPSG) for mapping and analysis in Egypt? Explain when to use each.",
    "ModelBuilder to Python": "Explain how to export a ModelBuilder model to a Python script in ArcGIS Pro, and what changes I should make to the exported code to make it production-ready.",
}

# ─────────────────────────────────────────────────────────────────────────────
# PROVIDER MODELS
# ─────────────────────────────────────────────────────────────────────────────

MODELS = {
    "🔵 Gemini 2.5 Flash  (Fast · Free · Recommended)": {
        "provider": "gemini",
        "id": "gemini-2.5-flash",
    },
    "🔵 Gemini 2.5 Pro  (Smarter · Slower)": {
        "provider": "gemini",
        "id": "gemini-2.5-pro",
    },
    "⚡ Groq · Llama 3.3 70B  (Fastest response)": {
        "provider": "groq",
        "id": "llama-3.3-70b-versatile",
    },
    "⚡ Groq · Llama 3.1 8B  (Ultra-fast · Lighter)": {
        "provider": "groq",
        "id": "llama-3.1-8b-instant",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# TOKEN ESTIMATION
# ─────────────────────────────────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English, ~2 for Arabic."""
    arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06ff')
    other_chars = len(text) - arabic_chars
    return int((arabic_chars / 2) + (other_chars / 4))


def count_history_tokens(messages: list) -> int:
    total = ""
    for m in messages:
        total += m.get("content", "")
    return estimate_tokens(total)

# ─────────────────────────────────────────────────────────────────────────────
# API CALL FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def stream_gemini(messages: list, system_prompt: str, model_id: str, api_key: str, temperature: float):
    """Stream response from Gemini."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_id, system_instruction=system_prompt)

    # Build Gemini history (all but last message)
    gemini_history = []
    for msg in messages[:-1]:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=gemini_history)

    response = chat.send_message(
        messages[-1]["content"],
        stream=True,
        generation_config={"temperature": temperature, "max_output_tokens": 4096},
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text


def stream_groq(messages: list, system_prompt: str, model_id: str, api_key: str, temperature: float):
    """Stream response from Groq."""
    client = Groq(api_key=api_key)

    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    response = client.chat.completions.create(
        model=model_id,
        messages=groq_messages,
        temperature=temperature,
        max_tokens=4096,
        stream=True,
    )
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT CHAT TO MARKDOWN
# ─────────────────────────────────────────────────────────────────────────────

def export_chat_to_markdown(messages: list, system_prompt: str, model_label: str) -> str:
    """Convert chat history to a clean Markdown document."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# ArcGIS Pro Script Helper — Chat Export",
        f"",
        f"**Exported:** {timestamp}  ",
        f"**Model:** {model_label}  ",
        f"**System Prompt:** {system_prompt[:120]}...  ",
        f"",
        f"---",
        f"",
    ]
    for msg in messages:
        role_label = "🧑 **You**" if msg["role"] == "user" else "🤖 **Assistant**"
        lines.append(f"### {role_label}")
        lines.append(f"")
        lines.append(msg["content"])
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
    return "\n".join(lines)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens_sent" not in st.session_state:
    st.session_state.total_tokens_sent = 0
if "total_tokens_received" not in st.session_state:
    st.session_state.total_tokens_received = 0
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "preset_trigger" not in st.session_state:
    st.session_state.preset_trigger = None

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    # Logo / branding
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size: 2.4rem;'>🗺️</div>
        <div style='font-weight: 600; font-size: 1.1rem; color: #58a6ff;'>ArcGIS Pro</div>
        <div style='font-size: 0.78rem; color: #8b949e;'>Script Helper · AI Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Settings")

    # --- Provider selection
    model_label = st.selectbox(
        "Model",
        list(MODELS.keys()),
        help="Gemini Flash = best default (free + fast). Groq = ultra-fast text responses."
    )
    selected_model = MODELS[model_label]

    st.markdown("---")

    # --- API Keys
    provider = selected_model["provider"]
    if provider == "gemini":
        api_key = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            value=os.environ.get("GOOGLE_API_KEY", ""),
            help="Get free at https://aistudio.google.com",
        )
    else:
        api_key = st.text_input(
            "🔑 Groq API Key",
            type="password",
            value=os.environ.get("GROQ_API_KEY", ""),
            help="Get free at https://console.groq.com",
        )

    st.markdown("---")

    # --- Specialty / System Prompt
    preset_label = st.selectbox(
        "Specialty Preset",
        list(SYSTEM_PROMPTS.keys()),
        help="Choose the ArcGIS Pro domain focus for this session."
    )
    system_prompt = st.text_area(
        "System Prompt",
        value=SYSTEM_PROMPTS[preset_label],
        height=160,
        help="Customize the AI's persona and rules."
    )

    st.markdown("---")

    # --- Temperature
    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.2,
        step=0.1,
        help="Lower = more deterministic code output. Higher = more creative/varied."
    )
    st.caption(
        "💡 Recommended: **0.1–0.2** for scripts, **0.5** for explanations"
    )

    st.markdown("---")

    # --- Stats
    st.markdown("### 📊 Session Stats")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='value'>{st.session_state.message_count}</div>
            <div class='label'>Messages</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='value'>~{st.session_state.total_tokens_sent + st.session_state.total_tokens_received:,}</div>
            <div class='label'>Tokens Used</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # --- Export & Clear buttons
    if st.session_state.messages:
        md_export = export_chat_to_markdown(
            st.session_state.messages, system_prompt, model_label
        )
        st.download_button(
            label="📥 Export Chat (Markdown)",
            data=md_export,
            file_name=f"arcgis_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_tokens_sent = 0
        st.session_state.total_tokens_received = 0
        st.session_state.message_count = 0
        st.session_state.preset_trigger = None
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.70rem; color:#8b949e; text-align:center;'>"
        "ITI · Gen AI Course · GIS Track<br>Day 3 Assignment · ArcGIS Pro Helper"
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA — Header
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class='app-header'>
    <div style='font-size: 2rem;'>🗺️</div>
    <div>
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE} &nbsp;·&nbsp; <span style='color:#58a6ff;'>{model_label.split('(')[0].strip()}</span></p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PRESET PROMPTS — Quick-access buttons
# ─────────────────────────────────────────────────────────────────────────────

with st.expander("⚡ Quick Preset Prompts — click to load", expanded=False):
    st.markdown(
        "<div style='font-size:0.80rem; color:#8b949e; margin-bottom:8px;'>"
        "Click any prompt to send it instantly to the chat.</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(5)
    preset_keys = list(PRESET_PROMPTS.keys())
    for i, key in enumerate(preset_keys):
        with cols[i % 5]:
            st.markdown("<div class='preset-btn'>", unsafe_allow_html=True)
            if st.button(key, key=f"preset_{i}"):
                st.session_state.preset_trigger = PRESET_PROMPTS[key]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHAT HISTORY DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

# Welcome message when chat is empty
if not st.session_state.messages:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #0d1f3c, #0a2d4a);
        border: 1px dashed #30363d;
        border-radius: 10px;
        padding: 28px 32px;
        text-align: center;
        margin: 20px 0;
    '>
        <div style='font-size: 2.5rem; margin-bottom: 12px;'>🐍</div>
        <div style='font-size: 1.1rem; font-weight: 600; color: #e6edf3; margin-bottom: 8px;'>
            Ready to generate ArcPy scripts
        </div>
        <div style='font-size: 0.85rem; color: #8b949e; max-width: 480px; margin: 0 auto;'>
            Ask me to write ArcPy scripts, explain geoprocessing tools, recommend workflows,
            or help with ModelBuilder automation. Use the preset buttons above for quick starts.
        </div>
        <div style='margin-top: 16px; font-size: 0.78rem; color: #58a6ff;'>
            💡 Tip: Set your API key in the sidebar before chatting
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────────────────────────────────────
# HANDLE PRESET TRIGGER
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.preset_trigger:
    user_input = st.session_state.preset_trigger
    st.session_state.preset_trigger = None
else:
    user_input = st.chat_input("Ask about ArcPy, geoprocessing tools, spatial analysis workflows...")

# ─────────────────────────────────────────────────────────────────────────────
# PROCESS USER INPUT
# ─────────────────────────────────────────────────────────────────────────────

if user_input:
    # Validate API key
    if not api_key or len(api_key.strip()) < 10:
        st.error(
            "⚠️ Please enter a valid API key in the sidebar before chatting. "
            f"{'Get Gemini key free at https://aistudio.google.com' if provider == 'gemini' else 'Get Groq key free at https://console.groq.com'}"
        )
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1

    tokens_in = estimate_tokens(user_input + system_prompt)
    st.session_state.total_tokens_sent += tokens_in

    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream assistant response
    with st.chat_message("assistant"):
        try:
            if provider == "gemini":
                stream_fn = stream_gemini(
                    st.session_state.messages,
                    system_prompt,
                    selected_model["id"],
                    api_key,
                    temperature,
                )
            else:
                stream_fn = stream_groq(
                    st.session_state.messages,
                    system_prompt,
                    selected_model["id"],
                    api_key,
                    temperature,
                )

            full_response = st.write_stream(stream_fn)

        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "quota" in err_msg.lower() or "rate" in err_msg.lower():
                full_response = (
                    "⚠️ **Rate limit reached.** Please wait a moment and try again.\n\n"
                    "💡 Tip: Switch to a different model in the sidebar to bypass this limit."
                )
            elif "401" in err_msg or "invalid" in err_msg.lower() or "api key" in err_msg.lower():
                full_response = (
                    "⚠️ **Invalid API key.** Please check your key in the sidebar.\n\n"
                    f"- Gemini keys: [aistudio.google.com](https://aistudio.google.com)\n"
                    f"- Groq keys: [console.groq.com](https://console.groq.com)"
                )
            elif "403" in err_msg:
                full_response = "⚠️ **Access denied.** Your API key may not have permission for this model."
            else:
                full_response = f"⚠️ **Unexpected error:** {err_msg}\n\nPlease try again or switch models."
            st.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.total_tokens_received += estimate_tokens(full_response)
    st.rerun()

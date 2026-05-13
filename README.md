# 🗺️ ArcGIS Pro Script Helper

> An AI-powered GIS assistant that generates ArcPy scripts, explains geoprocessing tools, and guides spatial analysis workflows — built with Streamlit and powered by Gemini + Groq.

**ITI · Gen AI Course · GIS Track · Day 3 Assignment**  
**Specialty:** ArcGIS Pro Script Helper (ArcPy)

---

## 🎯 What It Does

The ArcGIS Pro Script Helper is a chat assistant specialized for GIS professionals who work with ArcGIS Pro. It can:

- ✅ **Generate ArcPy scripts** for common tasks (buffer, clip, intersect, reproject, export, cursor operations)
- ✅ **Explain geoprocessing tools** and their parameters
- ✅ **Recommend coordinate systems** (always with WKID/EPSG codes)
- ✅ **Convert ModelBuilder logic** to Python scripts
- ✅ **Automate layout exports** using `arcpy.mp`
- ✅ **Advise on data management** (cursors, geodatabases, schema operations)

---

## 🖥️ App Features

| Feature | Status |
|---|---|
| Streamlit UI (sidebar + main chat area) | ✅ |
| Secure API key input (`type="password"`) | ✅ |
| Model selection — Gemini Flash, Gemini Pro, Groq Llama 3.3 70B, Groq Llama 3.1 8B | ✅ |
| 5 Specialty presets with customizable system prompt | ✅ |
| Temperature slider (0.0 – 2.0) | ✅ |
| Streaming responses | ✅ |
| Chat history persistent in session | ✅ |
| Clear chat button | ✅ |
| 10 preset prompt buttons (one-click task templates) | ✅ Bonus |
| Export chat to Markdown (download button) | ✅ Bonus |
| Real-time token counter | ✅ Bonus |
| Multi-provider support (Gemini + Groq) | ✅ Bonus |
| Error handling (rate limits, invalid keys, empty responses) | ✅ Bonus |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- A free **Gemini API key** from [Google AI Studio](https://aistudio.google.com)
- *(Optional)* A free **Groq API key** from [Groq Console](https://console.groq.com)

### 1. Clone the repository

```bash
git clone https://github.com/abdelrahmanashrafc38-ops/ArcGIS-pro-AI-Assistant.git
cd ArcGIS-pro-AI-Assistant
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API keys

```bash
# Copy the template
cp .env.example .env

# Edit .env and add your keys
GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here   # optional
```

> **Alternative:** Enter API keys directly in the app's sidebar (they are not stored between sessions).

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Cloud (Bonus)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo, branch `main`, file `app.py`
5. Add secrets in the Streamlit Cloud dashboard:
   ```
   GOOGLE_API_KEY = "your_key"
   GROQ_API_KEY = "your_key"
   ```
6. Click **Deploy**

---

## 🧭 How to Use

### Basic Chat
1. Enter your API key in the sidebar
2. Choose a **Specialty Preset** matching your task
3. Adjust **Temperature** (0.1–0.2 for code, 0.5 for explanations)
4. Type your question or use a **Preset Prompt** button

### Preset Prompts
Click any button in the "Quick Preset Prompts" expander for instant script generation:
- Buffer + Intersect
- Batch Reproject
- Attribute Table Export
- Clip by Extent
- Field Calculator
- Layout to PDF
- Merge Feature Classes
- Spatial Join
- CRS Best Practice
- ModelBuilder to Python

### Exporting Your Session
Click **📥 Export Chat (Markdown)** in the sidebar to download the full conversation as a `.md` file — useful for documentation.

---

## 🗂️ Project Structure

```
ArcGIS-pro-AI-Assistant/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── DESIGN.md           # Assignment design document (system prompt, test cases, reflection)
├── .env.example        # API key template
└── .gitignore          # Excludes .env and temporary files
```

---

## ⚠️ Important Limitations

- The app **generates** scripts but cannot **execute** them — copy output into ArcGIS Pro's Python window or a `.py` file
- Scripts contain **placeholder paths** — replace them with your actual data paths before running
- Always **verify EPSG codes** at [epsg.io](https://epsg.io) — the AI can confuse Esri WKIDs with EPSG codes
- Test scripts on **small sample data** before running on production datasets
- `arcpy.env.overwriteOutput = True` is set by default in generated scripts — be aware this will overwrite existing outputs

---

## 📚 Course Context

This app was built as the **Day 3 Assignment** for the ITI Generative AI Course — GIS Track.

**Concepts applied from the course:**
- LLM API anatomy (system prompt, messages, temperature, streaming, max tokens)
- Multi-provider support (Gemini SDK + Groq SDK)
- Streaming responses with `st.write_stream`
- Session state management in Streamlit
- Structured error handling (429, 401, 403)
- System prompt engineering for domain-specific assistants

---

## 🙏 Credits

- [Google AI Studio](https://aistudio.google.com) — Gemini 2.5 Flash / Pro
- [Groq](https://console.groq.com) — Llama 3.3 70B / 3.1 8B
- [Streamlit](https://streamlit.io) — UI framework
- [Esri ArcGIS Pro Documentation](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm)

---

*Built with ❤️ for the ITI Gen AI Course · GIS Track*

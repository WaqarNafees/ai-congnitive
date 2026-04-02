import streamlit as st
from modules.pdf_extractor import extract_text_from_pdf
from modules.embeddings import EmbeddingStore
from modules.summarizer import generate_summary, extract_insights, detect_research_gaps, generate_hypotheses
from modules.qa_engine import answer_question

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

section[data-testid="stSidebar"] {
    background: #0d1120 !important;
    border-right: 1px solid #1e2540;
}

section[data-testid="stSidebar"] * {
    color: #c8ccd8 !important;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0.3rem;
    letter-spacing: -0.5px;
}

.hero-sub {
    text-align: center;
    color: #6b7280;
    font-size: 1.05rem;
    font-weight: 300;
    letter-spacing: 0.5px;
    margin-bottom: 2.5rem;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2540, #a78bfa33, #1e2540, transparent);
    margin: 1.5rem 0 2rem 0;
}

.metric-card {
    background: linear-gradient(135deg, #111827, #1a2035);
    border: 1px solid #1e2540;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: #a78bfa44;
    transform: translateY(-2px);
}

.metric-number {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #a78bfa;
}

.metric-label {
    font-size: 0.78rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.2rem;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: #e8eaf0;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.insight-card {
    background: linear-gradient(135deg, #111827ee, #131c2fee);
    border: 1px solid #1e2540;
    border-left: 3px solid #a78bfa;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: all 0.25s ease;
}

.insight-card:hover {
    border-left-color: #60a5fa;
    background: linear-gradient(135deg, #151f30ee, #1a2540ee);
}

.gap-card {
    background: linear-gradient(135deg, #130f1aee, #1a1025ee);
    border: 1px solid #2d1b4e;
    border-left: 3px solid #f472b6;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
}

.hyp-card {
    background: linear-gradient(135deg, #0d1f1aee, #0f2520ee);
    border: 1px solid #1a3d2e;
    border-left: 3px solid #34d399;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
}

.summary-box {
    background: linear-gradient(135deg, #111827, #131c2f);
    border: 1px solid #1e2540;
    border-radius: 12px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #c8ccd8;
    font-size: 0.97rem;
}

.card-number {
    display: inline-block;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #a78bfa22;
    color: #a78bfa;
    font-size: 0.75rem;
    font-weight: 600;
    text-align: center;
    line-height: 24px;
    margin-right: 0.6rem;
    flex-shrink: 0;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px #7c3aed33 !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca) !important;
    box-shadow: 0 6px 20px #7c3aed55 !important;
    transform: translateY(-1px) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0d1120 !important;
    border-bottom: 1px solid #1e2540 !important;
    gap: 0.5rem;
    padding: 0 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border: none !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    padding: 0.7rem 1.2rem !important;
    border-radius: 8px 8px 0 0 !important;
}

.stTabs [aria-selected="true"] {
    background: #1a2035 !important;
    color: #a78bfa !important;
    border-bottom: 2px solid #a78bfa !important;
}

.upload-hint {
    background: linear-gradient(135deg, #111827, #131c2f);
    border: 1px dashed #2d3556;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    color: #4b5563;
    font-size: 0.9rem;
}

.stTextArea textarea, .stChatInput input {
    background: #111827 !important;
    border: 1px solid #1e2540 !important;
    color: #e8eaf0 !important;
    border-radius: 8px !important;
}

.status-badge {
    display: inline-block;
    background: #34d39922;
    color: #34d399;
    border: 1px solid #34d39944;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.5px;
}

.sidebar-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #a78bfa !important;
    margin-bottom: 0.2rem;
}

.sidebar-sub {
    font-size: 0.78rem;
    color: #4b5563 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

div[data-testid="stChatMessage"] {
    background: #111827 !important;
    border: 1px solid #1e2540 !important;
    border-radius: 10px !important;
    margin-bottom: 0.8rem !important;
}

.word-count {
    font-size: 0.78rem;
    color: #4b5563;
    text-align: right;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
for key in ["paper_text", "paper_name", "embedding_store", "summary",
            "insights", "gaps", "hypotheses", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">🔬 ResearchMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">AI Research Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**Analysis Settings**")
    num_hypotheses = st.slider("Hypotheses to Generate", 1, 5, 3)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.session_state.paper_text:
        word_count = len(st.session_state.paper_text.split())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{word_count:,}</div>
            <div class="metric-label">Words Extracted</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<span class="status-badge">● Paper Loaded</span>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;color:#374151;text-align:center;">Powered by Groq · LLaMA 3.3<br>Built with Streamlit</div>', unsafe_allow_html=True)

# ── Process Upload ─────────────────────────────────────────────────────────────
if uploaded_file and uploaded_file.name != st.session_state.paper_name:
    with st.spinner("Extracting and indexing paper..."):
        text = extract_text_from_pdf(uploaded_file)
        st.session_state.paper_text = text
        st.session_state.paper_name = uploaded_file.name
        for k in ["summary", "insights", "gaps", "hypotheses"]:
            st.session_state[k] = None
        st.session_state.chat_history = []
        store = EmbeddingStore()
        store.build(text)
        st.session_state.embedding_store = store

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">ResearchMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Intelligent Analysis · Deep Insights · Research Acceleration</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📋  Summary  ",
    "  💡  Insights  ",
    "  🔍  Research Gaps  ",
    "  🚀  Hypotheses  ",
    "  💬  Q&A Chat  "
])

# ── Tab 1: Summary ─────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">📋 Paper Summary</div>', unsafe_allow_html=True)
    if not st.session_state.paper_text:
        st.markdown('<div class="upload-hint">📂 Upload a research paper from the sidebar to begin analysis</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Generate Summary"):
                with st.spinner("Analyzing paper..."):
                    st.session_state.summary = generate_summary(st.session_state.paper_text)
        if st.session_state.summary:
            st.markdown(f'<div class="summary-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
        with st.expander("View Extracted Raw Text"):
            st.text_area("", st.session_state.paper_text[:4000], height=300, label_visibility="collapsed")
            st.markdown(f'<div class="word-count">{len(st.session_state.paper_text.split()):,} words extracted</div>', unsafe_allow_html=True)

# ── Tab 2: Insights ────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">💡 Key Insights & Trends</div>', unsafe_allow_html=True)
    if not st.session_state.paper_text:
        st.markdown('<div class="upload-hint">📂 Upload a research paper to extract insights</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Extract Insights"):
                with st.spinner("Extracting insights..."):
                    st.session_state.insights = extract_insights(st.session_state.paper_text)
        if st.session_state.insights:
            for i, insight in enumerate(st.session_state.insights, 1):
                st.markdown(f"""
                <div class="insight-card">
                    <span class="card-number">{i}</span>
                    <span style="color:#c8ccd8;font-size:0.95rem;">{insight}</span>
                </div>""", unsafe_allow_html=True)

# ── Tab 3: Gaps ────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">🔍 Research Gaps & Limitations</div>', unsafe_allow_html=True)
    if not st.session_state.paper_text:
        st.markdown('<div class="upload-hint">📂 Upload a research paper to detect gaps</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Detect Gaps"):
                with st.spinner("Identifying gaps..."):
                    st.session_state.gaps = detect_research_gaps(st.session_state.paper_text)
        if st.session_state.gaps:
            for i, gap in enumerate(st.session_state.gaps, 1):
                st.markdown(f"""
                <div class="gap-card">
                    <span class="card-number" style="background:#f472b622;color:#f472b6;">{i}</span>
                    <span style="color:#c8ccd8;font-size:0.95rem;">{gap}</span>
                </div>""", unsafe_allow_html=True)

# ── Tab 4: Hypotheses ──────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">🚀 Novel Hypotheses</div>', unsafe_allow_html=True)
    if not st.session_state.paper_text:
        st.markdown('<div class="upload-hint">📂 Upload a research paper to generate hypotheses</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Generate Hypotheses"):
                with st.spinner("Generating hypotheses..."):
                    st.session_state.hypotheses = generate_hypotheses(st.session_state.paper_text, n=num_hypotheses)
        if st.session_state.hypotheses:
            for i, hyp in enumerate(st.session_state.hypotheses, 1):
                st.markdown(f"""
                <div class="hyp-card">
                    <span class="card-number" style="background:#34d39922;color:#34d399;">{i}</span>
                    <span style="color:#c8ccd8;font-size:0.95rem;">{hyp}</span>
                </div>""", unsafe_allow_html=True)

# ── Tab 5: Q&A ─────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-title">💬 Interactive Q&A</div>', unsafe_allow_html=True)
    if not st.session_state.paper_text:
        st.markdown('<div class="upload-hint">📂 Upload a research paper to start asking questions</div>', unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        user_q = st.chat_input("Ask anything about the paper — methodology, findings, limitations...")
        if user_q:
            st.session_state.chat_history.append({"role": "user", "content": user_q})
            with st.chat_message("user"):
                st.markdown(user_q)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context = st.session_state.embedding_store.retrieve(user_q) if st.session_state.embedding_store else st.session_state.paper_text[:4000]
                    answer = answer_question(user_q, context)
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})

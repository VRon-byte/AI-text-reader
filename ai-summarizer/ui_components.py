import streamlit as st
from datetime import datetime
from main import generate_response
from prompts import build_prompt


def apply_custom_styles():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <style>
    /* ── Base ─────────────────────────────────────────────────────── */
    * { box-sizing: border-box; }

    .stApp {
        background: #080d14;
        font-family: 'DM Sans', sans-serif;
        color: #c9d4e8;
    }

    .block-container {
        padding: 1.5rem 2rem 4rem 2rem !important;
        max-width: 100% !important;
    }

    /* ── Sidebar: always expanded, never collapsed ────────────────── */
    section[data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        transform: none !important;
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        background: #0b1220 !important;
        border-right: 1px solid #14243a !important;
        position: relative !important;
        z-index: 1 !important;
    }

    /* Counteract Streamlit's collapsed translation */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: none !important;
        margin-left: 0 !important;
        left: 0 !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding: 1.4rem 1rem 2rem 1rem !important;
        width: 260px !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }

    /* Hide every collapse/expand toggle button */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarNavCollapseButton"],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    button[kind="header"] { display: none !important; }

    /* Kill other Streamlit chrome */
    #MainMenu, footer, header, .stDeployButton { display: none !important; }

    /* ── Nav logo / tagline ───────────────────────────────────────── */
    .nav-logo {
        font-family: 'DM Serif Display', serif;
        font-size: 1.55rem;
        color: #e8c97a;
        letter-spacing: -0.5px;
        line-height: 1;
        margin-bottom: 0.15rem;
    }

    .nav-tagline {
        font-size: 0.65rem;
        color: #3a5270;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1.4rem;
    }

    .nav-section-label {
        font-size: 0.62rem;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #2a4060;
        margin: 1.1rem 0 0.45rem 0.1rem;
    }

    /* ── Scrollable chat box ──────────────────────────────────────── */
    .chat-scroll-box {
        max-height: 55vh;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 0.5rem 0.2rem 0.5rem 0;
        margin-bottom: 0.5rem;
    }

    .chat-scroll-box::-webkit-scrollbar { width: 4px; }
    .chat-scroll-box::-webkit-scrollbar-track { background: transparent; }
    .chat-scroll-box::-webkit-scrollbar-thumb { background: #1e3050; border-radius: 6px; }

    /* ── Buttons ──────────────────────────────────────────────────── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        border-radius: 8px;
        border: 1px solid #14243a;
        background: #0d1a2d;
        color: #5a7898;
        padding: 0.42rem 0.85rem;
        transition: all 0.16s ease;
        letter-spacing: 0.01em;
        text-align: left;
        width: 100%;
    }

    .stButton > button:hover {
        background: #122035;
        border-color: #1e3a5f;
        color: #c9d4e8;
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    }

    .stButton > button[kind="primary"] {
        background: #0f2748;
        border-color: #1e4070;
        color: #8ab4e0;
    }

    .stButton > button[kind="primary"]:hover {
        background: #163460;
        color: #c8e0f8;
    }

    /* ── Session tab buttons — pill style ─────────────────────────── */
    /* Wrap session tabs in a div with class "tab-strip" in Python,    */
    /* OR just rely on the first stHorizontalBlock in main area        */
    .tab-strip-row > div[data-testid="stHorizontalBlock"] {
        gap: 0.3rem !important;
        margin-bottom: 0.8rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #0f1e32;
    }

    /* ── Inputs ───────────────────────────────────────────────────── */
    .stTextInput > div > div > input {
        background: #0a1624 !important;
        border: 1px solid #14243a !important;
        border-radius: 9px !important;
        color: #c9d4e8 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.86rem !important;
        padding: 0.5rem 0.8rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #1e4a80 !important;
        box-shadow: 0 0 0 3px rgba(30,74,128,0.18) !important;
    }

    .stTextInput > div > div > input::placeholder { color: #2a4060 !important; }

    .stSelectbox > div > div {
        background: #0a1624 !important;
        border: 1px solid #14243a !important;
        border-radius: 9px !important;
        color: #c9d4e8 !important;
    }

    [data-testid="stChatInput"] > div {
        background: #0a1624 !important;
        border: 1px solid #14243a !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #c9d4e8 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 1px dashed #14243a !important;
        border-radius: 10px !important;
        background: #080f1c !important;
    }

    [data-testid="stFileUploader"] label { display: none !important; }

    /* ── Chat messages ────────────────────────────────────────────── */
    .msg-wrapper {
        display: flex;
        gap: 0.7rem;
        align-items: flex-start;
        margin-bottom: 0.9rem;
        animation: fadeUp 0.22s ease forwards;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(7px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .msg-wrapper.user-msg { flex-direction: row-reverse; }

    .msg-avatar {
        font-size: 1.1rem;
        flex-shrink: 0;
        width: 1.8rem;
        text-align: center;
        margin-top: 0.15rem;
    }

    .msg-bubble {
        max-width: 78%;
        border-radius: 13px;
        padding: 0.8rem 1rem;
    }

    .user-msg .msg-bubble {
        background: #0d2240;
        border: 1px solid #1a3a60;
        border-top-right-radius: 4px;
    }

    .assistant-msg .msg-bubble {
        background: #0b1a30;
        border: 1px solid #12243a;
        border-top-left-radius: 4px;
    }

    .msg-content {
        font-size: 0.88rem;
        line-height: 1.35;
        color: #c9d4e8;
        white-space: pre-wrap;
        word-break: break-word; /* formatting additions */ 
    }

    .msg-time {
        font-size: 0.66rem;
        color: #2a4060;
        margin-top: 0.3rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Suggestions row ──────────────────────────────────────────── */
    .suggestions-row {
        margin: 0.5rem 0 1rem 0;
        padding-top: 0.6rem;
        border-top: 1px solid #0f1e32;
    }

    /* ── Welcome / empty state ────────────────────────────────────── */
    .welcome-state, .empty-state {
        text-align: center;
        padding: 3.5rem 2rem;
        color: #2a4060;
    }

    .welcome-icon, .empty-icon {
        font-size: 2.8rem;
        margin-bottom: 0.8rem;
        display: block;
    }

    .welcome-state h2 {
        font-family: 'DM Serif Display', serif;
        font-size: 1.45rem;
        color: #3a5878;
        margin-bottom: 0.4rem;
    }

    .welcome-state p, .empty-state p {
        font-size: 0.88rem;
        color: #2a4060;
    }

    /* ── Typography ───────────────────────────────────────────────── */
    .page-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.9rem;
        color: #dce8f8;
        letter-spacing: -0.4px;
        margin: 0 0 0.15rem 0;
        line-height: 1.2;
    }

    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.25rem;
        color: #c9d4e8;
        margin: 1.4rem 0 0.7rem 0;
    }

    /* ── Active doc badge ─────────────────────────────────────────── */
    .active-doc-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: #091d38;
        border: 1px solid #143660;
        border-radius: 100px;
        padding: 0.22rem 0.7rem;
        font-size: 0.76rem;
        color: #4a80b0;
        margin-bottom: 0.7rem;
    }

    /* ── Document cards ───────────────────────────────────────────── */
    .doc-card {
        background: #0b1724;
        border: 1px solid #162840;
        border-radius: 11px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.7rem;
        transition: all 0.18s ease;
    }

    .doc-card:hover {
        border-color: #1e3c60;
        background: #0d1f38;
        transform: translateY(-2px);
        box-shadow: 0 5px 18px rgba(0,0,0,0.28);
    }

    .doc-card.active-card {
        border-color: #1e5090 !important;
        background: #091d3a !important;
    }

    .doc-card-name {
        font-weight: 600;
        font-size: 0.86rem;
        color: #c9d4e8;
        margin-bottom: 0.18rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .doc-card-date {
        font-size: 0.68rem;
        color: #2a4060;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.45rem;
    }

    .doc-card-preview {
        font-size: 0.78rem;
        color: #3a5878;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .doc-tags { margin-top: 0.45rem; display: flex; flex-wrap: wrap; gap: 0.28rem; }

    .doc-tag {
        background: #0d2440;
        border: 1px solid #163660;
        border-radius: 100px;
        padding: 0.08rem 0.5rem;
        font-size: 0.68rem;
        color: #4a7aab;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Inline document viewer ───────────────────────────────────── */
    .doc-viewer-header {
        font-size: 0.7rem;
        color: #2a4060;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .doc-meta {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        font-size: 0.7rem;
        color: #2a4060;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.5rem;
    }

    .doc-meta span {
        background: #0d1a2d;
        border: 1px solid #14243a;
        border-radius: 5px;
        padding: 0.1rem 0.45rem;
    }

    .doc-viewer {
        background: #080f1c;
        border: 1px solid #14243a;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        max-height: 240px;
        overflow-y: auto;
        font-size: 0.78rem;
        line-height: 1.7;
        color: #4a6880;
        font-family: 'JetBrains Mono', monospace;
        white-space: pre-wrap;
        word-break: break-word;
        margin-bottom: 0.8rem;
    }

    .doc-viewer::-webkit-scrollbar { width: 3px; }
    .doc-viewer::-webkit-scrollbar-thumb { background: #1e3050; border-radius: 6px; }

    /* ── Intent modal ─────────────────────────────────────────────── */
    .intent-modal {
        background: linear-gradient(145deg, #0b1928, #0e2244);
        border: 1px solid #1a3a60;
        border-radius: 18px;
        padding: 2.5rem 2rem 2rem 2rem;
        margin: 2rem auto;
        max-width: 680px;
        box-shadow: 0 24px 60px rgba(0,0,0,0.55);
    }

    .intent-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        color: #e2eaf8;
        margin-bottom: 0.35rem;
    }

    .intent-subtitle {
        font-size: 0.86rem;
        color: #3a5878;
        margin-bottom: 1.6rem;
    }

    .intent-option {
        background: #091828;
        border: 1px solid #142e50;
        border-radius: 11px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.16s ease;
    }

    .intent-option:hover { border-color: #1e4a80; background: #0d2444; }
    .intent-option-icon  { font-size: 1.3rem; margin-bottom: 0.25rem; }
    .intent-option-label { font-weight: 600; font-size: 0.86rem; color: #c9d4e8; }
    .intent-option-desc  { font-size: 0.74rem; color: #3a5878; margin-top: 0.15rem; }

    /* ── Misc ─────────────────────────────────────────────────────── */
    hr { border-color: #142030 !important; }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        font-family: 'DM Serif Display', serif;
        color: #c9d4e8;
    }

    [data-testid="stMultiSelect"] > div {
        background: #0a1624 !important;
        border: 1px solid #14243a !important;
        border-radius: 9px !important;
    }

    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #080d14; }
    ::-webkit-scrollbar-thumb { background: #142030; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #1e3050; }
    </style>

    <script>
    (function keepSidebarOpen() {
        function forceOpen() {
            var doc = window.parent ? window.parent.document : document;
            var sb = doc.querySelector('[data-testid="stSidebar"]');
            if (sb) {
                sb.style.cssText += ';transform:none!important;visibility:visible!important;opacity:1!important;display:flex!important;width:260px!important;min-width:260px!important;';
                sb.setAttribute('aria-expanded', 'true');
            }
            doc.querySelectorAll('[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"]')
               .forEach(function(el){ el.style.display = 'none'; });
        }
        forceOpen();
        setTimeout(forceOpen, 200);
        setTimeout(forceOpen, 600);
    })();
    </script>
    """, unsafe_allow_html=True)


def render_doc_viewer(doc: dict):
    """Render a clean inline document preview — content is HTML-escaped so no markup bleeds through."""
    content = doc.get("content", "")
    name = doc.get("name", "")
    is_url = name.startswith("http")
    ext = name.rsplit(".", 1)[-1].upper() if "." in name and not is_url else "URL"

    word_count = len(content.split())
    char_count = len(content)
    line_count = content.count("\n") + 1
    icon = "🌐" if is_url else "📄"

    st.markdown(
        f'<div class="doc-viewer-header">📖 Document preview</div>'
        f'<div class="doc-meta">'
        f'<span>{icon} {ext}</span>'
        f'<span>{word_count:,} words</span>'
        f'<span>{line_count:,} lines</span>'
        f'<span>{char_count:,} chars</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    # HTML-escape document content so any tags inside render as plain text
    safe = (
        content[:3000]
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    suffix = "\n\n… (preview truncated)" if len(content) > 3000 else ""
    st.markdown(f'<div class="doc-viewer">{safe}{suffix}</div>', unsafe_allow_html=True)


# ── Intent options ─────────────────────────────────────────────────────────
INTENT_OPTIONS = [
    {"id": "summarize",   "icon": "📋", "label": "Summarize",      "desc": "Clean bullet-point summary",         "mode": "Summarize"},
    {"id": "study_sheet", "icon": "📚", "label": "Study Sheet",    "desc": "Key concepts, terms & structure",    "mode": "Study Sheet"},
    {"id": "key_terms",   "icon": "🔑", "label": "Key Terms",      "desc": "Extract and define key terms",       "mode": "Key Terms"},
    {"id": "explain",     "icon": "💡", "label": "Explain Simply", "desc": "Plain-language breakdown",           "mode": "Explain Simple"},
    {"id": "flashcards",  "icon": "🃏", "label": "Flashcards",     "desc": "Q&A cards for memorization",         "mode": "Flashcards"},
    {"id": "chat",        "icon": "💬", "label": "Just Chat",      "desc": "Ask questions freely about the doc", "mode": "Chat"},
]


def render_upload_intent_modal(text_reader):
    upload_type, upload_data = st.session_state.pending_upload

    st.markdown(f"""
    <div class="intent-modal">
        <div class="intent-title">What would you like to do?</div>
        <div class="intent-subtitle">
            <strong>{st.session_state.pending_upload_name[:60]}</strong> is ready —
            choose a starting action below.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, opt in enumerate(INTENT_OPTIONS):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="intent-option">
                <div class="intent-option-icon">{opt['icon']}</div>
                <div class="intent-option-label">{opt['label']}</div>
                <div class="intent-option-desc">{opt['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(opt["label"], key=f"intent_{opt['id']}", use_container_width=True):
                if upload_type == "file":
                    text = text_reader.extract_from_upload(upload_data)
                else:
                    text = text_reader.extract_from_url(upload_data)

                doc_entry = {
                    "name": st.session_state.pending_upload_name,
                    "content": text,
                    "tags": [],
                    "uploaded": datetime.now().strftime("%b %d, %H:%M"),
                    "summary": ""
                }
                st.session_state.documents.append(doc_entry)
                # ← CHANGED: was `st.session_state.current_doc_index = len(...) - 1`
                # Now adds the new doc's index into the selection set instead of replacing a single index
                new_idx = len(st.session_state.documents) - 1
                st.session_state.selected_doc_indices = {new_idx}

                st.session_state.analysis_mode = opt["mode"]

                if opt["id"] != "chat":
                    prompt = build_prompt(opt["mode"], text)
                    with st.spinner(f"Running {opt['label']}…"):
                        result = generate_response(prompt)
                    st.session_state.chats[st.session_state.active_chat]["messages"].append({
                        "role": "assistant",
                        "content": result,
                        "time": datetime.now().strftime("%H:%M")
                    })
                    st.session_state.documents[-1]["summary"] = result[:300]
                else:
                    st.session_state.chats[st.session_state.active_chat]["messages"].append({
                        "role": "assistant",
                        "content": f"📄 **{st.session_state.pending_upload_name}** loaded and ready. Ask me anything!",
                        "time": datetime.now().strftime("%H:%M")
                    })

                st.session_state.pending_upload = None
                st.session_state.pending_upload_name = ""
                st.session_state.show_intent_modal = False
                st.session_state.uploader_key += 1
                st.session_state.active_tab = "chat"
                st.rerun()

    st.markdown("---")
    if st.button("✕  Cancel", key="intent_cancel"):
        st.session_state.pending_upload = None
        st.session_state.pending_upload_name = ""
        st.session_state.show_intent_modal = False
        st.session_state.uploader_key += 1
        st.rerun()
import streamlit as st
from datetime import datetime
from main import generate_response
from text_reader import TextReader
from prompts import build_prompt, get_smart_suggestions
from ui_components import apply_custom_styles, render_upload_intent_modal, render_doc_viewer

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config( #page title, icon, & layout
    page_title="Scholar — AI Study Assistant",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

text_reader = TextReader()#text reader for applying
apply_custom_styles()

# ── Session state ──────────────────────────────────────────────────────────────
def init_state():#App memory for every script rerun from user interaction
    defaults = {
        "chats": {"Session 1": {"messages": [], "tags": [], "created": datetime.now().strftime("%b %d")}},
        "active_chat": "Session 1",
        "documents": [],
        "current_doc_index": None,
        "analysis_mode": "Chat",
        "pending_upload": None,
        "pending_upload_name": "",
        "show_intent_modal": False,
        "search_query": "",
        "active_tab": "chat",
        "doc_filter_tag": None,
        "uploader_key": 0,
        "show_doc_preview": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Helpers ────────────────────────────────────────────────────────────────────
def active_messages():#utility functions for fetching message list
    #adding new messages to the list (user and assisstant) with timestamp,
    #and the fetching text content from a chosen doc
    return st.session_state.chats[st.session_state.active_chat]["messages"]

def push_message(role, content):
    active_messages().append({
        "role": role,
        "content": content,
        "time": datetime.now().strftime("%H:%M")
    })

def current_document():
    idx = st.session_state.current_doc_index
    if idx is not None and idx < len(st.session_state.documents):
        return st.session_state.documents[idx]["content"]
    return None

# ── Intent modal (full-page takeover) ─────────────────────────────────────────
if st.session_state.show_intent_modal and st.session_state.pending_upload is not None:
    render_upload_intent_modal(text_reader)#user option popup before re-rendering app for a upload + text extraction
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR  — st.sidebar is natively fixed/sticky in Streamlit
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
        <div class="nav-logo">Scholar</div>
        <div class="nav-tagline">AI Study Assistant</div>
    """, unsafe_allow_html=True)

    # ── Navigate ───────────────────────────────────────────────────────────
    #Navigating sidebar menu, changing active tab for "chat" and "library"
    st.markdown('<div class="nav-section-label">Navigate</div>', unsafe_allow_html=True)
    if st.button("💬  Chat", key="nav_chat", use_container_width=True,
                 type="primary" if st.session_state.active_tab == "chat" else "secondary"):
        st.session_state.active_tab = "chat"
        st.rerun()
    if st.button("📁  Library", key="nav_lib", use_container_width=True,
                 type="primary" if st.session_state.active_tab == "library" else "secondary"):
        st.session_state.active_tab = "library"
        st.rerun()

    # ── Upload ─────────────────────────────────────────────────────────────
    #Drag-&-drop file types + url paste boxes, changes app state if new content is uploaded
    st.markdown('<div class="nav-section-label">Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop a file",
        type=["txt", "pdf", "docx"],
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )
    url_input = st.text_input(
        "url", placeholder="Paste a URL…",
        label_visibility="collapsed",
        key="url_nav"
    )
#restrictions on uploading same doc

    if uploaded_file and not any(d["name"] == uploaded_file.name for d in st.session_state.documents):
        st.session_state.pending_upload = ("file", uploaded_file)
        st.session_state.pending_upload_name = uploaded_file.name
        st.session_state.show_intent_modal = True
        st.rerun()
#restrictions on pasting non-valid url
    if (url_input and url_input.startswith("http")
            and not any(d["name"] == url_input for d in st.session_state.documents)):
        st.session_state.pending_upload = ("url", url_input)
        st.session_state.pending_upload_name = url_input
        st.session_state.show_intent_modal = True
        st.rerun()

    # ── Sessions ───────────────────────────────────────────────────────────
    st.markdown('<div class="nav-section-label">Sessions</div>', unsafe_allow_html=True)
    #default active_chat inside 1st session
    if st.button("＋  New session", use_container_width=True):
        name = f"Session {len(st.session_state.chats) + 1}"
        st.session_state.chats[name] = {
            "messages": [], "tags": [], "created": datetime.now().strftime("%b %d")
        }
        st.session_state.active_chat = name
        st.session_state.active_tab = "chat"
        st.rerun()
    #app state changes- active chat- when user interacts with session buttons
    for chat_name in list(st.session_state.chats.keys()):
        is_active = chat_name == st.session_state.active_chat
        n_msgs = len(st.session_state.chats[chat_name]["messages"])
        label = f"{'▸ ' if is_active else ''}{chat_name}  ·  {n_msgs}"
        if st.button(label, key=f"sess_{chat_name}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_chat = chat_name
            st.session_state.active_tab = "chat"
            st.rerun()

    #app state changes- deleting sessions except 1st
    if len(st.session_state.chats) > 1:
        if st.button("🗑  Delete session", use_container_width=True):
            del st.session_state.chats[st.session_state.active_chat]
            st.session_state.active_chat = list(st.session_state.chats.keys())[0]
            st.rerun()

    # ── Documents quick-list ────────────────────────────────────────────────
    if st.session_state.documents:
        st.markdown('<div class="nav-section-label">Documents</div>', unsafe_allow_html=True)
        #Documents uploaded list with a mark to signify activation for chat
        for i, doc in enumerate(st.session_state.documents):
            is_active = st.session_state.current_doc_index == i
            icon = "✓ " if is_active else "· "
            short = doc["name"][:22] + ("…" if len(doc["name"]) > 22 else "")
            if st.button(icon + short, key=f"sb_doc_{i}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.current_doc_index = i
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── LIBRARY ────────────────────────────────────────────────────────────────
if st.session_state.active_tab == "library":
    st.markdown('<h1 class="page-title">Document Library</h1>', unsafe_allow_html=True)


    search = st.text_input(
        "search", placeholder="Search by title, content, or tag…",
        label_visibility="collapsed", value=st.session_state.search_query
    )
    #Searching docs with either doc name, first 500 chars, or tags----
    st.session_state.search_query = search

    docs = st.session_state.documents
    if search:
        docs = [d for d in docs if
                search.lower() in d["name"].lower() or
                search.lower() in d.get("content", "")[:500].lower() or
                any(search.lower() in t.lower() for t in d.get("tags", []))]

    if not docs:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📄</div>
            <p>No documents yet — upload a file or paste a URL on the left.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        all_tags = sorted({t for d in st.session_state.documents for t in d.get("tags", [])})
        if all_tags:
            pill_cols = st.columns(min(len(all_tags) + 1, 8))
            with pill_cols[0]:
                if st.button("All", key="tag_all"):
                    st.session_state.doc_filter_tag = None
                    st.rerun()
            for i, tag in enumerate(all_tags[:7]):
                with pill_cols[i + 1]:
                    if st.button(f"#{tag}", key=f"tag_{tag}"):
                        st.session_state.doc_filter_tag = tag
                        st.rerun()

        if st.session_state.doc_filter_tag:
            docs = [d for d in docs if st.session_state.doc_filter_tag in d.get("tags", [])]
#-----
#filtered docs organized into 3 columns with doc name, upload date, content preview, & tags ---
        grid = st.columns(3)
        for i, doc in enumerate(docs):
            real_idx = st.session_state.documents.index(doc)
            with grid[i % 3]:
                is_active = st.session_state.current_doc_index == real_idx
                card_class = "doc-card active-card" if is_active else "doc-card"
                preview = doc.get("content", "")[:180].replace("\n", " ")
                tags_html = " ".join(f'<span class="doc-tag">#{t}</span>' for t in doc.get("tags", []))
                icon = "🌐" if doc["name"].startswith("http") else "📄"
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="doc-card-name">{icon} {doc['name'][:38]}</div>
                    <div class="doc-card-date">{doc.get('uploaded','')}</div>
                    <div class="doc-card-preview">{preview}…</div>
                    <div class="doc-tags">{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("✓ Active" if is_active else "Use",
                                 key=f"use_doc_{real_idx}", use_container_width=True):
                        st.session_state.current_doc_index = real_idx
                        st.session_state.active_tab = "chat"
                        st.rerun()
                with b2:
                    if st.button("🗑", key=f"del_doc_{real_idx}", use_container_width=True):
                        st.session_state.documents.pop(real_idx)
                        if st.session_state.current_doc_index == real_idx:
                            st.session_state.current_doc_index = None
                        st.rerun()
#----
                # ── Instant tag via on_change ──────────────────────────────
                def _add_tag(idx=real_idx):
                    val = st.session_state.get(f"tag_input_{idx}", "").strip()
                    if val and val not in st.session_state.documents[idx].get("tags", []):
                        st.session_state.documents[idx].setdefault("tags", []).append(val)

                st.text_input(
                    "tag",
                    key=f"tag_input_{real_idx}",
                    placeholder="Add tag & press Enter…",
                    label_visibility="collapsed",
                    on_change=_add_tag, #Executes on enter via reading input value from session state key
                )
#----
                
                # Show live pills immediately — reflects state without extra interaction
                live_tags = st.session_state.documents[real_idx].get("tags", [])
                if live_tags:
                    pills = " ".join(f'<span class="doc-tag">#{t}</span>' for t in live_tags)
                    st.markdown(f'<div class="doc-tags" style="margin-top:0.3rem">{pills}</div>',
                                unsafe_allow_html=True)
#Find connections for min 2 selected docs and sends content to AI based on selected button prompts, pushed to active chat
    if len(st.session_state.documents) >= 2:
        st.markdown("---")
        st.markdown('<h2 class="section-title">🔗 Find Connections</h2>', unsafe_allow_html=True)
        selected = st.multiselect(
            "Select documents to compare",
            options=[d["name"] for d in st.session_state.documents],
            default=[d["name"] for d in st.session_state.documents[:2]]
        )
        if st.button("✨ Analyze Connections", type="primary") and len(selected) >= 2:
            selected_docs = [d for d in st.session_state.documents if d["name"] in selected]
            combined = "\n\n---\n\n".join(
                f"DOCUMENT: {d['name']}\n{d['content'][:2000]}" for d in selected_docs
            )
            prompt = f"""You are an academic research assistant. Analyze these documents:
1. Shared themes and concepts
2. Contradictions or differences in perspective
3. How they could be cited together
4. A synthesis of the main argument across all documents

Documents:
{combined}"""
            with st.spinner("Analyzing…"):
                result = generate_response(prompt)
            push_message("assistant", f"**Connection Analysis: {', '.join(selected)}**\n\n{result}")
            st.session_state.active_tab = "chat"
            st.rerun()

# ── CHAT ───────────────────────────────────────────────────────────────────
else:
    active_doc = None
    if st.session_state.current_doc_index is not None:
        idx = st.session_state.current_doc_index
        if idx < len(st.session_state.documents):
            active_doc = st.session_state.documents[idx]

    # ── Session tabs — single row of clickable buttons only ────────────────
    #session tabs on top and side for switching
    chat_names = list(st.session_state.chats.keys())
    if chat_names:
        tab_cols = st.columns(min(len(chat_names), 8))
        for i, name in enumerate(chat_names[:8]):
            is_active = name == st.session_state.active_chat
            n = len(st.session_state.chats[name]["messages"])
            with tab_cols[i]:
                if st.button(
                    f"{name} · {n}",
                    key=f"tab_{name}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state.active_chat = name
                    st.rerun()

    # ── Header row ──────────────────────────────────────────────────────────
    #Chat session and mode in heading and active doc marking
    hdr, mode_sel = st.columns([3, 1])
    with hdr:
        st.markdown(
            f'<h1 class="page-title">{st.session_state.active_chat}</h1>',
            unsafe_allow_html=True
        )
        if active_doc:
            st.markdown(
                f'<div class="active-doc-badge">📄 {active_doc["name"][:50]}</div>',
                unsafe_allow_html=True
            )
    with mode_sel:
        st.session_state.analysis_mode = st.selectbox(
            "Mode",
            ["Chat", "Summarize", "Study Sheet", "Key Terms", "Explain Simple", "Flashcards"],
            label_visibility="collapsed"
        )

    # ── Collapsible document preview ────────────────────────────────────────
    if active_doc:
        toggle_label = "🔼 Hide document" if st.session_state.show_doc_preview else "🔽 View document"
        if st.button(toggle_label, key="toggle_doc_preview"):
            st.session_state.show_doc_preview = not st.session_state.show_doc_preview
            st.rerun()
        if st.session_state.show_doc_preview:
            render_doc_viewer(active_doc)

    # ── Scrollable messages container ────────────────────────────────────────
    messages = active_messages()

    st.markdown('<div class="chat-scroll-box">', unsafe_allow_html=True)

    if not messages:
        st.markdown("""
        <div class="welcome-state">
            <div class="welcome-icon">📖</div>
            <h2>Ready to study?</h2>
            <p>Upload a document on the left, or just start chatting.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        msgs_html = ""
        for msg in messages:
            role_class = "user-msg" if msg["role"] == "user" else "assistant-msg"
            avatar = "🧑‍🎓" if msg["role"] == "user" else "🎓"
            safe_content = (msg["content"]
                            .replace("&", "&amp;")
                            .replace("<", "&lt;")
                            .replace(">", "&gt;"))
            msgs_html += f"""
            <div class="msg-wrapper {role_class}">
                <div class="msg-avatar">{avatar}</div>
                <div class="msg-bubble">
                    <div class="msg-content">{safe_content}</div>
                    <div class="msg-time">{msg.get('time','')}</div>
                </div>
            </div>"""
        st.markdown(msgs_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # /chat-scroll-box

    # ── Smart suggestions ────────────────────────────────────────────────────
    last_assistant = next((m for m in reversed(messages) if m["role"] == "assistant"), None)
    if last_assistant:
        suggestions = get_smart_suggestions(st.session_state.analysis_mode, last_assistant["content"])
        st.markdown('<div class="suggestions-row">', unsafe_allow_html=True)
        sug_cols = st.columns(len(suggestions))
        for i, sug in enumerate(suggestions):
            with sug_cols[i]:
                if st.button(sug, key=f"sug_{i}_{len(messages)}", use_container_width=True):
                    push_message("user", sug)
                    doc_text = current_document()
                    prompt = build_prompt(st.session_state.analysis_mode, doc_text, sug) if doc_text else sug
                    with st.spinner(""):
                        response = generate_response(prompt)
                    push_message("assistant", response)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Chat input ───────────────────────────────────────────────────────────
    user_input = st.chat_input("Ask anything about your document…")
    if user_input:
        push_message("user", user_input)
        doc_text = current_document()
        if st.session_state.analysis_mode != "Chat" and doc_text:
            prompt = build_prompt(st.session_state.analysis_mode, doc_text, user_input)
        elif doc_text:
            prompt = build_prompt("Chat", doc_text, user_input)
        else:
            prompt = user_input
        with st.spinner("Thinking…"):
            response = generate_response(prompt)
        push_message("assistant", response)
        st.rerun()
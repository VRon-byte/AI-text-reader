import re

# ── Core prompt builder ───────────────────────────────────────────────────────
# ← CHANGED: signature now accepts `documents` dict {name: content} for multi-doc support
# `document` (single string) kept for backwards compatibility
def build_prompt(mode: str, document: str = None, user_input: str = None, documents: dict = None) -> str:
    # ← NEW: build a unified doc_block and a flag for whether we're in multi-doc mode
    if documents and len(documents) > 1:
        # Multiple docs: cap each at 2000 chars to avoid hitting token limits
        doc_block = "\n\n---\n\n".join(
            f"[Document: {name}]\n{content[:2000]}"   # ← NEW: 2000 char cap per doc in multi mode
            for name, content in documents.items()
        )
        multi = True
    else:
        # Single doc path — works the same as before
        if documents:
            name, content = next(iter(documents.items()))
            doc_block = content[:5000]
        else:
            doc_block = (document or "")[:5000]  # ← original fallback, unchanged
        multi = False
    if mode == "Summarize":
        # ← CHANGED: multi-doc version summarizes each doc separately then synthesizes
        if multi:
          return f"""You are an expert academic summarizer. Summarize the following document for a college student.

Format your response with:
- **TL;DR** (Don't actually add in the letters TL;DR) (2-3 sentences)
- **Main Points** (bullet list)
Then end with:
## Combined Synthesis
- Shared themes
- Key differences
- Overall takeaway

Documents:
{doc_block}"""
        else:
            # ← UNCHANGED from original
            return f"""You are an expert academic summarizer. Summarize the following document for a college student.

Format your response with:
- **TL;DR** (Don't actually add in the letters TL;DR)(2-3 sentences)
- **Main Points** (bullet list)
- **Key Takeaways** (3-5 items)
- **Questions to Consider** (2-3 prompts)

Document:
{doc_block}"""
    elif mode == "Study Sheet":
        return f"""Create a comprehensive study guide for a college student based on this document.

Structure it as:
# Study Guide

## Core Concepts
[List major concepts with brief explanations]

## Key Definitions
[Term: Definition format]

## Important Relationships
[How concepts connect]

## Summary
[2-3 paragraph overview]

## Potential Exam Questions
[5 likely exam questions with answers]

Document:
{doc_block}"""

    elif mode == "Key Terms":
        # ← CHANGED: multi mode asks the model to note which doc each term came from
        return f"""Extract and define all important terms, concepts, names, and theories from {"these documents" if multi else "this document"}.

Format each as:
**Term** — Clear, concise definition. Explain why it matters in context.{"Note which document(s) use this term." if multi else ""}

Group related terms together under headings if possible.

Document:
{doc_block}"""

    elif mode == "Explain Simple":
        # ← CHANGED: multi mode asks for per-doc explanation then a comparison
        return f"""Explain {"these documents" if multi else "this document"} as if talking to someone encountering the topic for the first time.

Use:
- Simple everyday language (no jargon without explanation)
- Analogies and real-world examples
- Short sentences
- A friendly, encouraging tone
{"- Explain each document separately, then briefly compare them" if multi else ""}

Document:
{doc_block}"""

    elif mode == "Flashcards":
        # ← CHANGED: multi mode adds cross-document comparison cards
        return f"""Create 10-15 flashcard-style Q&A pairs from {"these documents" if multi else "this document"}.
Format each as:
**Q:** [Question]
**A:** [Concise answer]

Focus on: definitions, key facts, cause-effect relationships, and important dates/names.
{"Also include 2-3 cards that ask about differences or connections between the documents." if multi else ""}

Document:
{doc_block}"""

    elif mode == "Chat":
        if user_input:
            # ← CHANGED: source_note adapts to single vs multi
            source_note = "the documents below" if multi else "the document below"
            name_note = " When referencing specific information, name the document it came from." if multi else ""
            return f"""You are a helpful academic assistant. Answer the student's question using ONLY the information in {source_note}.

If the answer isn't in the document(s), say so clearly.{name_note} Be concise but thorough.

Document:
{doc_block}

Student's Question:
{user_input}"""
        else:
            # ← CHANGED: plural "documents" in multi mode
            return f"Here {'are the documents' if multi else 'is the document'} to reference:\n\n{doc_block}"

    elif mode == "Connections":
        return user_input or ""

    else:
        if doc_block and user_input:
            return f"Document:\n{doc_block}\n\nQuestion: {user_input}"
        return user_input or doc_block


# ── Smart post-response suggestions ──────────────────────────────────────────
_SUGGESTIONS = {
    "Summarize": [
        "🃏 Turn this into flashcards",
        "🔑 Extract key terms",
        "❓ Quiz me on this",
        "📊 Create a study sheet",
    ],
    "Study Sheet": [
        "🃏 Make flashcards from this",
        "🤔 Explain the hardest concept",
        "❓ Give me practice questions",
        "🔗 What are the connections?",
    ],
    "Key Terms": [
        "📋 Summarize the document",
        "🃏 Turn terms into flashcards",
        "💡 Explain these simply",
        "❓ Quiz me on these terms",
    ],
    "Explain Simple": [
        "📋 Give me a full summary",
        "🔑 What are the key terms?",
        "❓ Ask me a question about this",
        "📊 Build a study sheet",
    ],
    "Flashcards": [
        "📋 Summarize the document",
        "❓ Quiz me verbally",
        "🔑 Show key terms",
        "📊 Make a study sheet",
    ],
    "Chat": [
        "📋 Summarize this document",
        "🃏 Make flashcards",
        "🔑 List key terms",
        "💡 Explain it simply",
    ],
}

_FALLBACK_SUGGESTIONS = [
    "📋 Summarize this",
    "🃏 Make flashcards",
    "🔑 Key terms",
    "❓ Quiz me",
]

def get_smart_suggestions(mode: str, last_response: str = "") -> list[str]:
    """
    Returns 4 context-aware suggestion buttons based on current mode
    and optionally the content of the last response.
    """
    base = _SUGGESTIONS.get(mode, _FALLBACK_SUGGESTIONS)

    # Content-aware adjustments
    if last_response:
        low = last_response.lower()
        overrides = []

        if "error" in low or "cannot" in low or "don't have" in low:
            overrides = [
                "📂 Switch to a different document",
                "💬 Ask a different question",
                "📋 Summarize what's available",
                "🔑 List key terms instead",
            ]
            return overrides

        if any(w in low for w in ["theory", "hypothesis", "argument", "claim"]):
            return [
                "🔍 Find evidence for this",
                "⚖️ What are counter-arguments?",
                "📋 Summarize this theory",
                "🃏 Make flashcards on this topic",
            ]

        if any(w in low for w in ["experiment", "study", "research", "data", "results"]):
            return [
                "📊 What were the key findings?",
                "🔬 Explain the methodology",
                "🃏 Flashcard the results",
                "🔗 How does this connect to other documents?",
            ]

    return base
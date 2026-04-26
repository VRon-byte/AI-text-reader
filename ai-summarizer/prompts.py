import re

# ── Core prompt builder ───────────────────────────────────────────────────────
def build_prompt(mode: str, document: str = None, user_input: str = None) -> str:
    doc = (document or "")[:5000]

    if mode == "Summarize":
        return f"""You are an expert academic summarizer. Summarize the following document for a college student.

Format your response with:
- **TL;DR** (2-3 sentences)
- **Main Points** (bullet list)
- **Key Takeaways** (3-5 items)
- **Questions to Consider** (2-3 prompts)

Document:
{doc}"""

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
{doc}"""

    elif mode == "Key Terms":
        return f"""Extract and define all important terms, concepts, names, and theories from this document.

Format each as:
**Term** — Clear, concise definition. Explain why it matters in context.

Group related terms together under headings if possible.

Document:
{doc}"""

    elif mode == "Explain Simple":
        return f"""Explain this document as if talking to someone encountering the topic for the first time.

Use:
- Simple everyday language (no jargon without explanation)
- Analogies and real-world examples
- Short sentences
- A friendly, encouraging tone

Document:
{doc}"""

    elif mode == "Flashcards":
        return f"""Create 10-15 flashcard-style Q&A pairs from this document.

Format each as:
**Q:** [Question]
**A:** [Concise answer]

Focus on: definitions, key facts, cause-effect relationships, and important dates/names.

Document:
{doc}"""

    elif mode == "Chat":
        if user_input:
            return f"""You are a helpful academic assistant. Answer the student's question using ONLY the information in the document below.

If the answer isn't in the document, say so clearly. Be concise but thorough.

Document:
{doc}

Student's Question:
{user_input}"""
        else:
            return f"Here is the document to reference:\n\n{doc}"

    elif mode == "Connections":
        return user_input or ""

    else:
        if doc and user_input:
            return f"Document:\n{doc}\n\nQuestion: {user_input}"
        return user_input or doc


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
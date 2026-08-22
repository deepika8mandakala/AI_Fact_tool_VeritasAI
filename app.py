import sys
from pathlib import Path

import gradio as gr


# ============================================================
# PROJECT PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# VERITASAI PIPELINE
# ============================================================

from app.verification.pipeline import verify_pipeline


# ============================================================
# CLAIM VERIFICATION
# ============================================================

def verify_claim(claim, top_k):

    if not claim or not claim.strip():

        return (
            "⚠️ Please enter a claim.",
            "No claim was provided.",
            "",
            ""
        )

    try:

        result = verify_pipeline(
            claim.strip(),
            int(top_k)
        )

        summary = result.get(
            "summary",
            {}
        )

        verdict = summary.get(
            "final_verdict",
            "INSUFFICIENT_EVIDENCE"
        )

        confidence = float(
            summary.get(
                "confidence",
                0.0
            )
        )

        explanation = result.get(
            "explanation",
            "No explanation generated."
        )

        reasoning = result.get(
            "reasoning",
            []
        )

        evidence_results = result.get(
            "results",
            []
        )

        # ----------------------------------------------------
        # Verdict
        # ----------------------------------------------------

        if verdict == "SUPPORTED":

            verdict_display = "🟢 SUPPORTED"

        elif verdict == "CONTRADICTED":

            verdict_display = "🔴 CONTRADICTED"

        else:

            verdict_display = (
                "🟡 INSUFFICIENT EVIDENCE"
            )

        verdict_text = (
            f"{verdict_display}\n\n"
            f"Confidence: {confidence:.2%}"
        )

        # ----------------------------------------------------
        # Reasoning
        # ----------------------------------------------------

        if reasoning:

            reasoning_text = "\n".join(
                f"• {item}"
                for item in reasoning
            )

        else:

            reasoning_text = (
                "No additional reasoning available."
            )

        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        evidence_text = ""

        for i, item in enumerate(
            evidence_results[:5],
            start=1
        ):

            document = item.get(
                "document",
                {}
            )

            title = document.get(
                "title",
                "Unknown"
            )

            source = document.get(
                "source",
                "Unknown"
            )

            chunk = document.get(
                "chunk_text",
                ""
            )

            score = item.get(
                "confidence",
                item.get(
                    "relevance_score",
                    0
                )
            )

            evidence_text += (
                f"### Evidence {i}\n\n"
                f"**Title:** {title}\n\n"
                f"**Source:** {source}\n\n"
                f"**Score:** {score}\n\n"
                f"{chunk}\n\n"
                f"---\n\n"
            )

        if not evidence_text:

            evidence_text = (
                "No evidence was available."
            )

        return (
            verdict_text,
            explanation,
            reasoning_text,
            evidence_text
        )

    except Exception as exc:

        print(
            "VERITASAI ERROR:",
            type(exc).__name__,
            str(exc)
        )

        return (
            "❌ Verification Error",
            str(exc),
            "The verification pipeline encountered an error.",
            ""
        )


# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(
    title="VeritasAI"
) as demo:

    gr.Markdown(
        """
# 🛡️ VeritasAI

### AI-Powered Claim Verification & Live Misinformation Detection

Verify potentially misleading claims using:

**BGE Embeddings → FAISS Retrieval → DeBERTa NLI → Verdict → Groq Explanation**
"""
    )

    with gr.Row():

        with gr.Column():

            claim_input = gr.Textbox(
                label="Claim",
                placeholder=(
                    "Enter a factual claim to verify..."
                ),
                lines=4
            )

            top_k = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="Number of Evidence Results"
            )

            verify_button = gr.Button(
                "🔍 Verify Claim",
                variant="primary"
            )

        with gr.Column():

            verdict_output = gr.Textbox(
                label="Verification Verdict",
                lines=3
            )

            explanation_output = gr.Markdown(
                label="AI Explanation"
            )

    reasoning_output = gr.Markdown(
        label="Reasoning"
    )

    evidence_output = gr.Markdown(
        label="Retrieved Evidence"
    )

    verify_button.click(
        fn=verify_claim,
        inputs=[
            claim_input,
            top_k
        ],
        outputs=[
            verdict_output,
            explanation_output,
            reasoning_output,
            evidence_output
        ]
    )

    gr.Markdown(
        """
---

### Verification Pipeline

`Claim`
→ `BGE Embedding`
→ `FAISS Evidence Retrieval`
→ `Evidence Filtering`
→ `DeBERTa NLI`
→ `Verdict + Confidence`
→ `Groq Explanation`

**Evidence retrieval and NLI determine the verification result. Groq is used for the human-readable explanation.**
"""
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
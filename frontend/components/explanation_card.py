import streamlit as st


def show_explanation(result):

    reasoning = result.get(
        "reasoning",
        []
    )

    explanation = result.get(
        "explanation",
        "No explanation was provided."
    )

    # =====================================================
    # AI Reasoning
    # =====================================================

    st.markdown("### 🤖 AI Reasoning")

    if reasoning:

        for reason in reasoning:

            st.info(
                f"• {reason}"
            )

    else:

        st.info(
            "No additional reasoning was provided."
        )

    # =====================================================
    # AI Explanation
    # =====================================================

    st.markdown("### 💡 AI Explanation")

    st.write(
        explanation
    )
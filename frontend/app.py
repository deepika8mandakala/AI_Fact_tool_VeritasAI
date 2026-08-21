import streamlit as st

from components.analytics import (
    show_analytics
)

from components.single_verification import (
    show_single_verification
)

from components.history import (
    show_history
)

from components.confidence_chart import (
    show_confidence_chart
)


st.set_page_config(
    page_title="VeritasAI",
    page_icon="🛡️",
    layout="wide",
)


st.title(
    "🛡️ VeritasAI"
)

st.caption(
    "AI-powered claim verification and live misinformation monitoring"
)


show_analytics()

st.markdown("---")

show_single_verification()

st.markdown("---")

confidence = show_history()

show_confidence_chart(
    confidence
)
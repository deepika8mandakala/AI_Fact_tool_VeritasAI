import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    get_history,
    clear_history
)
from components.history import (
    show_history
)
from components.confidence_chart import (
    show_confidence_chart
)

from components.analytics import show_analytics
from components.single_verification import show_single_verification
from components.batch_verification import (
    show_batch_verification
)
st.set_page_config(
    page_title="VeritasAI",
    layout="wide"
)

st.title("🛡️ VeritasAI")
stats = show_analytics()
show_single_verification()

show_batch_verification()
confidence = show_history()
show_confidence_chart(
    confidence
)
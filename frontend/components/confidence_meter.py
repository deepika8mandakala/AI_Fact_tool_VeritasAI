import streamlit as st

def confidence_meter(conf):

    st.subheader("Confidence")

    st.progress(conf)

    st.write(f"{conf*100:.1f}%")
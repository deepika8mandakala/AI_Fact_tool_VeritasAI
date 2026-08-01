import streamlit as st


def show_explanation(result):

    st.header("🤖 AI Reasoning")

    for reason in result["reasoning"]:
        st.success(reason)

    st.markdown("---")

    st.subheader("AI Explanation")

    st.info(result["explanation"])
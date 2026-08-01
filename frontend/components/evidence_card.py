import streamlit as st

def show_evidence(results):

    st.header("📚 Evidence")

    for i, evidence in enumerate(results):

        doc = evidence["document"]

        with st.expander(f"Evidence {i+1}"):

            st.markdown(f"### {doc['title']}")

            c1, c2 = st.columns(2)

            with c1:

                st.write("**Source**")
                st.write(doc["source"])

                st.write("**Published**")
                st.write(doc.get("published_at", "N/A"))

                st.write("**Verdict**")
                st.write(evidence["verdict"])

            with c2:

                st.metric(
                    "Confidence",
                    f"{evidence['confidence']*100:.1f}%"
                )

                st.metric(
                    "Retrieval",
                    f"{evidence['retrieval_score']:.3f}"
                )

                st.metric(
                    "Credibility",
                    f"{evidence['source_score']:.2f}"
                )

            st.info(evidence["highlight"])

            if doc.get("url"):
                st.link_button(
                    "🔗 Open Original Article",
                    doc["url"]
                )
import streamlit as st

from utils import (
    verify_claim,
    verify_social_post,
    start_live_monitor,
    stop_live_monitor,
    get_live_status,
    get_live_results,
)

from components.verdict_card import show_verdict
from components.metrics import show_metrics
from components.explanation_card import show_explanation
from components.evidence_card import show_evidence_card


# =========================================================
# NORMAL VERIFICATION RESULT
# =========================================================

def display_verification_result(verification):

    summary = verification.get(
        "summary",
        {}
    )

    show_verdict(summary)

    show_metrics(verification)

    show_explanation(verification)

    evidence = verification.get(
        "results",
        []
    )

    st.markdown("### 📚 Evidence")

    if not evidence:

        st.info(
            "No supporting evidence was found."
        )

        return

    for evidence_item in evidence:

        show_evidence_card(
            evidence_item
        )


# =========================================================
# LIVE CLAIM RESULT
# =========================================================

def display_live_result(item):

    claim = item.get(
        "claim",
        ""
    )

    verdict = item.get(
        "verdict",
        "INSUFFICIENT_EVIDENCE"
    )

    confidence = float(
        item.get(
            "confidence",
            0.0
        )
    )

    verification = item.get(
        "verification",
        {}
    )

    st.markdown(
        "### 📝 Detected Claim"
    )

    st.write(claim)

    # -----------------------------------------------------
    # Verdict
    # -----------------------------------------------------

    if verdict == "SUPPORTED":

        st.success(
            f"🟢 SUPPORTED — "
            f"{confidence * 100:.1f}%"
        )

    elif verdict == "CONTRADICTED":

        st.error(
            f"🔴 CONTRADICTED — "
            f"{confidence * 100:.1f}%"
        )

    else:

        st.warning(
            f"🟡 INSUFFICIENT EVIDENCE — "
            f"{confidence * 100:.1f}%"
        )

    # -----------------------------------------------------
    # Explanation
    # -----------------------------------------------------

    explanation = verification.get(
        "explanation"
    )

    if explanation:

        st.info(
            explanation
        )

    # -----------------------------------------------------
    # Evidence
    # -----------------------------------------------------

    evidence = verification.get(
        "results",
        []
    )

    if evidence:

        with st.expander(
            f"📚 Evidence ({len(evidence)})"
        ):

            for evidence_item in evidence:

                show_evidence_card(
                    evidence_item
                )

    else:

        st.caption(
            "No supporting evidence was found."
        )


# =========================================================
# LIVE DATA SECTION
# =========================================================

@st.fragment(run_every="5s")
def live_data_fragment():

    try:

        status = get_live_status()

    except Exception as e:

        st.error(
            f"Backend connection failed: {e}"
        )

        return

    running = status.get(
        "running",
        False
    )

    hashtag = status.get(
        "hashtag"
    )

    posts_processed = status.get(
        "posts_processed",
        0
    )

    claims_detected = status.get(
        "claims_detected",
        0
    )

    # -----------------------------------------------------
    # Get live results
    # -----------------------------------------------------

    try:

        results = get_live_results()

    except Exception:

        results = []

    supported = sum(
        1
        for item in results
        if item.get("verdict")
        == "SUPPORTED"
    )

    contradicted = sum(
        1
        for item in results
        if item.get("verdict")
        == "CONTRADICTED"
    )

    insufficient = sum(
        1
        for item in results
        if item.get("verdict")
        == "INSUFFICIENT_EVIDENCE"
    )

    # =====================================================
    # LIVE STATUS
    # =====================================================

    if running:

        st.success(
            f"🟢 LIVE — Monitoring #{hashtag}"
        )

    else:

        st.info(
            "⚪ Live monitor is stopped."
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    st.markdown(
        "### 📊 Live Statistics"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Posts",
            posts_processed
        )

    with col2:

        st.metric(
            "Claims",
            claims_detected
        )

    with col3:

        st.metric(
            "🟢 Supported",
            supported
        )

    with col4:

        st.metric(
            "🔴 Contradicted",
            contradicted
        )

    with col5:

        st.metric(
            "🟡 Insufficient",
            insufficient
        )

    # =====================================================
    # LIVE CLAIMS
    # =====================================================

    st.markdown(
        "### ⚡ Live Claims"
    )

    if not results:

        st.info(
            "No claims detected yet."
        )

        if running:

            st.caption(
                "Waiting for new Mastodon posts..."
            )

        return

    for index, item in enumerate(
        results,
        start=1
    ):

        post = item.get(
            "post",
            {}
        )

        account = post.get(
            "account",
            {}
        )

        username = (
            account.get("display_name")
            or account.get("username")
            or "Unknown user"
        )

        created_at = post.get(
            "created_at",
            ""
        )

        st.markdown(
            f"**👤 {username}**  "
            f"`{created_at}`"
        )

        display_live_result(
            item
        )

        st.divider()


# =========================================================
# LIVE MONITOR CONTROLS
# =========================================================

def show_live_monitor():

    st.subheader(
        "🔴 Live Claim Monitor"
    )

    st.caption(
        "Monitor public Mastodon posts in real time, "
        "detect factual claims, and verify them automatically."
    )

    # -----------------------------------------------------
    # Check current backend status
    # -----------------------------------------------------

    try:

        status = get_live_status()

    except Exception as e:

        st.error(
            f"Unable to connect to backend: {e}"
        )

        return

    running = status.get(
        "running",
        False
    )

    current_hashtag = status.get(
        "hashtag",
        ""
    )

    # -----------------------------------------------------
    # Hashtag
    # -----------------------------------------------------

    hashtag = st.text_input(
        "Mastodon Hashtag",
        value=current_hashtag or "",
        placeholder="movies",
        disabled=running,
        key="live_hashtag",
    )

    # -----------------------------------------------------
    # Controls
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ Start Monitoring",
            disabled=running,
            type="primary",
            width="stretch",
            key="start_live_monitor",
        ):

            if not hashtag.strip():

                st.warning(
                    "Please enter a hashtag."
                )

                return

            try:

                result = start_live_monitor(
                    hashtag.strip()
                )

                st.success(
                    result.get(
                        "message",
                        "Live monitoring started."
                    )
                )

                # One full rerun is appropriate here
                # because the user explicitly changed
                # the monitor state.
                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to start monitor: {e}"
                )

    with col2:

        if st.button(
            "⏹ Stop Monitoring",
            disabled=not running,
            width="stretch",
            key="stop_live_monitor",
        ):

            try:

                result = stop_live_monitor()

                st.info(
                    result.get(
                        "message",
                        "Live monitoring stopped."
                    )
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to stop monitor: {e}"
                )

    # -----------------------------------------------------
    # Live fragment
    # -----------------------------------------------------

    live_data_fragment()


# =========================================================
# MAIN VERIFICATION UI
# =========================================================

def show_single_verification():

    st.subheader(
        "🔍 Verify Information"
    )

    mode = st.radio(
        "Choose verification method",
        [
            "Social Media Post",
            "Enter Claim",
            "Live Monitor",
        ],
        horizontal=True,
        key="verification_mode",
    )

    # =====================================================
    # SOCIAL MEDIA
    # =====================================================

    if mode == "Social Media Post":

        url = st.text_input(
            "🔗 Paste Social Media Post URL",
            placeholder=(
                "https://mastodon.social/@username/123456789"
            ),
            key="social_post_url",
        )

        st.caption(
            "Paste a public Mastodon post URL. "
            "VeritasAI will extract and verify factual claims."
        )

        if st.button(
            "🔍 Verify Post",
            key="verify_social_post",
            type="primary",
        ):

            if not url.strip():

                st.warning(
                    "Please paste a social media post URL."
                )

                return

            with st.spinner(
                "🔍 Fetching post and verifying..."
            ):

                try:

                    result = verify_social_post(
                        url
                    )

                except Exception as e:

                    st.error(
                        f"Verification failed: {e}"
                    )

                    return

            claims_found = result.get(
                "claims_found",
                0
            )

            if claims_found == 0:

                st.warning(
                    result.get(
                        "message",
                        "No factual claim was detected."
                    )
                )

                return

            st.success(
                f"Verification complete — "
                f"{claims_found} claim(s) detected."
            )

            for index, item in enumerate(
                result.get(
                    "results",
                    []
                ),
                start=1,
            ):

                st.markdown(
                    f"### 📝 Detected Claim {index}"
                )

                st.write(
                    item.get(
                        "claim",
                        ""
                    )
                )

                display_verification_result(
                    item.get(
                        "verification",
                        {}
                    )
                )

    # =====================================================
    # MANUAL CLAIM
    # =====================================================

    elif mode == "Enter Claim":

        claim = st.text_area(
            "📝 Enter a claim to verify",
            placeholder=(
                "Example: Titanic was directed by James Cameron."
            ),
            height=120,
            key="single_claim",
        )

        top_k = st.slider(
            "Top K Evidence",
            1,
            10,
            5,
            key="single_top_k",
        )

        if st.button(
            "🔍 Verify Claim",
            key="verify_single",
            type="primary",
        ):

            if not claim.strip():

                st.warning(
                    "Please enter a claim."
                )

                return

            with st.spinner(
                "🔍 Searching trusted sources..."
            ):

                try:

                    result = verify_claim(
                        claim,
                        top_k
                    )

                except Exception as e:

                    st.error(
                        f"Verification failed: {e}"
                    )

                    return

            st.success(
                "Verification Complete"
            )

            display_verification_result(
                result
            )

    # =====================================================
    # LIVE MONITOR
    # =====================================================

    elif mode == "Live Monitor":

        show_live_monitor()
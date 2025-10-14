# dashboard.py

import streamlit as st
import requests
import re
import time  # <-- THIS IS THE FIX

st.set_page_config(
    layout="wide",
    page_title="AI Coding Assistant",
    page_icon="✨"
)

BACKEND_URL = "http://127.0.0.1:8000"

# -------------------- Session State --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_code" not in st.session_state:
    st.session_state.current_code = ""
if "analysis_report" not in st.session_state:
    st.session_state.analysis_report = ""

# -------------------- Report Parsing --------------------
def parse_and_display_report(report_text):
    # Header section with style similar to chat
    st.markdown(
        "<h2 style='font-size:26px; margin-bottom:0; color:#3B82F6;'>📋 AI Analysis Report</h2>",
        unsafe_allow_html=True
    )
    st.markdown("<hr style='margin-top:4px; margin-bottom:18px;'>", unsafe_allow_html=True)

    # Clean markdown formatting (avoid bold ** artifacts)
    cleaned_report_text = report_text.replace("**", "")

    # Extract corrected code if present
    code_match = re.search(
        r"### (?:[0-9]+\.\s)?(?:Final\s)?Corrected\s(?:&\s)?(?:Optimized\s)?Code\n```(?P<lang>\w+)?\n(?P<code>[\s\S]+)```",
        cleaned_report_text,
        re.IGNORECASE
    )

    if code_match:
        analysis_text = cleaned_report_text[:code_match.start()].strip()
        corrected_code = code_match.group('code').strip()
        lang = code_match.group('lang') or "text"

        # Styled analysis text box
        with st.container():
            st.markdown(
                "<div style='background-color:#F8FAFC; padding:15px; border-radius:10px; border:1px solid #E5E7EB;'>"
                "<h4 style='color:#2563EB; margin-top:0;'>💡 Detailed Analysis</h4>"
                f"<div style='font-size:15px; color:#111827; line-height:1.6;'>{analysis_text}</div>"
                "</div>",
                unsafe_allow_html=True
            )

        # Divider
        st.markdown("<br><hr style='margin:20px 0;'>", unsafe_allow_html=True)

        # Code display with Streamlit's code block
        with st.expander("✨ Suggested / Corrected Code", expanded=True):
            st.code(corrected_code, language=lang)
    else:
        # If parsing fails, show formatted text anyway
        st.markdown(
            "<div style='background-color:#F8FAFC; padding:15px; border-radius:10px; border:1px solid #E5E7EB;'>"
            "<h4 style='color:#2563EB; margin-top:0;'>💡 Full AI Feedback</h4>"
            f"<div style='font-size:15px; color:#111827; line-height:1.6;'>{cleaned_report_text}</div>"
            "</div>",
            unsafe_allow_html=True
        )

    # -------------------- Auto-scroll to report --------------------
    st.markdown(
        """
        <script>
            const reportSection = document.querySelector('h2');
            if(reportSection){ reportSection.scrollIntoView({behavior: 'smooth'}); }
        </script>
        """,
        unsafe_allow_html=True
    )

# -------------------- Sidebar --------------------
with st.sidebar:
    st.title("AI Assistant")
    st.markdown("Your ultimate partner for writing exceptional code.")

    st.header("1. Select Language")
    language = st.selectbox(
        "Which language is your code in?",
        ["Java", "Python", "JavaScript", "C++", "C", "SQL"],
        label_visibility="collapsed"
    ).lower()

    st.header("2. Choose Your Goal")
    intent_options = {
        "Find & Fix All Errors": "fix_errors",
        "Optimize Performance": "optimize",
        "Improve Readability & Style": "improve_style",
        "Generate Unit Tests": "generate_tests",
        "Explain This Code": "explain_code",
    }
    intent_selection = st.radio("What do you need help with?", options=intent_options.keys())
    intent = intent_options[intent_selection]

# -------------------- Main Layout --------------------
col1, col2 = st.columns(2)

# --------- Left Column: Code Input ----------
with col1:
    st.header("Your Code")
    pasted_code = st.text_area("Paste your code snippet here", height=550, label_visibility="collapsed", key="code_input")

    analyze_button = st.button("🚀 Get Full AI Analysis", use_container_width=True, type="primary")

    if analyze_button and pasted_code:
        st.session_state.current_code = pasted_code
        st.session_state.analysis_report = ""
        st.session_state.chat_history = []

        payload = {"code": pasted_code, "language": language, "intent": intent}
        with st.spinner("Your personal AI expert is performing a deep analysis..."):
            try:
                response = requests.post(f"{BACKEND_URL}/review", json=payload, timeout=120)
                if response.status_code == 200:
                    st.session_state.analysis_report = response.json()["report"]

                    # -----------------------------
                    # Show persistent success message for 7 seconds
                    # -----------------------------
                    message_placeholder = st.empty()
                    message_placeholder.success("🎉 Analysis Complete! Report generated below.")
                    time.sleep(7)
                    message_placeholder.empty()  # Remove after 7s

                    st.rerun()  # Re-run to display report
                else:
                    st.session_state.analysis_report = f"Error: {response.text}"
            except requests.exceptions.ConnectionError:
                st.session_state.analysis_report = "Connection Error: Could not connect to the backend."

# --------- Right Column: Chat ----------
with col2:

    if st.session_state.current_code:
        st.header("💬 Chat About This Code")

        chat_container = st.container(height=550)
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Ask a follow-up question..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            with chat_container:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    with st.spinner("Thinking..."):
                        chat_payload = {
                            "code_context": st.session_state.current_code,
                            "history": st.session_state.chat_history,
                            "language": language
                        }
                        try:
                            chat_response = requests.post(f"{BACKEND_URL}/chat", json=chat_payload)
                            if chat_response.status_code == 200:
                                ai_reply = chat_response.json()["reply"]
                                message_placeholder.markdown(ai_reply)
                                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                            else:
                                error_msg = f"Error: {chat_response.text}"
                                message_placeholder.error(error_msg)
                        except requests.exceptions.ConnectionError:
                            error_msg = "Connection Error: Could not connect to the backend."
                            message_placeholder.error(error_msg)
    else:
        st.info("Paste your code on the left and click 'Get Full AI Analysis' to begin.")

# -------------------- Display Report --------------------
if st.session_state.analysis_report:
    st.markdown("---")
    parse_and_display_report(st.session_state.analysis_report)

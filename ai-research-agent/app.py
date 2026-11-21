
import streamlit as st

from src.agent import conduct_research
from src.memory import (
    initialize_database,
    get_history,
    get_report,
    delete_research
)
from src.exporter import create_pdf, create_docx

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="R",
    layout="wide"
)

initialize_database()

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_report" not in st.session_state:
    st.session_state.selected_report = None

if "delete_confirmation" not in st.session_state:
    st.session_state.delete_confirmation = None

# =====================================
# EXPORT FUNCTION
# =====================================

def render_export_buttons(report, key_prefix):

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download PDF",
            data=create_pdf(report),
            file_name="research_report.pdf",
            mime="application/pdf",
            key=f"{key_prefix}_pdf"
        )

    with col2:
        st.download_button(
            "Download Word",
            data=create_docx(report),
            file_name="research_report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key=f"{key_prefix}_docx"
        )

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("AI Research Agent")

    if st.button("+ New Research", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_report = None
        st.rerun()

    st.divider()

    st.subheader("Research Settings")

    research_mode = st.selectbox(
        "Research Mode",
        [
            "General",
            "Academic",
            "Technical",
            "Cybersecurity"
        ]
    )

    st.divider()

    st.subheader("Research History")

    history = get_history()

    for research_id, topic, created_at in history[:20]:

        col1, col2 = st.columns([5, 1])

        with col1:
            if st.button(
                topic[:35],
                key=f"history_{research_id}",
                use_container_width=True
            ):
                st.session_state.selected_report = research_id
                st.session_state.messages = []
                st.session_state.delete_confirmation = None
                st.rerun()

        with col2:
            if st.button(
                "X",
                key=f"delete_{research_id}",
                help="Delete research"
            ):
                st.session_state.delete_confirmation = research_id

    # Deletion confirmation
    if st.session_state.delete_confirmation is not None:

        research_id = st.session_state.delete_confirmation

        st.warning("Delete this research permanently?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, delete", key="confirm_delete"):

                delete_research(research_id)

                if st.session_state.selected_report == research_id:
                    st.session_state.selected_report = None

                st.session_state.delete_confirmation = None
                st.rerun()

        with col2:
            if st.button("Cancel", key="cancel_delete"):
                st.session_state.delete_confirmation = None
                st.rerun()

# =====================================
# MAIN INTERFACE
# =====================================

st.title("AI Research Agent")

st.caption(
    "Your intelligent assistant for web research and information analysis."
)

# =====================================
# WELCOME MESSAGE
# =====================================

if not st.session_state.messages and not st.session_state.selected_report:

    st.markdown(
        """
        <div style="text-align:center; padding:70px 10px 30px;">
            <h2>What would you like to research?</h2>
            <p style="color:gray;">
                Ask a question and let AI Research Agent investigate it.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================
# DISPLAY SELECTED HISTORY
# =====================================

if st.session_state.selected_report:

    report = get_report(st.session_state.selected_report)

    if report:

        st.markdown("### Previous Research")

        st.markdown(report)

        render_export_buttons(
            report,
            f"history_{st.session_state.selected_report}"
        )

        st.download_button(
            "Download Research Report (Markdown)",
            data=report,
            file_name="research_report.md",
            mime="text/markdown",
            key=f"history_download_{st.session_state.selected_report}"
        )

# =====================================
# DISPLAY CHAT MESSAGES
# =====================================

for index, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("sources"):

            with st.expander("View Research Sources"):

                for number, source in enumerate(
                    message["sources"], start=1
                ):

                    st.markdown(f"**{number}. {source['title']}**")
                    st.write(source["snippet"])
                    st.markdown(f"[Open Source]({source['url']})")

        if message["role"] == "assistant" and message.get("query"):

            render_export_buttons(
                message["content"],
                f"chat_{index}"
            )

            st.download_button(
                "Download Research Report (Markdown)",
                data=message["content"],
                file_name="research_report.md",
                mime="text/markdown",
                key=f"download_{index}"
            )

            if st.button(
                "Regenerate",
                key=f"regenerate_{index}"
            ):

                with st.spinner("Regenerating research..."):

                    result = conduct_research(
                        message["query"],
                        max_results=5,
                        mode=message.get("mode", "General")
                    )

                    if result["success"]:

                        st.session_state.messages[index] = {
                            "role": "assistant",
                            "content": result["report"],
                            "sources": result["sources"],
                            "query": message["query"],
                            "mode": message.get("mode", "General")
                        }

                        st.rerun()

                    else:
                        st.error(result["error"])

# =====================================
# CHAT INPUT
# =====================================

prompt = st.chat_input(
    "Ask anything you want to research..."
)

if prompt:

    st.session_state.selected_report = None

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Searching the web and analysing information..."):

            try:

                result = conduct_research(
                    prompt,
                    max_results=5,
                    mode=research_mode
                )

                if result["success"]:

                    report = result["report"]

                    st.markdown(report)

                    render_export_buttons(
                        report,
                        f"new_{len(st.session_state.messages)}"
                    )

                    with st.expander("View Research Sources"):

                        for number, source in enumerate(
                            result["sources"], start=1
                        ):

                            st.markdown(
                                f"**{number}. {source['title']}**"
                            )

                            st.write(source["snippet"])

                            st.markdown(
                                f"[Open Source]({source['url']})"
                            )

                    st.download_button(
                        "Download Research Report (Markdown)",
                        data=report,
                        file_name="research_report.md",
                        mime="text/markdown",
                        key=f"new_download_{len(st.session_state.messages)}"
                    )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": report,
                        "sources": result["sources"],
                        "query": prompt,
                        "mode": research_mode
                    })

                else:

                    st.error(result["error"])

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["error"]
                    })

            except Exception as error:

                st.error(f"Research failed: {error}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Research failed: {error}"
                })
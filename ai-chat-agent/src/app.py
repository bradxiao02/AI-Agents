import sys
from pathlib import Path

import streamlit as st

# Allow imports from the src directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import (
    system_prompt,
    get_ai_response,
    choose_tool,
    execute_tool,
    get_recent_history,
    load_memory,
    save_memory,
    clear_history,
    validate_user_input
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Chat Agent",
    page_icon="AI",
    layout="centered"
)


# ==========================================
# SESSION INITIALIZATION
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

if "last_tool" not in st.session_state:
    st.session_state.last_tool = None


# ==========================================
# PAGE HEADER
# ==========================================

st.title("AI Chat Agent")
st.caption("A general-purpose AI assistant powered by Ollama.")

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Agent Controls")
    st.write("Manage your conversation.")

    if st.button("Clear Conversation", use_container_width=True):

        st.session_state.messages = []
        st.session_state.last_tool = None

        clear_history()

        st.rerun()

    st.divider()

    st.subheader("Agent Information")

    st.write("Model: Qwen 2.5 1.5B")
    st.write("Engine: Ollama")
    st.write("Tools: 5 registered")


# ==========================================
# DISPLAY CONVERSATION
# ==========================================

for message in st.session_state.messages:

    if not isinstance(message, dict):
        continue

    role = message.get("role")
    content = message.get("content")

    if role in ("user", "assistant") and isinstance(content, str):

        with st.chat_message(role):
            st.markdown(content)


# ==========================================
# USER INPUT
# ==========================================

user_message = st.chat_input("Ask me anything...")


if user_message:

    # --------------------------------------
    # INPUT VALIDATION
    # --------------------------------------

    if not validate_user_input(user_message):

        st.error("Invalid input. Maximum length is 5,000 characters.")

    else:

        user_message = user_message.strip()

        # ----------------------------------
        # COMMAND HANDLING
        # ----------------------------------

        if user_message.lower() == "/clear":

            st.session_state.messages = []
            st.session_state.last_tool = None

            clear_history()

            st.success("Conversation cleared.")

            st.rerun()

        elif user_message.lower() == "/history":

            message_count = len(st.session_state.messages)

            st.info(
                f"Your conversation contains {message_count} messages."
            )

        else:

            # ------------------------------
            # DISPLAY USER MESSAGE
            # ------------------------------

            st.session_state.messages.append({
                "role": "user",
                "content": user_message
            })

            with st.chat_message("user"):
                st.markdown(user_message)

            # ------------------------------
            # TOOL SELECTION AND EXECUTION
            # ------------------------------

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    tool_decision = choose_tool(user_message)

                    execution = execute_tool(tool_decision)

                    if not isinstance(execution, dict):
                        st.error("Unexpected tool execution response.")
                        st.stop()

                    if not execution.get("success", False):
                        st.error(
                            execution.get(
                                "error",
                                "Tool execution failed."
                            )
                        )
                        st.stop()

                    tool_used = execution.get("tool_used")
                    tool_result = execution.get("result")

                    if tool_used:
                        st.caption(f"Tool used: {tool_used}")

                    # --------------------------
                    # PREPARE CONVERSATION
                    # CONTEXT
                    # --------------------------

                    recent_history = get_recent_history(
                        st.session_state.messages[:-1]
                    )

                    if tool_used:

                        messages = recent_history + [
                            {
                                "role": "user",
                                "content": (
                                    f"Current request: {user_message}\n\n"
                                    f"Tool result: {tool_result}\n\n"
                                    "Use the tool result to answer the "
                                    "user naturally and accurately. "
                                    "Do not invent additional results."
                                )
                            }
                        ]

                    else:

                        messages = recent_history + [
                            {
                                "role": "user",
                                "content": user_message
                            }
                        ]

                    # --------------------------
                    # SEND REQUEST TO OLLAMA
                    # --------------------------

                    payload = {
                        "model": "qwen2.5:1.5b",
                        "messages": [system_prompt] + messages,
                        "stream": False
                    }

                    ai_message = get_ai_response(payload)

                    # --------------------------
                    # DISPLAY AND SAVE RESPONSE
                    # --------------------------

                    if ai_message:

                        st.markdown(ai_message)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": ai_message
                        })

                        save_memory(st.session_state.messages)

                    else:

                        st.error(
                            "Unable to get a response from the AI model. "
                            "Check whether Ollama is running."
                        )

                        st.session_state.messages.pop()

            st.rerun()

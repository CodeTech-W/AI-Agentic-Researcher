import streamlit as st
from ai_researcher_2 import graph, config
from pathlib import Path
import glob
import os

# =========================================
# Page Config
# =========================================

st.set_page_config(
    page_title="AI Agentic Researcher",
    layout="wide"
)

st.title("📚 AI Agentic Researcher")
st.write("Generate complete research papers with AI")

# =========================================
# Session State
# =========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================
# Chat Input
# =========================================

user_input = st.chat_input(
    "Write a research paper on Prompt Engineering"
)

# =========================================
# User Message
# =========================================

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    st.chat_message("user").write(user_input)

    chat_input = {
        "messages": st.session_state.messages
    }

    try:

        with st.spinner("Researching papers..."):

            full_response = ""
            placeholder = st.empty()

            # =========================================
            # STREAM RESPONSE (SAFE VERSION)
            # =========================================

            for s in graph.stream(
                chat_input,
                config,
                stream_mode="values"
            ):

                messages = s.get("messages", [])
                if not messages:
                    continue

                message = messages[-1]

                # -------------------------
                # Tool Calls
                # -------------------------
                if hasattr(message, "tool_calls") and message.tool_calls:

                    for tool_call in message.tool_calls:
                        st.info(f"Tool Called: {tool_call.get('name', 'unknown')}")

                # -------------------------
                # Content Handling (FIXED)
                # -------------------------
                if hasattr(message, "content") and message.content:

                    content = message.content

                    # safety for non-string outputs
                    if not isinstance(content, str):
                        content = str(content)

                    full_response += content + "\n"

                    placeholder.chat_message("assistant").write(full_response)

            # =========================================
            # Save Chat History
            # =========================================

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

            # =========================================
            # PDF DOWNLOAD
            # =========================================

            pdfs = glob.glob("output/*.pdf")

            if pdfs:

                latest_pdf = max(pdfs, key=os.path.getctime)

                st.success("PDF Generated Successfully!")

                with open(latest_pdf, "rb") as f:
                    st.download_button(
                        label="📥 Download Research Paper PDF",
                        data=f,
                        file_name=Path(latest_pdf).name,
                        mime="application/pdf"
                    )

    except Exception as e:
        st.error(f"Error: {str(e)}")
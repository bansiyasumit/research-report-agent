"""
Streamlit frontend.

Flow:
1. Sidebar: pick a free Gemini model, paste your Gemini API key, paste a
   Serper API key.
2. Main: topic input + "Run research" button -> runs the Phase 1 crew
   (research -> analysis -> fact-check).
3. Editable text area showing the Phase 1 output — this IS the
   human-in-the-loop checkpoint. Nothing in Phase 2 runs until the user
   clicks approve, and Phase 2 uses whatever text is in the box at that
   point (their edits included), not a re-run of Phase 1.
4. "Approve & generate report" button -> runs the Phase 2 crew.
5. Download buttons for the final report (PDF / DOCX).

All credentials live only in st.session_state / local variables for the
lifetime of this browser session's script run — never written to disk,
never logged, never read from os.environ (see crew/tools.py for the one
necessary exception forced by the SerperDevTool library itself).
"""

import tempfile
from pathlib import Path

import streamlit as st

from crew.crew_builder import build_phase1_crew, build_phase2_crew
from crew.tools import build_search_tool
from utils.llm_factory import MODEL_OPTIONS, build_llm
from utils.report_export import markdown_to_docx, markdown_to_pdf

st.set_page_config(page_title="Research & Report Agent", layout="wide")
st.title("Research & Report Automation Agent")
st.caption(
    "Multi-agent research, fact-checking, and report writing — powered by "
    "a free Gemini API key, nothing is stored."
)

# session_state holds the Phase 1 output across reruns so the editable
# text area survives the "Approve" button click (Streamlit reruns the
# whole script on every interaction, so this can't just be a local var).
if "findings" not in st.session_state:
    st.session_state.findings = ""
if "report_markdown" not in st.session_state:
    st.session_state.report_markdown = ""

with st.sidebar:
    st.header("Model")
    model_label = st.selectbox("Gemini model", list(MODEL_OPTIONS.keys()))
    selected_model = MODEL_OPTIONS[model_label]
    st.caption(
        "Gemini's free tier gives newer models a much smaller daily "
        "request quota than the -Lite models, and a single research run "
        "makes many LLM calls — switch models here if you hit a quota or "
        "'high demand' error."
    )
    st.divider()
    st.header("API Keys")
    llm_api_key = st.text_input("Gemini API Key", type="password")
    serper_api_key = st.text_input("Serper API Key", type="password")
    st.caption(
        "Keys are used only for this session's requests and are never "
        "saved to disk or logged."
    )
    st.divider()
    st.markdown(
        "**Get free keys:**\n"
        "- [Gemini](https://aistudio.google.com/apikey)\n"
        "- [Serper](https://serper.dev)"
    )

topic = st.text_input("Research topic", placeholder="e.g. The EV battery supply chain in 2025")

run_disabled = not (topic and llm_api_key and serper_api_key)
if st.button("Run research", type="primary", disabled=run_disabled):
    try:
        llm = build_llm(llm_api_key, model=selected_model)
        search_tool = build_search_tool(serper_api_key)
        phase1_crew = build_phase1_crew(llm, search_tool, topic)
        with st.spinner("Researching, analyzing, and fact-checking — this can take a few minutes..."):
            result = phase1_crew.kickoff()
        st.session_state.findings = str(result)
        st.session_state.report_markdown = ""  # clear any stale report from a previous topic
    except Exception as e:
        st.error(f"Phase 1 failed: {e}")

if run_disabled and not st.session_state.findings:
    st.info("Enter a topic and both API keys to begin.")

if st.session_state.findings:
    st.subheader("Review findings")
    st.caption(
        "This is the human-in-the-loop checkpoint. Edit anything below "
        "before approving — the report is written from exactly this text."
    )
    edited_findings = st.text_area(
        "Combined research, analysis, and fact-check findings",
        value=st.session_state.findings,
        height=500,
        key="findings_editor",
    )
    st.session_state.findings = edited_findings

    if st.button("Approve & generate report", type="primary"):
        try:
            llm = build_llm(llm_api_key, model=selected_model)
            phase2_crew = build_phase2_crew(llm, st.session_state.findings, topic)
            with st.spinner("Writing the final report..."):
                result = phase2_crew.kickoff()
            st.session_state.report_markdown = str(result)
        except Exception as e:
            st.error(f"Phase 2 failed: {e}")

if st.session_state.report_markdown:
    st.subheader("Final report")
    st.markdown(st.session_state.report_markdown)

    tmp_dir = Path(tempfile.mkdtemp())
    pdf_path = tmp_dir / "report.pdf"
    docx_path = tmp_dir / "report.docx"
    markdown_to_pdf(st.session_state.report_markdown, str(pdf_path))
    markdown_to_docx(st.session_state.report_markdown, str(docx_path))

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download PDF",
            data=pdf_path.read_bytes(),
            file_name="report.pdf",
            mime="application/pdf",
        )
    with col2:
        st.download_button(
            "Download DOCX",
            data=docx_path.read_bytes(),
            file_name="report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

import streamlit as st
from ai_quiz_builder.pdf_handler import extract_text
from ai_quiz_builder.logic import StudyAssistant

# Initialize StudyAssistant
assistant = StudyAssistant()

# Set Streamlit page configuration
st.set_page_config(page_title="Study Notes Agent", layout="wide")

# Session state for extracted PDF text
if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""

# Sidebar for PDF upload
with st.sidebar:
    st.header("Upload Lecture PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # Pass bytes_data directly to pypdf
        st.session_state["pdf_text"] = extract_text(bytes_data)
        if st.session_state["pdf_text"].startswith("Error:"):
            st.error(st.session_state["pdf_text"])
            st.session_state["pdf_text"] = "" # Clear invalid PDF text
        else:
            st.success("PDF processed successfully!")

# Main area
st.title("📚 Study Notes Agent")

if st.session_state["pdf_text"]:
    st.subheader("Document Content (Preview)")
    st.expander("Click to view full document text").write(st.session_state["pdf_text"][:1000] + "..." if len(st.session_state["pdf_text"]) > 1000 else st.session_state["pdf_text"])

    # Tabs for different functionalities
    tab1, tab2 = st.tabs(["Summarizer", "Quizzer"])

    with tab1:
        st.header("Generate Study Notes")
        if st.button("Generate Notes"):
            with st.spinner("Generating notes..."):
                response = assistant.process_task(
                    "Summarize this text into key concepts and important points.",
                    st.session_state["pdf_text"]
                )
                st.markdown("### Generated Notes")
                st.markdown(response)

    with tab2:
        st.header("Generate Quiz Questions")
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz..."):
                response = assistant.process_task(
                    "Create 5 Multiple Choice Questions (MCQs) based on this text, each with 4 options and the correct answer indicated.",
                    st.session_state["pdf_text"]
                )
                st.markdown("### Generated Quiz")
                st.markdown(response)
else:
    st.info("Please upload a PDF document in the sidebar to get started.")


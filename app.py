import streamlit as st

st.title("Mortgage Analysis Assistant")

st.write("Upload a mortgage document to begin.")

uploaded_file = st.file_uploader(
    "Upload Mortgage PDF",
    type=["pdf"]
)
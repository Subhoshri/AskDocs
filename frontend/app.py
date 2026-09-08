import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AskDocs",
    page_icon="📚",
    layout="centered"
)


st.title("📚 AskDocs")
st.caption("AI-powered document question-answering system")


# -----------------------------
# Upload documents
# -----------------------------

st.header("Upload Documents")

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


if st.button("Upload Documents"):

    if not uploaded_files:
        st.warning("Please select at least one PDF.")

    else:

        for uploaded_file in uploaded_files:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            try:

                response = requests.post(
                    f"{API_URL}/documents/upload",
                    files=files
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        f"{data['filename']} uploaded successfully "
                        f"({data['chunks_indexed']} chunks)"
                    )

                else:

                    st.error(
                        f"Upload failed: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the AskDocs backend."
                )


# -----------------------------
# Ask questions
# -----------------------------

st.header("Ask a Question")

question = st.text_input(
    "Enter your question"
)


if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            response = requests.post(
                f"{API_URL}/query",
                json={
                    "question": question,
                    "top_k": 8
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.subheader("Answer")

                st.write(data["answer"])

                st.subheader("Sources")

                for source in data["sources"]:

                    st.write(
                        f"📄 {source['document']} "
                        f"· Page {source['page']}"
                    )

            else:

                st.error(
                    f"Query failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the AskDocs backend."
            )
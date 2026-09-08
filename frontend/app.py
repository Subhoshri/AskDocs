import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AskDocs",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AskDocs")
st.caption(
    "AI-powered document question-answering with "
    "source-aware retrieval"
)


# -----------------------------
# Upload
# -----------------------------

st.header("📄 Upload Documents")

uploaded_files = st.file_uploader(
    "Choose one or more PDF documents",
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

                with st.spinner(
                    f"Processing {uploaded_file.name}..."
                ):

                    response = requests.post(
                        f"{API_URL}/documents/upload",
                        files=files
                    )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        f"✓ {data['filename']} "
                        f"({data['chunks_indexed']} chunks indexed)"
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
# Get documents
# -----------------------------

st.header("📚 Your Documents")

try:

    response = requests.get(
        f"{API_URL}/documents"
    )

    if response.status_code == 200:

        documents = response.json()["documents"]

        if not documents:

            st.info("No documents uploaded yet.")

        else:

            for document in documents:

                col1, col2, col3 = st.columns([5, 1, 1])

                with col1:
                    st.write(f"📄 **{document['filename']}**")

                with col2:
                    st.link_button(
                        "View",
                        f"{API_URL}/documents/"
                        f"{document['document_id']}/file"
                    )

                with col3:
                    if st.button(
                        "Delete",
                        key=f"delete_{document['document_id']}"
                    ):
                        try:
                            response = requests.delete(
                                f"{API_URL}/documents/"
                                f"{document['document_id']}"
                            )

                            if response.status_code == 200:
                                st.success(
                                    f"Deleted {document['filename']}"
                                )
                                st.rerun()
                            else:
                                st.error(
                                    f"Delete failed: {response.text}"
                                )

                        except requests.exceptions.ConnectionError:
                            st.error(
                                "Could not connect to the AskDocs backend."
                            )

except requests.exceptions.ConnectionError:

    st.warning(
        "Backend is not running."
    )


# -----------------------------
# Document selection
# -----------------------------

st.header("🔎 Search Scope")

try:

    response = requests.get(
        f"{API_URL}/documents"
    )

    if response.status_code == 200:

        documents = response.json()["documents"]

        document_options = {
            document["filename"]: document["document_id"]
            for document in documents
        }

        selected_scope = st.radio(
            "Where should AskDocs search?",
            ["All documents", "Specific documents"]
        )

        selected_document_ids = None

        if selected_scope == "Specific documents":

            selected_names = st.multiselect(
                "Select documents",
                options=list(document_options.keys())
            )

            selected_document_ids = [
                document_options[name]
                for name in selected_names
            ]

            if not selected_document_ids:

                st.info(
                    "Select at least one document."
                )


        # -----------------------------
        # Question
        # -----------------------------

        st.header("💬 Ask a Question")

        question = st.text_input(
            "Enter your question",
            placeholder="e.g. What projects are mentioned?"
        )

        if st.button("Ask", type="primary"):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            elif (
                selected_scope == "Specific documents"
                and not selected_document_ids
            ):

                st.warning(
                    "Please select at least one document."
                )

            else:

                try:

                    with st.spinner("Searching documents..."):

                        response = requests.post(
                            f"{API_URL}/query",
                            json={
                                "question": question,
                                "top_k": 8,
                                "document_ids": selected_document_ids
                            }
                        )

                    if response.status_code == 200:

                        data = response.json()

                        # -----------------------------
                        # Answer
                        # -----------------------------

                        st.subheader("Answer")

                        st.write(data["answer"])


                        # -----------------------------
                        # Group sources
                        # -----------------------------

                        st.subheader("Sources")

                        grouped_sources = {}

                        for source in data["sources"]:

                            filename = source["document"]
                            page = source["page"]

                            if filename not in grouped_sources:
                                grouped_sources[filename] = set()

                            grouped_sources[filename].add(page)


                        for filename, pages in grouped_sources.items():

                            page_list = sorted(pages)

                            pages_text = ", ".join(
                                str(page)
                                for page in page_list
                            )

                            st.write(
                                f"📄 **{filename}**  \n"
                                f"Pages: {pages_text}"
                            )

                    else:

                        st.error(
                            f"Query failed: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to the AskDocs backend."
                    )

except requests.exceptions.ConnectionError:

    st.warning(
        "Could not connect to the AskDocs backend."
    )
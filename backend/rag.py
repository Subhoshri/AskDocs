import os
from google import genai


class AnswerGenerator:

    def __init__(self, api_key):

        if not api_key:
            raise ValueError("GEMINI_API_KEY is required.")

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, question, retrieved_chunks):

        if not retrieved_chunks:

            return (
                "I could not find enough relevant information "
                "in the provided documents to answer this question."
            )

        context_parts = []

        for result in retrieved_chunks:

            metadata = result["metadata"]

            context_parts.append(
                f"""
[Source]
Document: {metadata["filename"]}
Page: {metadata["page_number"]}

Content:
{metadata["text"]}
"""
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an AI document question-answering assistant.

Your job is to answer the user's question using ONLY
the information contained in the provided document excerpts.

IMPORTANT:
The retrieved excerpts may contain irrelevant information.
Do NOT mention information merely because it appears in
the context. Use only excerpts that are actually relevant
to the user's question.

Rules:

1. Do not use outside knowledge.
2. Do not invent or assume facts.
3. Ignore irrelevant retrieved excerpts.
4. If the available excerpts do not contain enough relevant
   information, clearly say that the answer cannot be
   determined from the provided documents.
5. Keep answers concise and directly answer the question.
6. Do not unnecessarily list every retrieved passage.
7. When the user asks what a document is about, provide a
   short high-level description of its main subject instead
   of listing acknowledgements, copyright information,
   indexes, references, or other incidental content.
8. If multiple documents contain relevant information,
   organize the answer by document.
9. If relevant documents contain conflicting information,
   explicitly identify the conflict and present both versions.
10. Mention document names and page numbers when citing
    information.

For broad questions such as:
"What is this document about?"
"Summarize this document."
"What does this document contain?"

focus on the main purpose, subject, or content of the document,
not incidental text.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text
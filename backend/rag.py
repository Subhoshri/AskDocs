import os
from google import genai


class AnswerGenerator:

    def __init__(self, api_key):

        if not api_key:
            raise ValueError("GEMINI_API_KEY is required.")

        self.client = genai.Client(api_key=api_key)

    def generate(self, question, retrieved_chunks):

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

Answer the user's question using ONLY the information
provided in the context below.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts.
3. If the context does not contain enough information,
   clearly say that the answer cannot be determined
   from the provided documents.
4. If multiple sources contain conflicting information,
   explicitly identify the conflict.
5. Do not arbitrarily choose one conflicting source.
6. Mention the relevant document and page when presenting
   information from a source.
7. Keep the answer concise and clear.

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
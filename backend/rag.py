from openai import OpenAI

class RAGGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_answer(self, question, retrieved_chunks):
        context_parts = []

        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]

            context_parts.append(
                f"""
                Source: {metadata['filename']}
                Page: {metadata['page_number']}

                Content:
                {metadata['text']}
                """
            )

        context = "\n\n".join(context_parts)
        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided document context.

Rules:
1. Do not invent information.
2. If the context does not contain enough information, say that the answer cannot be determined from the documents.
3. If multiple sources contain conflicting information, explicitly mention the conflict.
4. Cite the relevant document and page for each claim.

Context:
{context}

Question:
{question}
"""

        response = self.client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text
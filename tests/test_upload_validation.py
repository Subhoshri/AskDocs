from fastapi.testclient import TestClient
from backend.main import app, pipeline
import backend.main as main


client = TestClient(app)


def test_reject_non_pdf():
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "notes.txt",
                b"hello world",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert "Only PDF files are supported" in response.json()["detail"]


def test_reject_invalid_pdf_signature():
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "fake.pdf",
                b"this is not actually a pdf",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400
    assert "Invalid PDF file" in response.json()["detail"]


def test_reject_oversized_file():
    large_file = b"%PDF-" + b"a" * (20 * 1024 * 1024)

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "large.pdf",
                large_file,
                "application/pdf"
            )
        }
    )

    assert response.status_code == 413
    assert "20 MB" in response.json()["detail"]


def test_empty_question_rejected():
    response = client.post(
        "/query",
        json={
            "question": "   "
        }
    )

    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]
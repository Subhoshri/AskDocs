from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_list_documents():
    response = client.get("/documents")

    assert response.status_code == 200
    assert "documents" in response.json()


def test_document_not_found():
    response = client.get(
        "/documents/nonexistent-document/file"
    )

    assert response.status_code == 404


def test_delete_nonexistent_document():
    response = client.delete(
        "/documents/nonexistent-document"
    )

    assert response.status_code == 404
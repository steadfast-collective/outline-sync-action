from urllib.parse import urljoin
from requests import Session


DEFAULT_API_BASE_URL = "https://app.getoutline.com/api/"


class OutlineApiSession(Session):

    base_url = None

    def __init__(self, auth_token, base_url=None):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = DEFAULT_API_BASE_URL
        super().__init__()

        self.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {auth_token}",
            }
        )

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL.

        Also applies rate limiting rules from exact. State based on response headers
        """
        url = urljoin(self.base_url, url)
        return super().request(method, url, *args, **kwargs)


class OutlineApi:
    def __init__(self, auth_token, base_url=None):
        self.session = OutlineApiSession(auth_token, base_url=base_url)

    def document_get(self, doc_id: str):
        response = self.session.post("documents.info", json={"id": doc_id})
        response.raise_for_status()
        return response.json()

    def document_create(self, title, collection_id, text, publish=True):
        response = self.session.post(
            "documents.create",
            json={
                "title": title,
                "collectionId": collection_id,
                "text": text,
                "publish": publish,
            },
        )
        response.raise_for_status()
        return response.json()

    def document_update(self, doc_id, title, text, publish=True):
        response = self.session.post(
            "documents.update",
            json={
                "id": doc_id,
                "title": title,
                "text": text,
                "append": False,  # Assumes we always send the full document
                "publish": publish,
            },
        )
        response.raise_for_status()
        return response.json()

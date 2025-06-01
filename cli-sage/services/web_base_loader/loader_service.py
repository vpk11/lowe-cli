import requests

class LoaderService:
    """Service to handle web base loader operations."""

    @staticmethod
    def load(web_path):
        """Load documents from the specified web path."""

        r = requests.get(web_path)
        return r.json()
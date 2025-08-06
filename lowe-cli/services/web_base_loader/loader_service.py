from typing import Union
import requests

# Type alias for JSON data
JsonData = Union[dict, list, str, int, float, bool, None]


class LoaderService:
    """Service to handle web base loader operations."""

    @staticmethod
    def load(web_path: str) -> JsonData:
        """
        Load documents from the specified web path.
        
        Args:
            web_path: The URL path to load JSON data from
            
        Returns:
            JSON data from the web response
        """
        r: requests.Response = requests.get(web_path)
        return r.json()
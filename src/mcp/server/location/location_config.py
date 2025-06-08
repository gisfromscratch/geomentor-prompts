
import os
from typing import Optional, Dict


class ArcGISApiKeyManager:
    """
    ArcGISApiKeyManager provides utility methods for managing ArcGIS API keys.

    Attributes:
        ENV_KEY (str): The environment variable key used to look up the ArcGIS API key.

    Methods:
        get_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
            Retrieves the ArcGIS API key. If an explicit key is provided, it is returned.
            Otherwise, searches the environment variables for a key matching ENV_KEY (case-insensitive).

        add_key_to_params(params: Dict, api_key: Optional[str] = None) -> None:
            Adds the ArcGIS API key to the provided params dictionary under the "token" key.
            The API key is retrieved using get_api_key, optionally using the provided api_key.
    """
    ENV_KEY = "arcgis_api_key"

    @staticmethod
    def get_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
        """
        Retrieve an API key for ArcGIS services.

        If an explicit API key is provided as an argument, it is returned immediately.
        Otherwise, the function searches the environment variables for a key matching
        the expected environment variable name (case-insensitive) defined by
        `ArcGISApiKeyManager.ENV_KEY`. If found, the corresponding value is returned.
        If no API key is found, returns None.

        Args:
            explicit_key (Optional[str]): An explicit API key to use. Defaults to None.

        Returns:
            Optional[str]: The API key if found, otherwise None.
        """
        if explicit_key:
            return explicit_key
        for key, value in os.environ.items():
            if key.lower() == ArcGISApiKeyManager.ENV_KEY:
                return value
        return None

    @staticmethod
    def add_key_to_params(params: Dict, api_key: Optional[str] = None) -> None:
        """
        Adds an API key to the provided parameters dictionary under the "token" key.

        Args:
            params (Dict): The dictionary of parameters to which the API key will be added.
            api_key (Optional[str], optional): An optional API key to use. If not provided, a default key is retrieved.

        Returns:
            None: This function modifies the params dictionary in place.

        Side Effects:
            Modifies the input params dictionary by adding a "token" key if an API key is available.
        """
        key = ArcGISApiKeyManager.get_api_key(api_key)
        if key:
            params["token"] = key

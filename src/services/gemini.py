# KAN-466: Establecer Conexión Segura con APIs de Gemini Enterprise
import httpx
from src.config import config
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

class GeminiService:
    """
    Manages secure and authenticated connections to the Gemini Enterprise API.
    """

    def __init__(self):
        if not config.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is not set. Cannot connect to Gemini.")
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.api_key = config.GEMINI_API_KEY
        self.base_url = config.GEMINI_API_URL
        # Using httpx for async-ready, modern HTTP requests
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Content-Type": "application/json",
            },
            # All communication is over HTTPS/TLS by default with httpx
            timeout=30.0,
        )

    def _get_auth_params(self):
        return {"key": self.api_key}

    def health_check(self) -> bool:
        """
        Performs a health check call to a Gemini API endpoint.
        This is a simulated endpoint for demonstration.
        A real API might have a /health or similar endpoint.
        Here we check if the model is accessible.
        """
        try:
            # Example: a lightweight call to list models
            response = self.client.get(
                f"/v1beta/models",
                params=self._get_auth_params()
            )

            if response.status_code == 200:
                logger.info("Successfully connected to Gemini Enterprise API.")
                return True
            elif response.status_code in [401, 403]:
                logger.error(f"Authentication failed. Status: {response.status_code}. Response: {response.text}")
                return False
            else:
                logger.warning(f"Gemini health check failed with status {response.status_code}.")
                return False
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting {e.request.url!r}: {e}")
            return False

    def generate_content(self, prompt: str) -> str:
        """
        Makes a call to the Gemini API to generate content.
        """
        try:
            response = self.client.post(
                f"/v1beta/models/{config.GEMINI_MODEL_NAME}:generateContent",
                params=self._get_auth_params(),
                json={"contents": [{"parts": [{"text": prompt}]}]}
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling Gemini: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred calling Gemini: {e}")
            raise

# Singleton instance
gemini_service = GeminiService()

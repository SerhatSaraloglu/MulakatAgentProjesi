from app.config import LM_STUDIO_MODEL
from app.llm.providers.lm_studio.client import client
from lmstudio_client import generate_response


def test_legacy_import_exposes_generate_response():
    assert callable(generate_response)


def test_client_uses_current_model_configuration():
    assert client.base_url
    assert LM_STUDIO_MODEL == "google/gemma-3-4b"

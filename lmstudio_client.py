"""Backward-compatible import for the LM Studio client."""

from app.llm.providers.lm_studio.client import generate_response

__all__ = ["generate_response"]
